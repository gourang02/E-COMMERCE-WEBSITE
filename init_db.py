from app import app, db, Product, User
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        # Create all database tables
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(email='admin@example.com').first()
        if admin:
            # Update existing admin password
            admin.password_hash = generate_password_hash('admin123')
            admin.is_admin = True
            db.session.commit()
            print("Admin password reset!")
        else:
            # Create admin user
            admin = User(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True,
                name='Admin User'  # Add the required name field
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created!")
        
        # Add some sample products if none exist
        if Product.query.count() == 0:
            products = [
                Product(
                    name="Classic Aviator Sunglasses",
                    category="sunglasses",
                    description="Timeless aviator sunglasses with UV protection.",
                    price=129.99,
                    stock=50,
                    image_url="/static/images/aviator.jpg"
                ),
                Product(
                    name="Vintage Round Glasses",
                    category="eyeglasses",
                    description="Stylish round frames for a retro look.",
                    price=89.99,
                    stock=30,
                    image_url="/static/images/round.jpg"
                ),
                # Add more sample products as needed
            ]
            
            for product in products:
                db.session.add(product)
            
            db.session.commit()
            print("Sample products added!")

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
