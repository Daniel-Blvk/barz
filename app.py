# app.py updates for PostgreSQL and Flask-Migrate
from flask import Flask, render_template, request, redirect, url_for, flash, session
import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)

# Load configuration from environment variables
app.config['DEBUG'] = os.environ.get('FLASK_ENV') == 'development' # Will be False in production
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# File upload configuration
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'static/uploads')
# Use a default fallback if variable is missing, then convert to int
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', '50777216')) 
# Get comma-separated string, then convert to a set of extensions
app.config['ALLOWED_EXTENSIONS'] = set(os.environ.get('ALLOWED_EXTENSIONS', 'png,jpg,jpeg,gif,mp3,wav,m4a').split(',')) 


# migrate = Migrate(app, db)  # Initialize Flask-Migrate


# Helper functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.context_processor
def utility_processor():
    return dict(datetime=datetime)

# Context processor to make global variables available to all templates
@app.context_processor
def inject_global_vars():
    # Get active videos for homepage
    homepage_videos = HomepageVideo.query.filter_by(is_active=True).all()
    
    return {
        'podcast': config.PODCAST_CONFIG,
        'social_links': config.SOCIAL_LINKS,
        'contact_info': config.CONTACT_INFO,
        'admin_registered': Admin.query.first() is not None,
        'homepage_videos': homepage_videos
    }


db = SQLAlchemy(app)
migrate = Migrate(app, db)

 # Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    messages = db.relationship('ContactMessage', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'





class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pin = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())  
    def __repr__(self):
        return f'<Admin {self.username}>'


class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    is_read = db.Column(db.Boolean, default=False)  
    def __repr__(self):
        return f'<ContactMessage {self.subject}>'


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    excerpt = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publish_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())  
    def __repr__(self):
        return f'<BlogPost {self.title}>'


class PodcastEpisode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(20), nullable=False)
    episode_number = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    audio_url = db.Column(db.String(200), nullable=False)
    publish_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())  
    def __repr__(self):
        return f'<PodcastEpisode {self.title}>'

class UpcomingEpisode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    scheduled_date = db.Column(db.DateTime, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())  
    def __repr__(self):
        return f'<UpcomingEpisode {self.title}>'

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())  
    def __repr__(self):
        return f'<Event {self.title}>'

class HomepageVideo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    video_url = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())  
    def __repr__(self):
        return f'<HomepageVideo {self.title}>'



# Helper functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
# Context processor to make global variables available to all templates
@app.context_processor
def inject_global_vars():
    # Get active videos for homepage
    homepage_videos = HomepageVideo.query.filter_by(is_active=True).all()  
    return {
        'podcast': config.PODCAST_CONFIG,
        'social_links': config.SOCIAL_LINKS,
        'contact_info': config.CONTACT_INFO,
        'admin_registered': Admin.query.first() is not None,
        'homepage_videos': homepage_videos
    }
    
# Routes for main pages
@app.route('/')
def homepage():
    """Render the podcast homepage"""
    # Get published episodes
    episodes = PodcastEpisode.query.filter_by(is_published=True).order_by(PodcastEpisode.publish_date.desc()).all()  
    # Get upcoming episodes
    upcoming_episodes = UpcomingEpisode.query.order_by(UpcomingEpisode.scheduled_date.asc()).all()  
    # Get blog posts
    blog_posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.publish_date.desc()).limit(3).all()  
    # Get events
    events = Event.query.order_by(Event.event_date.desc()).limit(3).all()  
    return render_template('index.html', 
                         episodes=episodes, 
                         upcoming_episodes=upcoming_episodes,
                         blog_posts=blog_posts,
                         events=events
    )
@app.route('/host')
def host():
    """Render the host page"""
    return render_template('host.html', hosts=config.HOSTS)
@app.route('/blog')
def blog():
    """Render the blog page"""
    # Get all published blog posts
    blog_posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.publish_date.desc()).all()
    return render_template('blog.html', blog_posts=blog_posts)
@app.route('/blog/<int:post_id>')
def blog_post(post_id):
    """Render individual blog post"""
    post = BlogPost.query.get_or_404(post_id)
    return render_template('blog_post.html', post=post)
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Render the contact page and handle form submissions"""
    if request.method == 'POST':
        # Check if user is logged in
        user_id = session.get('user_id') if 'user_id' in session else None      
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')      
        # Create new message
        new_message = ContactMessage(
            user_id=user_id,
            name=name,
            email=email,
            subject=subject,
            message=message
        )      
        try:
            db.session.add(new_message)
            db.session.commit()
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('There was an error sending your message. Please try again.', 'error')      
        return redirect(url_for('contact'))  
    return render_template('contact.html')
@app.route('/episode/<int:episode_id>')
def episode_detail(episode_id):
    """Route for individual episode pages"""
    episode = PodcastEpisode.query.get_or_404(episode_id)
    return render_template('episode.html', episode=episode)
@app.route('/events')
def events():
    """Render events page"""
    events = Event.query.order_by(Event.event_date.desc()).all()
    return render_template('events.html', events=events)
# User authentication routes (unchanged from previous implementation)
# ... [Keep the existing user authentication routes] ..
# Admin authentication routes (unchanged from previous implementation)
# ... [Keep the existing admin authentication routes] ..

# User authentication routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Basic validation
        if not all([username, email, password, confirm_password]):
            flash('Please fill in all fields', 'error')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('There was an error creating your account. Please try again.', 'error')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('homepage'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('homepage'))

# Admin authentication routes
@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    """Admin registration (only works once)"""
    # Check if admin already exists
    if Admin.query.first():
        flash('Admin registration is closed. Only one admin account can exist.', 'error')
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        pin = request.form.get('pin')
        confirm_pin = request.form.get('confirm_pin')
        
        if not all([username, pin, confirm_pin]):
            flash('Please fill in all fields', 'error')
            return redirect(url_for('admin_register'))
        
        if pin != confirm_pin:
            flash('PINs do not match', 'error')
            return redirect(url_for('admin_register'))
        
        # Create admin
        hashed_pin = generate_password_hash(pin)
        new_admin = Admin(
            username=username,
            pin=hashed_pin
        )
        
        try:
            db.session.add(new_admin)
            db.session.commit()
            flash('Admin registration successful! Please log in.', 'success')
            return redirect(url_for('admin_login'))
        except Exception as e:
            db.session.rollback()
            flash('There was an error creating the admin account.', 'error')
    
    return render_template('admin_register.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login"""
    if request.method == 'POST':
        username = request.form.get('username')
        pin = request.form.get('pin')
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and check_password_hash(admin.pin, pin):
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or PIN', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_id', None)
    session.pop('admin_username', None)
    flash('Admin logout successful', 'success')
    return redirect(url_for('homepage'))

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))  
    # Get statistics
    user_count = User.query.count()
    message_count = ContactMessage.query.count()
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    blog_count = BlogPost.query.count()
    episode_count = PodcastEpisode.query.count()  
    return render_template('admin_dashboard.html', 
                          user_count=user_count, 
                          message_count=message_count,
                          blog_count=blog_count,
                          episode_count=episode_count,
                          recent_messages=recent_messages
    )
# Admin content management routes
@app.route('/admin/blog')
def admin_blog():
    """Admin blog management"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))  
    blog_posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('admin_blog.html', blog_posts=blog_posts)
@app.route('/admin/blog/new', methods=['GET', 'POST'])
def admin_new_blog():
    """Create new blog post"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))  
    if request.method == 'POST':
        title = request.form.get('title')
        excerpt = request.form.get('excerpt')
        content = request.form.get('content')
        author = request.form.get('author')
        publish_date = request.form.get('publish_date')
        is_published = 'is_published' in request.form      
        # Handle image upload
        if 'image' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)      
        file = request.files['image']      
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)      
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'blog', filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file.save(file_path)          
            # Create new blog post
            new_blog = BlogPost(
                title=title,
                excerpt=excerpt,
                content=content,
                author=author,
                image=f"/static/uploads/blog/{filename}",
                publish_date=datetime.strptime(publish_date, '%Y-%m-%d') if publish_date else datetime.utcnow(),
                is_published=is_published
            )          
            try:
                db.session.add(new_blog)
                db.session.commit()
                flash('Blog post created successfully!', 'success')
                return redirect(url_for('admin_blog'))
            except Exception as e:
                db.session.rollback()
                flash('There was an error creating the blog post. Please try again.', 'error')      
        else:
            flash('Invalid file type. Allowed types: ' + ', '.join(app.config['ALLOWED_EXTENSIONS']), 'error')  
    return render_template('admin_blog_form.html')
@app.route('/admin/blog/edit/<int:post_id>', methods=['GET', 'POST'])
def admin_edit_blog(post_id):
    """Edit blog post"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))  
    post = BlogPost.query.get_or_404(post_id)  
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.excerpt = request.form.get('excerpt')
        post.content = request.form.get('content')
        post.author = request.form.get('author')
        publish_date = request.form.get('publish_date')
        post.is_published = 'is_published' in request.form      
        if publish_date:
            post.publish_date = datetime.strptime(publish_date, '%Y-%m-%d')      
        # Handle image upload if a new file is provided
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'blog', filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                file.save(file_path)
                post.image = f"/static/uploads/blog/{filename}"      
        try:
            db.session.commit()
            flash('Blog post updated successfully!', 'success')
            return redirect(url_for('admin_blog'))
        except Exception as e:
            db.session.rollback()
            flash('There was an error updating the blog post. Please try again.', 'error')  
    return render_template('admin_blog_form.html', post=post)
@app.route('/admin/blog/delete/<int:post_id>')
def admin_delete_blog(post_id):
    """Delete blog post"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))  
    post = BlogPost.query.get_or_404(post_id)  
    try:
        db.session.delete(post)
        db.session.commit()
        flash('Blog post deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('There was an error deleting the blog post. Please try again.', 'error')  
    return redirect(url_for('admin_blog'))
@app.route('/admin/episodes')
def admin_episodes():
    """Admin episodes management"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))  
    episodes = PodcastEpisode.query.order_by(PodcastEpisode.episode_number.desc()).all()
    upcoming_episodes = UpcomingEpisode.query.order_by(UpcomingEpisode.scheduled_date.asc()).all()  
    return render_template('admin_episodes.html', 
                          episodes=episodes, 
                          upcoming_episodes=upcoming_episodes
    )
@app.route('/admin/episodes/new', methods=['GET', 'POST'])
def admin_new_episode():
    """Create new podcast episode"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))  
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        duration = request.form.get('duration')
        episode_number = request.form.get('episode_number')
        publish_date = request.form.get('publish_date')
        is_published = 'is_published' in request.form      
        # Handle image upload
        image_file = request.files['image']
        audio_file = request.files['audio']      
        image_filename = None
        audio_filename = None      
        if image_file and image_file.filename != '' and allowed_file(image_file.filename):
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'episodes', 'images', image_filename)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image_file.save(image_path)      
        if audio_file and audio_file.filename != '' and allowed_file(audio_file.filename):
            audio_filename = secure_filename(audio_file.filename)
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'episodes', 'audio', audio_filename)
            os.makedirs(os.path.dirname(audio_path), exist_ok=True)
            audio_file.save(audio_path)      
        if not image_filename or not audio_filename:
            flash('Both image and audio files are required', 'error')
            return redirect(request.url)      
        # Create new episode
        new_episode = PodcastEpisode(
            title=title,
            description=description,
            duration=duration,
            episode_number=episode_number,
            image_url=f"/static/uploads/episodes/images/{image_filename}",
            audio_url=f"/static/uploads/episodes/audio/{audio_filename}",
            publish_date=datetime.strptime(publish_date, '%Y-%m-%d') if publish_date else datetime.utcnow(),
            is_published=is_published
        )      
        try:
            db.session.add(new_episode)
            db.session.commit()
            flash('Episode created successfully!', 'success')
            return redirect(url_for('admin_episodes'))
        except Exception as e:
            db.session.rollback()
            flash('There was an error creating the episode. Please try again.', 'error')  
    return render_template('admin_episode_form.html')
@app.route('/admin/upcoming/new', methods=['GET', 'POST'])
def admin_new_upcoming():
    """Create new upcoming episode"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))  
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        scheduled_date = request.form.get('scheduled_date')      
        # Handle image upload
        image_file = request.files['image']      
        if image_file and image_file.filename != '' and allowed_file(image_file.filename):
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'upcoming', image_filename)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image_file.save(image_path)          
            # Create new upcoming episode
            new_upcoming = UpcomingEpisode(
                title=title,
                description=description,
                scheduled_date=datetime.strptime(scheduled_date, '%Y-%m-%d'),
                image_url=f"/static/uploads/upcoming/{image_filename}"
            )          
            try:
                db.session.add(new_upcoming)
                db.session.commit()
                flash('Upcoming episode created successfully!', 'success')
                return redirect(url_for('admin_episodes'))
            except Exception as e:
                db.session.rollback()
                flash('There was an error creating the upcoming episode. Please try again.', 'error')
        else:
            flash('Image file is required', 'error')  
    return render_template('admin_upcoming_form.html')
@app.route('/admin/events')
def admin_events():
    """Admin events management"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))  
    events = Event.query.order_by(Event.event_date.desc()).all()
    return render_template('admin_events.html', events=events)
@app.route('/admin/events/new', methods=['GET', 'POST'])
def admin_new_event():
    """Create new event"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))  
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        event_date = request.form.get('event_date')
        location = request.form.get('location')      
        # Handle image upload
        image_file = request.files['image']      
        if image_file and image_file.filename != '' and allowed_file(image_file.filename):
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'events', image_filename)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image_file.save(image_path)          
            # Create new event
            new_event = Event(
                title=title,
                description=description,
                event_date=datetime.strptime(event_date, '%Y-%m-%d'),
                location=location,
                image_url=f"/static/uploads/events/{image_filename}"
            )          
            try:
                db.session.add(new_event)
                db.session.commit()
                flash('Event created successfully!', 'success')
                return redirect(url_for('admin_events'))
            except Exception as e:
                db.session.rollback()
                flash('There was an error creating the event. Please try again.', 'error')
        else:
            flash('Image file is required', 'error')  
    return render_template('admin_event_form.html')
@app.route('/admin/videos')
def admin_videos():
    """Admin videos management"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))  
    videos = HomepageVideo.query.order_by(HomepageVideo.created_at.desc()).all()
    return render_template('admin_videos.html', videos=videos)
@app.route('/admin/videos/new', methods=['GET', 'POST'])
def admin_new_video():
    """Create new homepage video"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))  
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        video_url = request.form.get('video_url')
        is_active = 'is_active' in request.form      
        # Create new video
        new_video = HomepageVideo(
            title=title,
            description=description,
            video_url=video_url,
            is_active=is_active
        )      
        try:
            db.session.add(new_video)
            db.session.commit()
            flash('Video added successfully!', 'success')
            return redirect(url_for('admin_videos'))
        except Exception as e:
            db.session.rollback()
            flash('There was an error adding the video. Please try again.', 'error')  
    return render_template('admin_video_form.html')
@app.route('/admin/messages')
def admin_messages():
    """Admin contact messages management"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))  
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin_messages.html', messages=messages)
@app.route('/admin/messages/<int:message_id>/toggle-read')
def admin_toggle_message_read(message_id):
    """Toggle message read status"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))  
    message = ContactMessage.query.get_or_404(message_id)
    message.is_read = not message.is_read  
    try:
        db.session.commit()
        flash('Message status updated!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('There was an error updating the message status.', 'error')  
    return redirect(url_for('admin_messages'))
@app.route('/admin/messages/<int:message_id>/delete')
def admin_delete_message(message_id):
    """Delete contact message"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))  
    message = ContactMessage.query.get_or_404(message_id)  
    try:
        db.session.delete(message)
        db.session.commit()
        flash('Message deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('There was an error deleting the message.', 'error')  
    return redirect(url_for('admin_messages'))

# Add these routes to your app.py

@app.route('/admin/videos/edit/<int:video_id>', methods=['GET', 'POST'])
def admin_edit_video(video_id):
    """Edit homepage video"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))
    
    video = HomepageVideo.query.get_or_404(video_id)
    
    if request.method == 'POST':
        video.title = request.form.get('title')
        video.description = request.form.get('description')
        video.video_url = request.form.get('video_url')
        video.is_active = 'is_active' in request.form
        
        try:
            db.session.commit()
            flash('Video updated successfully!', 'success')
            return redirect(url_for('admin_videos'))
        except Exception as e:
            db.session.rollback()
            flash('There was an error updating the video. Please try again.', 'error')
    
    return render_template('admin_video_form.html', video=video)

@app.route('/admin/videos/delete/<int:video_id>')
def admin_delete_video(video_id):
    """Delete homepage video"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))
    
    video = HomepageVideo.query.get_or_404(video_id)
    
    try:
        db.session.delete(video)
        db.session.commit()
        flash('Video deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('There was an error deleting the video. Please try again.', 'error')
    
    return redirect(url_for('admin_videos'))

@app.route('/admin/episodes/edit/<int:episode_id>', methods=['GET', 'POST'])
def admin_edit_episode(episode_id):
    """Edit podcast episode"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))
    
    episode = PodcastEpisode.query.get_or_404(episode_id)
    
    if request.method == 'POST':
        episode.title = request.form.get('title')
        episode.description = request.form.get('description')
        episode.duration = request.form.get('duration')
        episode.episode_number = request.form.get('episode_number')
        publish_date = request.form.get('publish_date')
        episode.is_published = 'is_published' in request.form
        
        if publish_date:
            episode.publish_date = datetime.strptime(publish_date, '%Y-%m-%d')
        
        # Handle image upload if a new file is provided
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'episodes', 'images', filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                file.save(file_path)
                episode.image_url = f"/static/uploads/episodes/images/{filename}"
        
        # Handle audio upload if a new file is provided
        if 'audio' in request.files:
            file = request.files['audio']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'episodes', 'audio', filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                file.save(file_path)
                episode.audio_url = f"/static/uploads/episodes/audio/{filename}"
        
        try:
            db.session.commit()
            flash('Episode updated successfully!', 'success')
            return redirect(url_for('admin_episodes'))
        except Exception as e:
            db.session.rollback()
            flash('There was an error updating the episode. Please try again.', 'error')
    
    return render_template('admin_episode_form.html', episode=episode)

@app.route('/admin/episodes/delete/<int:episode_id>')
def admin_delete_episode(episode_id):
    """Delete podcast episode"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))
    
    episode = PodcastEpisode.query.get_or_404(episode_id)
    
    try:
        db.session.delete(episode)
        db.session.commit()
        flash('Episode deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('There was an error deleting the episode. Please try again.', 'error')
    
    return redirect(url_for('admin_episodes'))

@app.route('/admin/upcoming/edit/<int:upcoming_id>', methods=['GET', 'POST'])
def admin_edit_upcoming(upcoming_id):
    """Edit upcoming episode"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))
    
    upcoming = UpcomingEpisode.query.get_or_404(upcoming_id)
    
    if request.method == 'POST':
        upcoming.title = request.form.get('title')
        upcoming.description = request.form.get('description')
        scheduled_date = request.form.get('scheduled_date')
        
        if scheduled_date:
            upcoming.scheduled_date = datetime.strptime(scheduled_date, '%Y-%m-%d')
        
        # Handle image upload if a new file is provided
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'upcoming', filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                file.save(file_path)
                upcoming.image_url = f"/static/uploads/upcoming/{filename}"
        
        try:
            db.session.commit()
            flash('Upcoming episode updated successfully!', 'success')
            return redirect(url_for('admin_episodes'))
        except Exception as e:
            db.session.rollback()
            flash('There was an error updating the upcoming episode. Please try again.', 'error')
    
    return render_template('admin_upcoming_form.html', upcoming=upcoming)

@app.route('/admin/upcoming/delete/<int:upcoming_id>')
def admin_delete_upcoming(upcoming_id):
    """Delete upcoming episode"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))
    
    upcoming = UpcomingEpisode.query.get_or_404(upcoming_id)
    
    try:
        db.session.delete(upcoming)
        db.session.commit()
        flash('Upcoming episode deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('There was an error deleting the upcoming episode. Please try again.', 'error')
    
    return redirect(url_for('admin_episodes'))

@app.route('/admin/events/edit/<int:event_id>', methods=['GET', 'POST'])
def admin_edit_event(event_id):
    """Edit event"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))
    
    event = Event.query.get_or_404(event_id)
    
    if request.method == 'POST':
        event.title = request.form.get('title')
        event.description = request.form.get('description')
        event_date = request.form.get('event_date')
        event.location = request.form.get('location')
        
        if event_date:
            event.event_date = datetime.strptime(event_date, '%Y-%m-%d')
        
        # Handle image upload if a new file is provided
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'events', filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                file.save(file_path)
                event.image_url = f"/static/uploads/events/{filename}"
        
        try:
            db.session.commit()
            flash('Event updated successfully!', 'success')
            return redirect(url_for('admin_events'))
        except Exception as e:
            db.session.rollback()
            flash('There was an error updating the event. Please try again.', 'error')
    
    return render_template('admin_event_form.html', event=event)

@app.route('/admin/events/delete/<int:event_id>')
def admin_delete_event(event_id):
    """Delete event"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))
    
    event = Event.query.get_or_404(event_id)
    
    try:
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('There was an error deleting the event. Please try again.', 'error')
    
    return redirect(url_for('admin_events'))

@app.route('/admin/messages/view/<int:message_id>')
def admin_view_message(message_id):
    """View contact message"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))
    
    message = ContactMessage.query.get_or_404(message_id)
    message.is_read = True
    db.session.commit()
    
    return render_template('admin_message_view.html', message=message)

@app.route('/admin/messages/toggle-read/<int:message_id>')
def admin_toggle_message_read_alt(message_id):  # Changed function name
    """Toggle message read status"""
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))
    
    message = ContactMessage.query.get_or_404(message_id)
    message.is_read = not message.is_read
    db.session.commit()
    
    flash(f'Message marked as {"read" if message.is_read else "unread"}', 'success')
    return redirect(url_for('admin_messages'))






if __name__ == '__main__':
    # Create upload directories if they don't exist
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'blog'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'episodes', 'images'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'episodes', 'audio'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'upcoming'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'events'), exist_ok=True)
    
    app.run(
        host=config.APP_CONFIG['HOST'],
        port=config.APP_CONFIG['PORT'],
        debug=config.APP_CONFIG['DEBUG']
    )