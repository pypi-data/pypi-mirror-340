import neo4j
import logging
from logging.handlers import RotatingFileHandler
from contextlib import closing
from pathlib import Path
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from pydantic import AnyUrl, BaseModel
from typing import Any
from neo4j import GraphDatabase
import re
import boto3
from botocore.exceptions import ClientError
import json
import os

logger = logging.getLogger('mcp_neo4j_cypher_read_only')
logger.info("Starting MCP neo4j Server")

def is_write_query(query: str) -> bool:
    return re.search(r"\b(MERGE|CREATE|SET|DELETE|REMOVE|ADD)\b", query, re.IGNORECASE) is not None

class Neo4jConnectionInfo(BaseModel):
    """
    Defines how to connect to a Neo4j database.
    If secret_name AND secret_region are provided, the password will be fetched from
    AWS Secrets Manager. If password is provided, it will be used directly.
    """
    uri: str
    user: str
    secret_name: str | None = None
    secret_region: str | None = None
    password: str | None = None

def get_neo4j_password(secret_name: str, secret_region: str) -> str:
    """Fetches the Neo4j password from AWS Secrets Manager."""
    logger.info(f"Attempting to fetch secret '{secret_name}' from region '{secret_region}'")
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager", region_name=secret_region
    )
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response["SecretString"]
        # Assuming the secret stores a JSON object with a 'password' key
        # Adjust the key if your secret is structured differently
        password = json.loads(secret).get("password") 
        if not password:
            # Try getting neo4j_password if password is not found
            password = json.loads(secret).get("neo4j_password")
        if not password:
            raise ValueError(f"Key 'password' or 'neo4j_password' not found in secret '{secret_name}'")
        logger.info(f"Successfully fetched secret '{secret_name}'")
        return password
    except ClientError as e:
        logger.error(f"Error fetching secret '{secret_name}' from region '{secret_region}': {e}")
        # Propagate the error to be handled during connection attempt
        raise e
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        logger.error(f"Error parsing secret '{secret_name}': {e}")
        raise ValueError(f"Could not parse password from secret '{secret_name}'. Ensure it's valid JSON with a 'password' or 'neo4j_password' key.")

class neo4jDatabase:
    def __init__(self, connection_info: Neo4jConnectionInfo):
        """Initialize connection to the neo4j database using connection info."""
        self.connection_info = connection_info
        resolved_password = None

        # Logic to resolve password (direct vs. Secrets Manager)
        if self.connection_info.password is not None and (
            self.connection_info.secret_name is None
            or self.connection_info.secret_region is None
        ):
            logger.debug("Using provided password for Neo4j connection.")
            resolved_password = self.connection_info.password
        elif self.connection_info.password is None and (
            self.connection_info.secret_name is not None
            and self.connection_info.secret_region is not None
        ):
            logger.debug(f"Fetching password from AWS Secrets Manager (Secret: {self.connection_info.secret_name}, Region: {self.connection_info.secret_region}).")
            try:
                resolved_password = get_neo4j_password(
                    self.connection_info.secret_name, self.connection_info.secret_region
                )
            except (ClientError, ValueError) as e:
                # Log the specific error and raise a connection error
                logger.error(f"Failed to retrieve or parse password from Secrets Manager: {e}")
                raise ConnectionError(f"Failed to get Neo4j password from AWS Secrets Manager: {e}") from e
        else:
            # This state indicates a configuration error (e.g., password missing and incomplete secret info)
            logger.error("Invalid Neo4j connection configuration: Provide either a password or both secret_name and secret_region.")
            raise ValueError("Invalid Neo4j connection configuration: Provide either a password or both secret_name and secret_region.")

        if resolved_password is None:
             # Should not happen if logic above is correct, but as a safeguard
            logger.error("Password resolution failed unexpectedly.")
            raise ConnectionError("Could not resolve Neo4j password.")

        logger.debug(f"Initializing database connection to {self.connection_info.uri} for user {self.connection_info.user}")

        try:
            # Include database in the driver arguments if specified
            driver_kwargs = {
                "auth": (self.connection_info.user, resolved_password),
                # Add encryption settings if needed, e.g., based on URI scheme
                # "encrypted": self.connection_info.uri.startswith("neo4j+s"), # Example
                # "trusted_certificates": neo4j.TrustSystemCAs() # Example for system CAs
            }

            d = GraphDatabase.driver(self.connection_info.uri, **driver_kwargs)
            d.verify_connectivity() # This is where the original ServiceUnavailable error occurred
            self.driver = d
            logger.info("Successfully connected to Neo4j and verified connectivity.")
        except neo4j.exceptions.AuthError as e:
             logger.error(f"Authentication failed for user {self.connection_info.user}: {e}")
             # Re-raise with a more context-specific message if desired
             raise ConnectionError(f"Neo4j authentication failed: {e}") from e
        except neo4j.exceptions.ServiceUnavailable as e:
            logger.error(f"Could not connect to Neo4j at {self.connection_info.uri}: {e}. Check network, firewall, URI, and server status.")
            # Re-raise the original error, it might be the root cause unrelated to password
            raise e
        except Exception as e:
            # Catch other potential driver errors
            logger.error(f"Error establishing Neo4j connection to {self.connection_info.uri}: {e}")
            raise ConnectionError(f"Failed to connect to Neo4j: {e}") from e

    def _execute_query(self, query: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Execute a Cypher query and return results as a list of dictionaries"""
        logger.debug(f"Executing query: {query}")
        try:
            result = self.driver.execute_query(query, params)
            counters = vars(result.summary.counters)
            if is_write_query(query):
                logger.debug(f"Write query affected {counters}")
                return [counters]
            else:
                results = [dict(r) for r in result.records]
                logger.debug(f"Read query returned {len(results)} rows")
                return results
        except Exception as e:
            logger.error(f"Database error executing query: {e}\n{query}")
            raise

    def close(self) -> None:
        "Close the Neo4j Driver"
        self.driver.close()


async def main(connection_info: Neo4jConnectionInfo):
    logger.info(f"Connecting to neo4j MCP Server with DB URL: {connection_info.uri}")

    try:
        db = neo4jDatabase(connection_info)
    except (ConnectionError, ValueError, ClientError) as e:
        # Handle connection errors during initialization
        logger.critical(f"Failed to initialize Neo4j database connection: {e}")
        # Exit or raise appropriately so the MCP server doesn't start incorrectly
        # For now, let's re-raise to let the caller handle it.
        raise RuntimeError(f"Neo4j connection failed during startup: {e}") from e

    server = Server("neo4j-manager")

    # Register handlers
    logger.debug("Registering handlers")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools"""
        return [
            types.Tool(
                name="read-neo4j-cypher",
                description="Execute a Cypher query on the neo4j database",
                annotations={
                    "destructiveHint": False,
                    "idempotentHint": True,
                    "readOnlyHint": True,
                    "title": "Read from Neo4j Database"
                },
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Cypher read query to execute"},
                    },
                    "required": ["query"],
                },
            ),
            types.Tool(
                name="get-neo4j-schema",
                description="List all node types, their attributes and their relationships TO other node-types in the neo4j database",
                annotations={
                    "destructiveHint": False,
                    "idempotentHint": True,
                    "readOnlyHint": True,
                    "title": "Get Neo4j Database Schema"
                },
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            )
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Handle tool execution requests"""
        try:
            if name == "get-neo4j-schema":
                results = db._execute_query(
                    """
call apoc.meta.data() yield label, property, type, other, unique, index, elementType
where elementType = 'node' and not label starts with '_'
with label, 
    collect(case when type <> 'RELATIONSHIP' then [property, type + case when unique then " unique" else "" end + case when index then " indexed" else "" end] end) as attributes,
    collect(case when type = 'RELATIONSHIP' then [property, head(other)] end) as relationships
RETURN label, apoc.map.fromPairs(attributes) as attributes, apoc.map.fromPairs(relationships) as relationships
                    """
                )
                return [types.TextContent(type="text", text=str(results))]

            elif name == "read-neo4j-cypher":
                if is_write_query(arguments["query"]):
                    raise ValueError("Only MATCH queries are allowed for read-query")
                results = db._execute_query(arguments["query"])
                return [types.TextContent(type="text", text=str(results))]
            
            else:
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="neo4j",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
