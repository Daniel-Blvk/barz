# test_db.py
from app import app, db
from app import User, Admin  # Import your models

with app.app_context():
    try:
        # Test connection
        connection = db.engine.connect()
        print("✅ Database connection successful!")
        
        # Check if tables exist
        inspector = db.inspect(db.engine)
        table_names = inspector.get_table_names()
        print(f"✅ Tables in database: {table_names}")
        
        # Test query
        user_count = User.query.count()
        admin_count = Admin.query.count()
        print(f"✅ Query test successful! Users: {user_count}, Admins: {admin_count}")
        
        connection.close()
        
    except Exception as e:
        print(f"❌ Database error: {str(e)}")