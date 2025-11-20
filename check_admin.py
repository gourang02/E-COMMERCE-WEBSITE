from app import app, db, User
from werkzeug.security import generate_password_hash

def check_admin():
    with app.app_context():
        # Check if admin user exists
        admin = User.query.filter_by(email='admin@example.com').first()
        
        if not admin:
            # Create admin user
            admin = User(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created!")
            print("Email: admin@example.com")
            print("Password: admin123")
        else:
            print("Admin user already exists!")
            print(f"Email: {admin.email}")

if __name__ == "__main__":
    check_admin()
