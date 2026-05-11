from neo4j import GraphDatabase
import logging

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        if self._driver:
            self._driver.close()
    
    def query(self, query, parameters=None, db=None):
        """Execute a Cypher query and return results"""
        assert self._driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self._driver.session(database=db) if db is not None else self._driver.session()
            response = list(session.run(query, parameters))
        except Exception as e:
            logging.error(f"Query failed: {e}")
            raise
        finally:
            if session is not None:
                session.close()
        return response
    
    def write_transaction(self, query, parameters=None, db=None):
        """Execute a write transaction"""
        assert self._driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self._driver.session(database=db) if db is not None else self._driver.session()
            response = session.write_transaction(
                lambda tx: list(tx.run(query, parameters))
            )
        except Exception as e:
            logging.error(f"Write transaction failed: {e}")
            raise
        finally:
            if session is not None:
                session.close()
        return response

def init_db():
    """Initialize database with constraints and indexes"""
    from app import db
    
    constraints = [
        "CREATE CONSTRAINT user_username IF NOT EXISTS FOR (u:User) REQUIRE u.username IS UNIQUE",
        "CREATE CONSTRAINT user_email IF NOT EXISTS FOR (u:User) REQUIRE u.email IS UNIQUE",
        "CREATE CONSTRAINT post_id IF NOT EXISTS FOR (p:Post) REQUIRE p.id IS UNIQUE",
    ]
    
    indexes = [
        "CREATE INDEX user_created IF NOT EXISTS FOR (u:User) ON (u.created_at)",
        "CREATE INDEX post_created IF NOT EXISTS FOR (p:Post) ON (p.created_at)",
    ]
    
    for constraint in constraints:
        try:
            db.query(constraint)
            print(f"Applied: {constraint}")
        except Exception as e:
            print(f"Constraint may already exist: {e}")
    
    for index in indexes:
        try:
            db.query(index)
            print(f"Applied: {index}")
        except Exception as e:
            print(f"Index may already exist: {e}")
