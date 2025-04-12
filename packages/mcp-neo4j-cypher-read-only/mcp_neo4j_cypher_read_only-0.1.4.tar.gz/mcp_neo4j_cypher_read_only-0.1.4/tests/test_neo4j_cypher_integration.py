import os
import pytest
import asyncio
from mcp_neo4j_cypher_read_only.server import neo4jDatabase, Neo4jConnectionInfo

@pytest.fixture(scope="function")
def neo4j():
    """Create a Neo4j driver using environment variables for connection details."""
    connection_info = Neo4jConnectionInfo(
        uri=os.environ.get("NEO4J_URL", "localhost:7687"),
        user=os.environ.get("NEO4J_USERNAME", "neo4j"),
        password=os.environ.get("NEO4J_PASSWORD", "password"),
    )
    db = neo4jDatabase(connection_info)

    # Use the internal method on the db instance to clear and add test data
    db._execute_query("MATCH (n) DETACH DELETE n")
    db._execute_query("CREATE (:TestNode {id: 1, name: 'Test'})-[:RELATES_TO]->(:OtherNode {value: 100})")
        
    yield db # Yield the db instance

    db.close() # Close the db instance
    
# Renamed test to reflect read operation
@pytest.mark.asyncio
async def test_execute_cypher_read_query(neo4j):
    # Execute a Cypher query to read a node
    query = "MATCH (n:TestNode {id: 1}) RETURN n.name AS name"
    result = neo4j._execute_query(query)
    
    # Verify the node read
    assert len(result) == 1
    assert result[0]["name"] == "Test"

@pytest.mark.asyncio
async def test_retrieve_schema(neo4j):
    # Execute the schema query used by the get-neo4j-schema tool
    query = """
call apoc.meta.data() yield label, property, type, other, unique, index, elementType
where elementType = 'node' and not label starts with '_'
with label, 
    collect(case when type <> 'RELATIONSHIP' then [property, type + case when unique then " unique" else "" end + case when index then " indexed" else "" end] end) as attributes,
    collect(case when type = 'RELATIONSHIP' then [property, head(other)] end) as relationships
RETURN label, apoc.map.fromPairs(attributes) as attributes, apoc.map.fromPairs(relationships) as relationships
    """
    result = neo4j._execute_query(query)
    
    # Verify the schema result structure for TestNode
    assert isinstance(result, list)
    test_node_schema = next((item for item in result if item["label"] == "TestNode"), None)
    assert test_node_schema is not None
    assert "attributes" in test_node_schema
    assert "relationships" in test_node_schema
    assert test_node_schema["attributes"] == {'id': 'INTEGER', 'name': 'STRING'} # Example assertion, adjust based on actual types
    assert test_node_schema["relationships"] == {'RELATES_TO': 'OtherNode'} # Example assertion


@pytest.mark.asyncio
async def test_execute_complex_read_query(neo4j):
    # Prepare additional test data (fixture already adds some)
    neo4j._execute_query("CREATE (a:Person {name: 'Alice', age: 30})")
    neo4j._execute_query("CREATE (b:Person {name: 'Bob', age: 25})")
    neo4j._execute_query("CREATE (c:Person {name: 'Charlie', age: 35})")
    neo4j._execute_query("MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'}) CREATE (a)-[:FRIEND]->(b)")
    neo4j._execute_query("MATCH (b:Person {name: 'Bob'}), (c:Person {name: 'Charlie'}) CREATE (b)-[:FRIEND]->(c)")

    # Execute a complex read query
    query = """
    MATCH (p:Person)-[:FRIEND]->(friend)
    RETURN p.name AS person, friend.name AS friend_name
    ORDER BY p.name, friend.name
    """
    result = neo4j._execute_query(query)

# Verify the query result
    assert len(result) == 2
    assert result[0]["person"] == "Alice"
    assert result[0]["friend_name"] == "Bob"
    assert result[1]["person"] == "Bob"
    assert result[1]["friend_name"] == "Charlie"
