import requests
import webbrowser
import time

def get_public_url(local_port=5000):
    try:
        # Try using localtunnel.me service
        print("Trying to get a public URL...")
        
        # Start a tunnel using localtunnel.me
        import subprocess
        import sys
        
        # Install required package if not already installed
        try:
            import pyngrok
        except ImportError:
            print("Installing required package...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyngrok"])
            import pyngrok
        
        # Set your ngrok authtoken (optional but recommended)
        # from pyngrok import ngrok
        # ngrok.set_auth_token("YOUR_NGROK_AUTH_TOKEN")
        
        # Start the tunnel
        from pyngrok import ngrok
        print("Creating secure tunnel to localhost:5000...")
        public_url = ngrok.connect(5000, "http")
        
        print(f"\n✅ Public URL created successfully!")
        print(f"🌐 Your application is now available at: {public_url}")
        print("\nPress Ctrl+C to stop the tunnel when done.")
        
        # Keep the tunnel running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping the tunnel...")
            ngrok.kill()
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nAlternative solutions:")
        print("1. Try using ngrok directly: https://ngrok.com/")
        print("2. Try localtunnel: npx localtunnel --port 5000")
        print("3. Try Cloudflare Tunnel: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/")

if __name__ == "__main__":
    get_public_url(5000)
