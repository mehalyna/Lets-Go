from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
import uuid

class User:
    """User model for Neo4j"""
    
    @staticmethod
    def create(username, email, password, bio=None, avatar_url=None):
        """Create a new user"""
        password_hash = generate_password_hash(password)
        query = """
        CREATE (u:User {
            username: $username,
            email: $email,
            password_hash: $password_hash,
            bio: $bio,
            avatar_url: $avatar_url,
            created_at: datetime()
        })
        RETURN u
        """
        result = db.query(query, {
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'bio': bio,
            'avatar_url': avatar_url
        })
        return result[0]['u'] if result else None
    
    @staticmethod
    def find_by_username(username):
        """Find user by username"""
        query = "MATCH (u:User {username: $username}) RETURN u"
        result = db.query(query, {'username': username})
        return result[0]['u'] if result else None
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        query = "MATCH (u:User {email: $email}) RETURN u"
        result = db.query(query, {'email': email})
        return result[0]['u'] if result else None
    
    @staticmethod
    def verify_password(username, password):
        """Verify user password"""
        user = User.find_by_username(username)
        if user and check_password_hash(user['password_hash'], password):
            return user
        return None
    
    @staticmethod
    def get_all(skip=0, limit=20):
        """Get all users with pagination"""
        query = """
        MATCH (u:User)
        RETURN u
        ORDER BY u.created_at DESC
        SKIP $skip
        LIMIT $limit
        """
        result = db.query(query, {'skip': skip, 'limit': limit})
        return [record['u'] for record in result]
    
    @staticmethod
    def update_profile(username, bio=None, avatar_url=None):
        """Update user profile"""
        query = """
        MATCH (u:User {username: $username})
        SET u.bio = $bio,
            u.avatar_url = $avatar_url
        RETURN u
        """
        result = db.query(query, {
            'username': username,
            'bio': bio,
            'avatar_url': avatar_url
        })
        return result[0]['u'] if result else None
    
    @staticmethod
    def follow(follower_username, followed_username):
        """Create a follow relationship"""
        query = """
        MATCH (follower:User {username: $follower_username})
        MATCH (followed:User {username: $followed_username})
        MERGE (follower)-[r:FOLLOWS {created_at: datetime()}]->(followed)
        RETURN r
        """
        result = db.query(query, {
            'follower_username': follower_username,
            'followed_username': followed_username
        })
        return result[0]['r'] if result else None
    
    @staticmethod
    def unfollow(follower_username, followed_username):
        """Remove a follow relationship"""
        query = """
        MATCH (follower:User {username: $follower_username})-[r:FOLLOWS]->(followed:User {username: $followed_username})
        DELETE r
        """
        db.query(query, {
            'follower_username': follower_username,
            'followed_username': followed_username
        })
    
    @staticmethod
    def get_followers(username, skip=0, limit=20):
        """Get users who follow this user"""
        query = """
        MATCH (follower:User)-[:FOLLOWS]->(u:User {username: $username})
        RETURN follower
        ORDER BY follower.username
        SKIP $skip
        LIMIT $limit
        """
        result = db.query(query, {'username': username, 'skip': skip, 'limit': limit})
        return [record['follower'] for record in result]
    
    @staticmethod
    def get_following(username, skip=0, limit=20):
        """Get users this user follows"""
        query = """
        MATCH (u:User {username: $username})-[:FOLLOWS]->(followed:User)
        RETURN followed
        ORDER BY followed.username
        SKIP $skip
        LIMIT $limit
        """
        result = db.query(query, {'username': username, 'skip': skip, 'limit': limit})
        return [record['followed'] for record in result]
    
    @staticmethod
    def is_following(follower_username, followed_username):
        """Check if follower follows followed"""
        query = """
        MATCH (follower:User {username: $follower_username})-[:FOLLOWS]->(followed:User {username: $followed_username})
        RETURN count(*) > 0 as is_following
        """
        result = db.query(query, {
            'follower_username': follower_username,
            'followed_username': followed_username
        })
        return result[0]['is_following'] if result else False
    
    @staticmethod
    def get_follower_count(username):
        """Get count of followers"""
        query = """
        MATCH (follower:User)-[:FOLLOWS]->(u:User {username: $username})
        RETURN count(follower) as count
        """
        result = db.query(query, {'username': username})
        return result[0]['count'] if result else 0
    
    @staticmethod
    def get_following_count(username):
        """Get count of users being followed"""
        query = """
        MATCH (u:User {username: $username})-[:FOLLOWS]->(followed:User)
        RETURN count(followed) as count
        """
        result = db.query(query, {'username': username})
        return result[0]['count'] if result else 0
