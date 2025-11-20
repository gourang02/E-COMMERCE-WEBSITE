from app import app, db, Product
from datetime import datetime

def add_sample_products():
    with app.app_context():
        # Sample optical products with Indian pricing (in INR)
        products = [
            {
                'name': 'Classic Aviator Sunglasses',
                'category': 'sunglasses',
                'description': 'Timeless aviator style with UV400 protection and lightweight metal frame.',
                'price': 1299.00,
                'stock': 50,
                'image_url': 'https://images.unsplash.com/photo-1511499767150-a48a237ac008?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8YXZpYXRvciUyMHN1bmdsYXNzZXN8ZW58MHx8MHx8fDA%3D'
            },
            {
                'name': 'Round Retro Eyeglasses',
                'category': 'eyeglasses',
                'description': 'Vintage round frames with anti-reflective and blue light blocking lenses.',
                'price': 2499.00,
                'stock': 30,
                'image_url': 'https://images.unsplash.com/photo-1591076482166-7de61a2e7b30?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8cm91bmQlMjBleWVnbGFzc2VzfGVufDB8fDB8fHww'
            },
            {
                'name': 'Polarized Wayfarer Sunglasses',
                'category': 'sunglasses',
                'description': 'Classic wayfarer design with polarized lenses for 100% UV protection.',
                'price': 1799.00,
                'stock': 45,
                'image_url': 'https://images.unsplash.com/photo-1511499767150-a48a237ac008?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8d2F5ZmFyZXIlMjBzdW5nbGFzc2VzfGVufDB8fDB8fHww'
            },
            {
                'name': 'Rectangle Full Rim Eyeglasses',
                'category': 'eyeglasses',
                'description': 'Modern rectangle frames with anti-scratch and anti-reflective coating.',
                'price': 1999.00,
                'stock': 35,
                'image_url': 'https://images.unsplash.com/photo-1591076482166-7de61a2e7b30?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8cmVjdGFuZ2xlJTIwZXllZ2xhc3Nlc3xlbnwwfHwwfHx8MA%3D%3D'
            },
            {
                'name': 'Mirror Coated Sports Sunglasses',
                'category': 'sunglasses',
                'description': 'Wraparound sports sunglasses with mirror coating and shatterproof lenses.',
                'price': 2199.00,
                'stock': 25,
                'image_url': 'https://images.unsplash.com/photo-1511499767150-a48a237ac008?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8c3BvcnRzJTIwc3VuZ2xhc3Nlc3xlbnwwfHwwfHx8MA%3D%3D'
            },
            {
                'name': 'Tortoise Shell Eyeglasses',
                'category': 'eyeglasses',
                'description': 'Classic tortoise shell pattern frames with blue light filtering lenses.',
                'price': 2599.00,
                'stock': 20,
                'image_url': 'https://images.unsplash.com/photo-1591076482166-7de61a2e7b30?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8dG9ydG9pc2UlMjBzaGVsbCUyMGV5ZWdsYXNzZXN8ZW58MHx8MHx8fDA%3D'
            },
            {
                'name': 'Oversized Cat Eye Sunglasses',
                'category': 'sunglasses',
                'description': 'Fashionable oversized cat eye sunglasses with UV400 protection.',
                'price': 1499.00,
                'stock': 30,
                'image_url': 'https://images.unsplash.com/photo-1511499767150-a48a237ac008?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Y2F0JTIwZXllJTIwc3VuZ2xhc3Nlc3xlbnwwfHwwfHx8MA%3D%3D'
            },
            {
                'name': 'Rimless Eyeglasses',
                'category': 'eyeglasses',
                'description': 'Lightweight rimless frames with high-index lenses for ultimate comfort.',
                'price': 2999.00,
                'stock': 15,
                'image_url': 'https://images.unsplash.com/photo-1591076482166-7de61a2e7b30?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8cmltbGVzcyUyMGV5ZWdsYXNzZXN8ZW58MHx8MHx8fDA%3D'
            },
            {
                'name': 'Pilot Sunglasses with Gradient Lenses',
                'category': 'sunglasses',
                'description': 'Classic pilot style with gradient lenses and metal frame.',
                'price': 1899.00,
                'stock': 40,
                'image_url': 'https://images.unsplash.com/photo-1511499767150-a48a237ac008?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cGlsb3QlMjBzdW5nbGFzc2VzfGVufDB8fDB8fHww'
            },
            {
                'name': 'Browline Eyeglasses',
                'category': 'eyeglasses',
                'description': 'Vintage-inspired browline frames with anti-reflective coating.',
                'price': 2799.00,
                'stock': 18,
                'image_url': 'https://images.unsplash.com/photo-1591076482166-7de61a2e7b30?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fGJyb3dsaW5lJTIwZXllZ2xhc3Nlc3xlbnwwfHwwfHx8MA%3D%3D'
            },
            {
                'name': 'Round Metal Sunglasses',
                'category': 'sunglasses',
                'description': 'Minimalist round metal frames with polarized lenses.',
                'price': 1599.00,
                'stock': 22,
                'image_url': 'https://images.unsplash.com/photo-1511499767150-a48a237ac008?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cm91bmQlMjBtZXRhbCUyMHN1bmdsYXNzZXN8ZW58MHx8MHx8fDA%3D'
            },
            {
                'name': 'Semi-Rimless Eyeglasses',
                'category': 'eyeglasses',
                'description': 'Semi-rimless design with spring hinges for comfort and durability.',
                'price': 2399.00,
                'stock': 28,
                'image_url': 'https://images.unsplash.com/photo-1591076482166-7de61a2e7b30?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fHNlbWktcmltbGVzcyUyMGV5ZWdsYXNzZXN8ZW58MHx8MHx8fDA%3D'
            }
        ]

        # Add products to database
        for product_data in products:
            # Check if product already exists
            existing = Product.query.filter_by(name=product_data['name']).first()
            if not existing:
                product = Product(
                    name=product_data['name'],
                    category=product_data['category'],
                    description=product_data['description'],
                    price=product_data['price'],
                    stock=product_data['stock'],
                    image_url=product_data['image_url'],
                    created_at=datetime.utcnow()
                )
                db.session.add(product)
                print(f"Added product: {product_data['name']}")
            else:
                print(f"Product already exists: {product_data['name']}")
        
        db.session.commit()
        print("\nAll products have been added successfully!")

if __name__ == "__main__":
    add_sample_products()
