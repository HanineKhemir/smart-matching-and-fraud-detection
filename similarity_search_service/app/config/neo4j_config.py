from neo4j import GraphDatabase
from app.config.config import NEO4J_USER, NEO4J_PASSWORD, NEO4J_URI

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
AUTH = (NEO4J_USER, NEO4J_PASSWORD)

with GraphDatabase.driver(NEO4J_URI, auth=AUTH) as driver:
    driver.verify_connectivity()