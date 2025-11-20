import os
import subprocess
import sys
import webbrowser

def install_package(package):
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def get_local_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't need to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def main():
    print("🚀 Setting up public access for your local server...")
    
    # Check if localtunnel is installed, if not install it
    try:
        import localtunnel
    except ImportError:
        print("Localtunnel not found. Installing...")
        install_package('localtunnel')
    
    # Get the port your Flask app is running on (default is 5000)
    port = 5000
    
    print(f"\n🌐 Your local IP address: {get_local_ip()}:{port}")
    print("   (Use this on devices connected to the same WiFi network)")
    
    print("\n🌍 Setting up public URL (this may take a moment)...")
    
    try:
        from localtunnel import start_tunnel
        
        def on_url_callback(url):
            print(f"\n✅ Public URL created successfully!")
            print(f"🔗 {url}")
            print("\n📱 Share this URL to access from any device")
            print("   (Press Ctrl+C to stop the server when done)")
            
            # Open in default browser
            webbrowser.open(url)
        
        # Start the tunnel
        tunnel = start_tunnel(port, subdomain=None, on_url=on_url_callback)
        
        # Keep the script running
        while True:
            try:
                import time
                time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Stopping the server...")
                tunnel.close()
                break
                
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nAlternative solutions:")
        print("1. Make sure your Flask app is running on port 5000")
        print("2. Try running: npx localtunnel --port 5000")
        print("3. Check your internet connection")

if __name__ == "__main__":
    main()
