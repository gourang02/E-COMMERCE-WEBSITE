import os
import razorpay
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import stripe
from dotenv import load_dotenv
from flask_migrate import Migrate

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure app
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Database configuration
if os.environ.get('DATABASE_URL'):
    # Use PostgreSQL if DATABASE_URL is set (Neon/Vercel)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace('postgres://', 'postgresql://', 1)
else:
    # Development fallback - Use SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Initialize Flask-Migrate
migrate = Migrate()
migrate.init_app(app, db)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Make 'now' and 'timedelta' available in all templates
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow(), 'timedelta': timedelta}

# Razorpay Configuration
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', 'your_razorpay_key_id')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', 'your_razorpay_key_secret')

# Initialize Razorpay client
if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET and RAZORPAY_KEY_ID != 'your_razorpay_key_id':
    try:
        razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        RAZORPAY_ENABLED = True
        print("Razorpay enabled")
    except Exception as e:
        print(f"Razorpay initialization failed: {e}")
        razorpay_client = None
        RAZORPAY_ENABLED = False
else:
    razorpay_client = None
    RAZORPAY_ENABLED = False
    print("Razorpay disabled - using mock mode")

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)   # ← ADD THIS
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship('Order', backref='user', lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')
    payment_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Add these new fields
    shipping_address = db.Column(db.String(500))
    city = db.Column(db.String(100))
    pincode = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    # Relationship with OrderItem
    items = db.relationship('OrderItem', backref='order', lazy=True)
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    product = db.relationship('Product', backref='order_items')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    products = Product.query.limit(8).all()
    return render_template('index.html', products=products)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
        
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')  # ADD THIS LINE
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))
        
        # Check if username already exists
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('Username already taken!', 'danger')
            return redirect(url_for('register'))
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered!', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(
            name=name,
            username=username,  # ADD THIS
            email=email, 
            password_hash=hashed_password
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('shop'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/shop')
def shop():
    category = request.args.get('category', 'all')
    if category == 'all':
        products = Product.query.all()
    else:
        products = Product.query.filter_by(category=category).all()
    return render_template('shop.html', products=products, category=category)

@app.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product_detail.html', product=product)

@app.route('/cart')
@login_required
def cart():
    cart_items = session.get('cart', {})
    products = []
    total = 0
    
    for product_id, quantity in cart_items.items():
        product = Product.query.get(int(product_id))
        if product:
            products.append({
                'product': product,
                'quantity': quantity,
                'subtotal': product.price * quantity
            })
            total += product.price * quantity
    
    return render_template('cart.html', cart_items=products, total=total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    cart = session.get('cart', {})
    
    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity
    
    session['cart'] = cart
    flash('Product added to cart!', 'success')
    return redirect(url_for('shop'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        session['cart'] = cart
        flash('Product removed from cart', 'info')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    # GET request - show checkout form
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('shop'))
    
    cart_items = session['cart']
    products = {}
    total = 0
    
    # Get product details for items in cart and check stock
    for product_id, quantity in cart_items.items():
        product = Product.query.get(int(product_id))
        if not product:
            flash(f'Product with ID {product_id} not found', 'danger')
            return redirect(url_for('cart'))
            
        if product.stock < quantity:
            flash(f'Sorry, only {product.stock} items available for {product.name}', 'danger')
            return redirect(url_for('cart'))
            
        products[product_id] = {
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'quantity': quantity,
            'subtotal': float(product.price) * quantity,
            'stock': product.stock
        }
        total += products[product_id]['subtotal']
    
    if request.method == 'POST':
        payment_method = request.form.get('payment_method')
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'address', 'city', 'pincode']
        for field in required_fields:
            if not request.form.get(field):
                flash(f'Please fill in all required fields', 'danger')
                return redirect(url_for('checkout'))
        
        try:
            if payment_method == 'online':
                payment_intent_id = request.form.get('payment_intent_id')
                if not payment_intent_id:
                    flash('Payment information is missing. Please try again.', 'danger')
                    return redirect(url_for('checkout'))
                
                try:
                    payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
                    if payment_intent.status != 'succeeded':
                        flash('Payment failed. Please try again or choose another payment method.', 'danger')
                        return redirect(url_for('checkout'))
                except Exception as e:
                    app.logger.error(f"Payment verification error: {str(e)}")
                    flash('Error verifying payment. Please try again.', 'danger')
                    return redirect(url_for('checkout'))
                
                payment_id = f'stripe_{payment_intent.id}'
                status = 'paid'
            else:
                payment_id = f'COD-{int(time.time())}'
                status = 'pending'
            
            # Start a database transaction
            db.session.begin_nested()
            
            # Create new order
            order = Order(
                user_id=current_user.id,
                total_amount=total,
                status=status,
                payment_id=payment_id,
                shipping_address=request.form.get('address'),
                city=request.form.get('city'),
                pincode=request.form.get('pincode'),
                phone=request.form.get('phone')
            )
            db.session.add(order)
            db.session.flush()  # Get the order ID
            
            # Add order items and update stock
            for product_id, item in products.items():
                product = Product.query.get(product_id)
                
                # Double-check stock before finalizing
                if product.stock < item['quantity']:
                    db.session.rollback()
                    flash(f'Sorry, only {product.stock} items available for {product.name}', 'danger')
                    return redirect(url_for('cart'))
                
                # Update product stock
                product.stock -= item['quantity']
                
                # Create order item
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product_id,
                    quantity=item['quantity'],
                    price=item['price']
                )
                db.session.add(order_item)
            
            # Commit the transaction
            db.session.commit()
            
            # Clear the cart only after successful order creation
            session.pop('cart', None)
            
            flash('Your order has been placed successfully!', 'success')
            return redirect(url_for('orders'))
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Checkout error: {str(e)}")
            flash('An error occurred while processing your order. Please try again.', 'danger')
            return redirect(url_for('checkout'))

    # For Razorpay payment
    if RAZORPAY_ENABLED and razorpay_client:
        try:
            # Create order in Razorpay
            razorpay_order = razorpay_client.order.create({
                'amount': int(total * 100),  # Convert to paise
                'currency': 'INR',
                'payment_capture': '1',  # Auto capture payment
                'notes': {
                    'user_id': current_user.id,
                    'email': current_user.email,
                    'order_type': 'ecommerce_order'
                }
            })
            
            razorpay_order_id = razorpay_order['id']
        except Exception as e:
            app.logger.error(f"Error creating Razorpay order: {str(e)}")
            razorpay_order_id = None
    else:
        # Mock mode - generate a fake order ID
        razorpay_order_id = f"mock_order_{current_user.id}_{int(datetime.utcnow().timestamp())}"
        print(f"Mock payment mode - generated order ID: {razorpay_order_id}")
    
    return render_template('checkout.html', 
                         products=products, 
                         total=total,
                         cart_items=cart_items,
                         razorpay_key=RAZORPAY_KEY_ID,
                         razorpay_order_id=razorpay_order_id,
                         amount=int(total * 100))  # Amount in paise

@app.route('/verify_payment', methods=['POST'])
@login_required
def verify_payment():
    if 'cart' not in session or not session['cart']:
        return jsonify({'error': 'Your cart is empty'}), 400
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request data'}), 400
            
        # Verify payment signature
        params_dict = {
            'razorpay_order_id': data.get('razorpay_order_id'),
            'razorpay_payment_id': data.get('razorpay_payment_id'),
            'razorpay_signature': data.get('razorpay_signature')
        }
        
        # Check if all required fields are present
        if not all(params_dict.values()):
            return jsonify({'error': 'Missing payment details'}), 400
        
        # Verify the payment signature
        try:
            if RAZORPAY_ENABLED and razorpay_client:
                razorpay_client.utility.verify_payment_signature(params_dict)
            else:
                # Mock mode - skip signature verification
                print(f"Mock payment verification for order: {params_dict['razorpay_order_id']}")
        except Exception as e:
            if RAZORPAY_ENABLED and razorpay_client:
                app.logger.error(f"Payment signature verification failed: {str(e)}")
                return jsonify({'error': 'Payment verification failed'}), 400
            else:
                # Mock mode - continue despite verification error
                print(f"Mock payment verification bypassed: {str(e)}")
        
        # If verification is successful, process the order
        cart_items = session['cart']
        total = 0
        products = {}
        
        # Calculate total and verify stock
        for product_id, quantity in cart_items.items():
            product = Product.query.get(int(product_id))
            if not product or product.stock < quantity:
                return jsonify({
                    'error': f'Product {product_id if product else ""} is out of stock or invalid',
                    'success': False
                }), 400
            
            total += product.price * quantity
            products[product_id] = {
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'quantity': quantity,
                'subtotal': float(product.price) * quantity
            }
        
        # Create order in database
        try:
            order = Order(
                user_id=current_user.id,
                total_amount=total,
                status='paid',
                payment_id=data['razorpay_payment_id'],
                shipping_address=data.get('address', 'N/A'),
                city=data.get('city', 'N/A'),
                pincode=data.get('pincode', 'N/A'),
                phone=data.get('phone', 'N/A')
            )
            db.session.add(order)
            db.session.flush()
            
            # Add order items and update stock
            for product_id, item in products.items():
                product = Product.query.get(product_id)
                product.stock -= item['quantity']
                
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product_id,
                    quantity=item['quantity'],
                    price=item['price']
                )
                db.session.add(order_item)
            
            db.session.commit()
            
            # Clear the cart after successful order
            session.pop('cart', None)
            
            return jsonify({
                'success': True,
                'redirect': url_for('orders')
            })
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error creating order: {str(e)}")
            return jsonify({
                'error': 'Failed to create order. Please try again.',
                'success': False
            }), 500
            
    except Exception as e:
        app.logger.error(f"Payment verification failed: {str(e)}")
        return jsonify({
            'error': 'Payment verification failed. Please try again.',
            'success': False
        }), 400

@app.route('/payment_success', methods=['POST'])
@login_required
def payment_success():
    payment_intent_id = request.form.get('payment_intent_id')
    cart_items = session.get('cart', {})
    
    total = 0
    for product_id, quantity in cart_items.items():
        product = Product.query.get(int(product_id))
        if product:
            total += product.price * quantity
    
    # Create order
    order = Order(
        user_id=current_user.id,
        total_amount=total,
        status='completed',
        payment_id=payment_intent_id
    )
    db.session.add(order)
    db.session.flush()
    
    # Create order items
    for product_id, quantity in cart_items.items():
        product = Product.query.get(int(product_id))
        if product:
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                price=product.price
            )
            db.session.add(order_item)
            
            # Update stock
            product.stock -= quantity
    
    db.session.commit()
    
    # Clear cart
    session['cart'] = {}
    
    flash('Payment successful! Your order has been placed.', 'success')
    return redirect(url_for('orders'))

@app.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=user_orders)

# Test route to check admin access
@app.route('/admin/test')
@login_required
def admin_test():
    if not current_user.is_admin:
        return jsonify({"status": "error", "message": "Access denied"}), 403
    return jsonify({"status": "success", "message": "Admin access granted", "user": current_user.email})

# Admin Routes
@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied', 'danger')
        return redirect(url_for('index'))
    
    try:
        total_users = User.query.count()
        total_products = Product.query.count()
        total_orders = Order.query.count()
        recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
        
        return render_template('admin/dashboard.html', 
                             total_users=total_users,
                             total_products=total_products,
                             total_orders=total_orders,
                             recent_orders=recent_orders)
    except Exception as e:
        app.logger.error(f'Error in admin_dashboard: {str(e)}')
        return f"An error occurred: {str(e)}", 500

@app.route('/admin/products')
@login_required
def admin_products():
    if not current_user.is_admin:
        flash('Access denied', 'danger')
        return redirect(url_for('index'))
    
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@app.route('/admin/product/add', methods=['GET', 'POST'])
@login_required
def admin_add_product():
    if not current_user.is_admin:
        flash('Access denied', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        product = Product(
            name=request.form.get('name'),
            category=request.form.get('category'),
            description=request.form.get('description'),
            price=float(request.form.get('price')),
            stock=int(request.form.get('stock')),
            image_url=request.form.get('image_url')
        )
        db.session.add(product)
        db.session.commit()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/add_product.html')
    
@app.route('/buy_now/<int:product_id>', methods=['POST'])
@login_required
def buy_now(product_id):
    # Add the product to the cart
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    session.modified = True
    
    flash('Product added to cart!', 'success')
    return redirect(url_for('checkout'))    

@app.route('/admin/product/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_product(id):
    if not current_user.is_admin:
        flash('Access denied', 'danger')
        return redirect(url_for('index'))
    
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.category = request.form.get('category')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.stock = int(request.form.get('stock'))
        product.image_url = request.form.get('image_url')
        
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/edit_product.html', product=product)

@app.route('/admin/product/delete/<int:id>')
@login_required
def admin_delete_product(id):
    if not current_user.is_admin:
        flash('Access denied', 'danger')
        return redirect(url_for('index'))
    
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        flash('Access denied', 'danger')
        return redirect(url_for('index'))
    
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

# This is needed for Vercel
app = app

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
