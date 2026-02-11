from app import app, db, User
from werkzeug.security import generate_password_hash

def create_test_admin():
    with app.app_context():
        # Create a new test admin user
        test_admin = User(
            name='Test Admin',
            username='testadmin',
            email='test@admin.com',
            password_hash=generate_password_hash('test123'),
            is_admin=True
        )
        db.session.add(test_admin)
        db.session.commit()
        print("Test admin user created!")
        print("Email: test@admin.com")
        print("Password: test123")

if __name__ == "__main__":
    create_test_admin()
