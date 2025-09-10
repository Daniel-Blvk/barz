# config.py - Updated version
import os

"""
Podcast Web Application Configuration
This file tracks all changes and configurations for the podcast homepage app.
"""

# Database Configuration - PostgreSQL
DATABASE_CONFIG = {
    'URI': 'postgresql://postgres:barznframes125@localhost/behindbars',
    'TRACK_MODIFICATIONS': False
}

# Upload Configuration
UPLOAD_CONFIG = {
    'UPLOAD_FOLDER': 'static/uploads',
    'MAX_FILE_SIZE': 16 * 1024 * 1024,  # 16MB
    'ALLOWED_EXTENSIONS': {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'm4a'}
}

# Application Configuration
APP_CONFIG = {
    'DEBUG': True,
    'HOST': 'localhost',
    'PORT': 5000,
    'SECRET_KEY': 'your-secret-key-here-change-in-production',
    'TEMPLATE': 'podcast-template'
}

# Podcast Information
PODCAST_CONFIG = {
    'title': 'Micro Podcast',
    'description': 'Discover powerful stories and insights through our thought-provoking podcast series.',
    'host': 'John Doe',
    'cover_image': 'https://i.postimg.cc/Y0nrN3zw/logo.png',
    'categories': ['Technology', 'Programming', 'Innovation'],
    'language': 'en-US'
}

# Social Links Configuration
SOCIAL_LINKS = {
    'twitter': '#',
    'facebook': '#',
    'instagram': '#',
    'youtube': '#',
    'spotify': '#',
    'apple_podcasts': '#',
    'soundcloud': '#'
}

# Contact Information
CONTACT_INFO = {
    'email': 'contact@example.com',
    'phone': '+1 (555) 123-4567',
    'phone2': '+1 (555) 987-6543',
    'address': '123 Podcast Street, City, State 12345'
}

# Hosts Information
HOSTS = [
    {
        'name': 'John Doe',
        'role': 'Main Host',
        'bio': 'Experienced podcast host with a passion for storytelling...',
        'image': '/static/images/host1.jpg',
        'social_media': {
            'twitter': '#',
            'instagram': '#',
            'linkedin': '#'
        }
    }
]

# Development Progress Tracking
DEVELOPMENT_PROGRESS = {
    'phase': 6,
    'completed_tasks': [
        'Project structure setup',
        'Basic Flask application',
        'Homepage route creation',
        'Configuration file setup',
        'HTML template extraction and organization',
        'Route creation for all navbar pages',
        'Base template implementation',
        'Individual page templates creation',
        'Database integration with SQLAlchemy',
        'User authentication system (register, login, logout)',
        'Admin authentication system with PIN',
        'Admin registration that becomes inactive after first registration',
        'Contact form message storage in database',
        'Admin dashboard with statistics and recent messages',
        'Flash messaging system for user feedback',
        'Enhanced database models for content management',
        'Blog post management system for admins',
        'Podcast episode management system',
        'Upcoming episodes management',
        'Events management system',
        'Homepage videos management',
        'File upload system with validation',
        'Content publishing/unpublishing system',
        'Contact messages management interface',
        'PostgreSQL database integration',
        'Database migration system with Flask-Migrate',
        'PostgreSQL database creation and configuration',
        'Missing template creation (admin_video_form, admin_episode_form, admin_upcoming_form, admin_event_form, admin_episodes, admin_events, admin_videos, admin_messages, blog_post)',
        'Complete content management system implementation',
        'Video management functionality',
        'Episode management functionality',
        'Upcoming episodes functionality',
        'Events management functionality',
        'Blog post display functionality'
    ],
    'next_tasks': [
        'Add edit functionality for all content types',
        'Add delete functionality for all content types',
        'Implement user profile management',
        'Add newsletter subscription system',
        'Implement comment system for blog',
        'Add podcast player with progress tracking',
        'Implement search functionality',
        'Add pagination for content lists',
        'Create RSS feed for podcast',
        'Implement email notifications',
        'Add social media sharing functionality',
        'Implement analytics tracking',
        'Add user roles and permissions',
        'Deploy to production server'
    ],
    'last_updated': '2024-01-30'
}