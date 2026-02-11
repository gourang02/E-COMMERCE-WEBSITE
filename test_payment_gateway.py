from app import app, razorpay_client, RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET

def test_payment_gateway():
    with app.app_context():
        print("Testing Payment Gateway Configuration...")
        print(f"Razorpay Key ID: {RAZORPAY_KEY_ID}")
        print(f"Razorpay Secret Key: {'*' * len(RAZORPAY_KEY_SECRET) if RAZORPAY_KEY_SECRET else 'None'}")
        
        # Test Razorpay client initialization
        try:
            # Try to create a test order
            test_order = razorpay_client.order.create({
                'amount': 100,  # 1 rupee in paise
                'currency': 'INR',
                'payment_capture': '1',
                'notes': {
                    'test': 'payment_gateway_test'
                }
            })
            
            print(f"✅ Razorpay client initialized successfully!")
            print(f"✅ Test order created: {test_order['id']}")
            
            # Clean up - cancel the test order
            try:
                razorpay_client.order.cancel(test_order['id'])
                print("✅ Test order cancelled successfully")
            except:
                print("⚠️  Could not cancel test order (this is normal)")
                
        except Exception as e:
            print(f"❌ Razorpay client error: {str(e)}")
            print("Please check your API keys and internet connection")
            return False
        
        print("\n🎉 Payment gateway is configured and working!")
        return True

if __name__ == "__main__":
    test_payment_gateway()
