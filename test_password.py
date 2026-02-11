from app import app, db, User
from werkzeug.security import check_password_hash

def test_password():
    with app.app_context():
        admin = User.query.filter_by(email='admin@example.com').first()
        if admin:
            print(f"Admin user found: {admin.email}")
            print(f"Username: {admin.username}")
            print(f"Is admin: {admin.is_admin}")
            
            # Test different passwords
            passwords_to_test = ['admin123', 'Admin123', 'password', 'admin']
            for pwd in passwords_to_test:
                result = check_password_hash(admin.password_hash, pwd)
                print(f"Password '{pwd}': {result}")
        else:
            print("Admin user not found!")

if __name__ == "__main__":
    test_password()
