from flask import Flask
from app.config import Config
from app.database import Neo4jConnection

db = None

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize Neo4j connection
    global db
    db = Neo4jConnection(
        uri=app.config['NEO4J_URI'],
        user=app.config['NEO4J_USER'],
        password=app.config['NEO4J_PASSWORD']
    )
    
    # Register blueprints
    from app.routes import auth, main, users, posts
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(posts.bp)
    
    # Register error handlers
    from app.routes import errors
    app.register_blueprint(errors.bp)
    
    return app
