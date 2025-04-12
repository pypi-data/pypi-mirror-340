from . import server
import asyncio
import argparse
import os
import logging
import sys
from .server import Neo4jConnectionInfo

logger = logging.getLogger('mcp_neo4j_cypher')

# Setup basic logging if no handlers are configured
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    """Main entry point for the package."""
    parser = argparse.ArgumentParser(description="MCP Neo4j Cypher Server")
    parser.add_argument("--db-url", required=True, help="Neo4j Bolt connection URL (e.g., bolt://localhost:7687, neo4j+s://your-aura-db.databases.neo4j.io)")
    parser.add_argument("--username", required=True, help="Neo4j username")
    parser.add_argument("--database", default="neo4j", help="Name of the Neo4j database to connect to (default: neo4j)")

    # Group for password options - mutually exclusive
    pw_group = parser.add_mutually_exclusive_group(required=True)
    pw_group.add_argument("--password", help="Neo4j password (use directly)")
    secret_group = pw_group.add_argument_group("AWS Secrets Manager")
    secret_group.add_argument("--secret-name", help="Name of the AWS Secret containing the password")
    secret_group.add_argument("--secret-region", help="AWS Region for the Secret")

    # Logging level argument
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Set the logging level")

    args = parser.parse_args()

    # Set logging level
    log_level = getattr(logging, args.log_level.upper(), logging.INFO)
    # Configure root logger - affects imported libraries too if not configured themselves
    logging.basicConfig(level=log_level, format='%(asctime)s [%(name)s] [%(levelname)s] %(message)s')
    # Set level specifically for this application's logger
    logger.setLevel(log_level)
    logger.info(f"Log level set to {args.log_level.upper()}")

    # Validate Secrets Manager arguments if provided
    if args.secret_name and not args.secret_region:
        parser.error("--secret-region is required when --secret-name is provided.")
    if args.secret_region and not args.secret_name:
        # This case is less likely due to the mutually exclusive group, but good practice
        parser.error("--secret-name is required when --secret-region is provided.")

    # Create ConnectionInfo object
    connection_info = Neo4jConnectionInfo(
        uri=args.db_url,
        user=args.username,
        password=args.password, # Will be None if secret args are used
        secret_name=args.secret_name,
        secret_region=args.secret_region,
        database=args.database
    )

    try:
        # Pass the connection_info object to the server's main coroutine
        asyncio.run(server.main(connection_info))
    except RuntimeError as e:
        # Catch the connection error raised from server.main
        logger.critical(f"Server startup failed: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Server stopped by user.")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        sys.exit(1)

# Optionally expose other important items at package level
__all__ = ["main", "server"]
