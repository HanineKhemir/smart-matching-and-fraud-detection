from app.config.neo4j_config import driver

def create_similarity_relationship(post_id_1: str, post_id_2: str):
    with driver.session() as session:
        session.run(
            """
            MERGE (a:Post {id: $id1})
            MERGE (b:Post {id: $id2})
            MERGE (a)-[r:SIMILAR_TO]->(b)
            MERGE (b)-[:SIMILAR_TO]->(a)
            """,
            id1=post_id_1,
            id2=post_id_2,
        )
    return True

def get_similar_posts(post_id: str):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (a:Post {id: $id})-[r:SIMILAR_TO]->(b:Post)
            RETURN b.id AS similar_post_id
            """,
            id=post_id

        )
        return [record["similar_post_id"] for record in result]

def delete_post(post_id: str):
    with driver.session() as session:
        session.run(
            """
            MATCH (p:Post {id: $id})
            DETACH DELETE p
            """,
            id=post_id
        )
