# Let's Go - Social Network

A modern social network application built with Flask and Neo4j graph database.

## 🌟 Features

- **User Authentication**: Secure registration, login, and session management
- **User Profiles**: Customizable profiles with avatar and bio
- **Social Connections**: Follow/unfollow users to build your network
- **Posts**: Create, view, and delete posts with optional images
- **Interactions**: Like posts and add comments
- **Personalized Feed**: See posts from users you follow
- **Explore**: Discover new users to connect with
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🛠️ Technology Stack

- **Backend**: Flask 3.0 (Python web framework)
- **Database**: Neo4j 5.14 (Graph database)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Authentication**: Session-based with Werkzeug password hashing
- **Containerization**: Docker & Docker Compose

## 📁 Project Structure

```
Lets-Go/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Configuration settings (Dev/Prod/Test)
│   ├── database.py          # Neo4j connection handler
│   ├── models/              # Data models
│   │   ├── __init__.py
│   │   ├── user.py          # User model (auth, follow, profile)
│   │   └── post.py          # Post model (likes, comments, feed)
│   ├── routes/              # Application routes/blueprints
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication routes
│   │   ├── main.py          # Home page and feed
│   │   ├── users.py         # User-related routes
│   │   ├── posts.py         # Post-related routes
│   │   └── errors.py        # Error handlers (403, 404, 500)
│   ├── templates/           # Jinja2 HTML templates
│   │   ├── base.html        # Base template with navigation
│   │   ├── auth/            # Login, register
│   │   ├── main/            # Home, about
│   │   ├── users/           # Profile, followers, following, explore
│   │   ├── posts/           # Create post, view post
│   │   └── errors/          # Error pages
│   └── static/              # Static files
│       ├── css/
│       │   └── style.css    # Custom styles
│       ├── js/
│       │   └── main.js      # Interactive features
│       └── images/          # Image assets
├── tests/                   # Test suite
│   ├── __init__.py
│   └── test_app.py          # Basic tests
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
├── init_db.py              # Database initialization script
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Multi-container setup
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Neo4j 5.14+ (or use Docker)
- pip (Python package manager)

### Option 1: Using Docker (Recommended)

This is the easiest way to get started. Docker will handle both the Flask app and Neo4j database.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mehalyna/Lets-Go.git
   cd Lets-Go
   ```

2. **Copy the environment file**:
   ```bash
   copy .env.example .env
   ```
   
3. **Start the application**:
   ```bash
   docker-compose up -d
   ```

4. **Access the application**:
   - Web App: http://localhost:5000
   - Neo4j Browser: http://localhost:7474
   - Neo4j Credentials: `neo4j` / `password123`

5. **Stop the application**:
   ```bash
   docker-compose down
   ```

### Option 2: Local Installation

If you prefer to run the app locally without Docker:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mehalyna/Lets-Go.git
   cd Lets-Go
   ```

2. **Create and activate a virtual environment**:
   
   **Windows**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
   
   **Linux/Mac**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install and start Neo4j**:
   - Download [Neo4j Desktop](https://neo4j.com/download/) or use a cloud instance
   - Create a new database
   - Start Neo4j with Bolt protocol on port 7687
   - Note your credentials

5. **Configure environment variables**:
   ```bash
   copy .env.example .env
   ```
   
   Edit `.env` with your Neo4j credentials:
   ```env
   SECRET_KEY=your-secret-key-here
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your-password
   ```

6. **Initialize the database**:
   ```bash
   python init_db.py
   ```

7. **Run the application**:
   ```bash
   python run.py
   ```

8. **Access the application**:
   - Open your browser and navigate to http://localhost:5000

## 🗄️ Database Schema

### Neo4j Graph Model

#### Nodes

- **User**
  - Properties: `username`, `email`, `password_hash`, `bio`, `avatar_url`, `created_at`
  - Constraints: Unique username, unique email

- **Post**
  - Properties: `id`, `content`, `image_url`, `created_at`
  - Constraints: Unique id

- **Comment**
  - Properties: `id`, `content`, `created_at`

#### Relationships

- **(User)-[:FOLLOWS]->(User)** - User follows another user
  - Properties: `created_at`

- **(User)-[:POSTED]->(Post)** - User created a post
  
- **(User)-[:LIKES]->(Post)** - User liked a post
  - Properties: `created_at`

- **(User)-[:COMMENTED]->(Comment)** - User created a comment

- **(Comment)-[:ON_POST]->(Post)** - Comment belongs to a post

### Why Neo4j?

Neo4j is a graph database that excels at modeling and querying relationships, making it perfect for social networks where connections between users, posts, and interactions are central to the application.

## 🔗 API Routes

### Authentication Routes
- `GET/POST /auth/register` - User registration
- `GET/POST /auth/login` - User login
- `GET /auth/logout` - User logout

### Main Routes
- `GET /` - Home page / Personalized feed
- `GET /about` - About page

### User Routes
- `GET /users/<username>` - View user profile
- `GET/POST /users/<username>/edit` - Edit user profile (requires auth)
- `POST /users/<username>/follow` - Follow a user (requires auth)
- `POST /users/<username>/unfollow` - Unfollow a user (requires auth)
- `GET /users/<username>/followers` - List user's followers
- `GET /users/<username>/following` - List users being followed
- `GET /users/explore` - Explore and discover users

### Post Routes
- `GET/POST /posts/create` - Create a new post (requires auth)
- `GET /posts/<post_id>` - View post details with comments
- `POST /posts/<post_id>/delete` - Delete a post (requires auth & ownership)
- `POST /posts/<post_id>/like` - Like a post (requires auth)
- `POST /posts/<post_id>/unlike` - Unlike a post (requires auth)
- `POST /posts/<post_id>/comment` - Add a comment (requires auth)

## ⚙️ Configuration

The application supports multiple configuration environments:

- **Development**: Debug mode enabled, verbose logging
- **Production**: Debug disabled, secure cookies
- **Testing**: Separate test database

Edit `.env` file to configure:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password

# Session Configuration
SESSION_COOKIE_SECURE=False
```

## 🧪 Testing

Run the test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=app
```

## 🎨 Development

### Code Formatting

Format code with Black:
```bash
black .
```

### Linting

Check code quality with Flake8:
```bash
flake8
```

### Database Management

Initialize database constraints and indexes:
```bash
python init_db.py
```

### Project Dependencies

Key dependencies:
- **Flask 3.0.0** - Web framework
- **neo4j 5.14.1** - Neo4j Python driver
- **Werkzeug 3.0.1** - WSGI utilities and password hashing
- **python-dotenv 1.0.0** - Environment variable management
- **pytest 7.4.3** - Testing framework

## 📸 Screenshots

### Home Page
The personalized feed shows posts from users you follow.

### User Profile
View user information, followers, following, and all their posts.

### Create Post
Share your thoughts with optional image attachments.

## 🔐 Security Features

- Password hashing using Werkzeug's secure methods
- Session-based authentication with secure cookies
- CSRF protection (can be enhanced with Flask-WTF)
- SQL injection prevention through parameterized queries
- XSS protection through Jinja2 auto-escaping

## 🚧 Future Enhancements

- [ ] Direct messaging between users
- [ ] Real-time notifications system
- [ ] Search functionality (users, posts, hashtags)
- [ ] Hashtags support
- [ ] User mentions (@username)
- [ ] Image upload (currently supports URLs only)
- [ ] Email verification for new accounts
- [ ] Password reset functionality
- [ ] User blocking/muting
- [ ] Post sharing/reposting
- [ ] Advanced feed algorithm (relevance-based)
- [ ] Profile privacy settings
- [ ] Mobile app (React Native)
- [ ] REST API with JWT authentication
- [ ] Multi-language support

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code follows the project's coding standards:
- Use Black for code formatting
- Follow PEP 8 guidelines
- Add tests for new features
- Update documentation as needed

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👥 Authors

- **mehalyna** - Initial work - [GitHub](https://github.com/mehalyna)

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- Powered by [Neo4j](https://neo4j.com/)
- Styled with [Bootstrap](https://getbootstrap.com/)
- Icons from [Bootstrap Icons](https://icons.getbootstrap.com/)

## 📧 Contact

For questions, issues, or suggestions, please open an issue on GitHub.

---

**Happy Coding!** 🚀