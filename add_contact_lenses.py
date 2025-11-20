from app import app, db, Product
from datetime import datetime

def add_contact_lenses():
    contact_lenses = [
        # Daily Disposable Lenses
        {
            'name': 'Acuvue Oasys 1-Day (30 Lenses)',
            'category': 'contact-lenses',
            'price': 1499.00,
            'stock': 50,
            'description': 'Daily disposable contact lenses with UV protection and HydraLuxe Technology for all-day comfort.',
            'image_url': 'https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Dailies AquaComfort Plus (90 Lenses)',
            'category': 'contact-lenses',
            'price': 2999.00,
            'stock': 40,
            'description': 'Premium daily disposable lenses with 3 moisture agents for lasting comfort throughout the day.',
            'image_url': 'https://images.unsplash.com/photo-1595475884565-3d0bdd54b095?w=800&auto=format&fit=crop&q=80'
        },
        # More products...
    ]

    with app.app_context():
        for lens in contact_lenses:
            existing = Product.query.filter_by(name=lens['name']).first()
            if not existing:
                new_lens = Product(
                    name=lens['name'],
                    category=lens['category'],
                    price=lens['price'],
                    stock=lens['stock'],
                    description=lens['description'],
                    image_url=lens['image_url']
                )
                db.session.add(new_lens)
                print(f"Added: {lens['name']}")
            else:
                print(f"Already exists: {lens['name']}")
        
        db.session.commit()
        print("\\nContact lenses have been added to the database!")

if __name__ == '__main__':
    print("Adding contact lenses to the database...")
    add_contact_lenses()