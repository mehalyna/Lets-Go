from datetime import datetime
from app import db
import uuid

class Post:
    """Post model for Neo4j"""
    
    @staticmethod
    def create(username, content, image_url=None):
        """Create a new post"""
        post_id = str(uuid.uuid4())
        query = """
        MATCH (u:User {username: $username})
        CREATE (p:Post {
            id: $post_id,
            content: $content,
            image_url: $image_url,
            created_at: datetime()
        })
        CREATE (u)-[:POSTED]->(p)
        RETURN p, u
        """
        result = db.query(query, {
            'username': username,
            'post_id': post_id,
            'content': content,
            'image_url': image_url
        })
        return result[0] if result else None
    
    @staticmethod
    def find_by_id(post_id):
        """Find post by ID"""
        query = """
        MATCH (u:User)-[:POSTED]->(p:Post {id: $post_id})
        RETURN p, u
        """
        result = db.query(query, {'post_id': post_id})
        return result[0] if result else None
    
    @staticmethod
    def get_all(skip=0, limit=10):
        """Get all posts with pagination"""
        query = """
        MATCH (u:User)-[:POSTED]->(p:Post)
        RETURN p, u
        ORDER BY p.created_at DESC
        SKIP $skip
        LIMIT $limit
        """
        result = db.query(query, {'skip': skip, 'limit': limit})
        return result
    
    @staticmethod
    def get_by_user(username, skip=0, limit=10):
        """Get posts by a specific user"""
        query = """
        MATCH (u:User {username: $username})-[:POSTED]->(p:Post)
        RETURN p, u
        ORDER BY p.created_at DESC
        SKIP $skip
        LIMIT $limit
        """
        result = db.query(query, {'username': username, 'skip': skip, 'limit': limit})
        return result
    
    @staticmethod
    def get_feed(username, skip=0, limit=10):
        """Get posts from users that the given user follows"""
        query = """
        MATCH (u:User {username: $username})-[:FOLLOWS]->(followed:User)-[:POSTED]->(p:Post)
        RETURN p, followed as u
        ORDER BY p.created_at DESC
        SKIP $skip
        LIMIT $limit
        """
        result = db.query(query, {'username': username, 'skip': skip, 'limit': limit})
        return result
    
    @staticmethod
    def delete(post_id, username):
        """Delete a post (only if user owns it)"""
        query = """
        MATCH (u:User {username: $username})-[:POSTED]->(p:Post {id: $post_id})
        DETACH DELETE p
        """
        db.query(query, {'post_id': post_id, 'username': username})
    
    @staticmethod
    def like(post_id, username):
        """Like a post"""
        query = """
        MATCH (u:User {username: $username})
        MATCH (p:Post {id: $post_id})
        MERGE (u)-[r:LIKES {created_at: datetime()}]->(p)
        RETURN r
        """
        result = db.query(query, {'post_id': post_id, 'username': username})
        return result[0]['r'] if result else None
    
    @staticmethod
    def unlike(post_id, username):
        """Unlike a post"""
        query = """
        MATCH (u:User {username: $username})-[r:LIKES]->(p:Post {id: $post_id})
        DELETE r
        """
        db.query(query, {'post_id': post_id, 'username': username})
    
    @staticmethod
    def is_liked_by(post_id, username):
        """Check if user has liked the post"""
        query = """
        MATCH (u:User {username: $username})-[:LIKES]->(p:Post {id: $post_id})
        RETURN count(*) > 0 as is_liked
        """
        result = db.query(query, {'post_id': post_id, 'username': username})
        return result[0]['is_liked'] if result else False
    
    @staticmethod
    def get_like_count(post_id):
        """Get number of likes for a post"""
        query = """
        MATCH (u:User)-[:LIKES]->(p:Post {id: $post_id})
        RETURN count(u) as count
        """
        result = db.query(query, {'post_id': post_id})
        return result[0]['count'] if result else 0
    
    @staticmethod
    def add_comment(post_id, username, content):
        """Add a comment to a post"""
        comment_id = str(uuid.uuid4())
        query = """
        MATCH (u:User {username: $username})
        MATCH (p:Post {id: $post_id})
        CREATE (c:Comment {
            id: $comment_id,
            content: $content,
            created_at: datetime()
        })
        CREATE (u)-[:COMMENTED]->(c)
        CREATE (c)-[:ON_POST]->(p)
        RETURN c, u
        """
        result = db.query(query, {
            'post_id': post_id,
            'username': username,
            'comment_id': comment_id,
            'content': content
        })
        return result[0] if result else None
    
    @staticmethod
    def get_comments(post_id, skip=0, limit=20):
        """Get comments for a post"""
        query = """
        MATCH (u:User)-[:COMMENTED]->(c:Comment)-[:ON_POST]->(p:Post {id: $post_id})
        RETURN c, u
        ORDER BY c.created_at ASC
        SKIP $skip
        LIMIT $limit
        """
        result = db.query(query, {'post_id': post_id, 'skip': skip, 'limit': limit})
        return result
