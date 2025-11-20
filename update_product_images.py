from app import app, db, Product

def update_product_images():
    with app.app_context():
        # Update each product with appropriate optical product images
        products = Product.query.all()
        
        # Optical product images from a free stock photo service (replace with your actual image URLs)
        image_urls = [
            "https://images.unsplash.com/photo-1556300902-451cccad62e5?w=500&auto=format&fit=crop&q=80",  # Aviator
            "https://images.unsplash.com/photo-1572635148818-ef6fd7eb32fc?w=500&auto=format&fit=crop&q=80",  # Round
            "https://images.unsplash.com/photo-1572635196184-35d5e9abeb50?w=500&auto=format&fit=crop&q=80",  # Wayfarer
            "https://images.unsplash.com/photo-1591076482166-7de61a2e7b30?w=500&auto=format&fit=crop&q=80",  # Rectangle
            "https://images.unsplash.com/photo 1521577352947-5958cb9ae5ef?w=500&auto=format&fit=crop&q=80",  # Sports
            "https://images.unsplash.com/photo-1555529669-e69e7aa0ba9a?w=500&auto=format&fit=crop&q=80",  # Cat Eye
            "https://images.unsplash.com/photo-1586339949916-3e945bcbef9a?w=500&auto=format&fit=crop&q=80",  # Rimless
            "https://images.unsplash.com/photo-1556300902-451cccad62e5?w=500&auto=format&fit=crop&q=80",  # Pilot
            "https://images.unsplash.com/photo-1555529669-e69e7aa0ba9a?w=500&auto=format&fit=crop&q=80",  # Browline
            "https://images.unsplash.com/photo-1572635148818-ef6fd7eb32fc?w=500&auto=format&fit=crop&q=80",  # Round Metal
            "https://images.unsplash.com/photo-1586339949916-3e945bcbef9a?w=500&auto=format&fit=crop&q=80",  # Semi-Rimless
            "https://images.unsplash.com/photo-1555529669-e69e7aa0ba9a?w=500&auto=format&fit=crop&q=80"   # Tortoise Shell
        ]
        
        for i, product in enumerate(products):
            if i < len(image_urls):
                product.image_url = image_urls[i]
                print(f"Updated image for {product.name}")
        
        db.session.commit()
        print("\nAll product images have been updated successfully!")

if __name__ == "__main__":
    update_product_images()
