from app import app, db, User
from werkzeug.security import generate_password_hash

def recreate_admin():
    with app.app_context():
        # Delete existing admin users
        existing_admins = User.query.filter_by(is_admin=True).all()
        for admin in existing_admins:
            db.session.delete(admin)
        
        # Create a fresh admin user
        new_admin = User(
            name='Administrator',
            username='superadmin',
            email='superadmin@opticals.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(new_admin)
        db.session.commit()
        
        print("Admin user recreated successfully!")
        print("Email: superadmin@opticals.com")
        print("Password: admin123")
        print("Login at: http://localhost:8081/login")

if __name__ == "__main__":
    recreate_admin()
