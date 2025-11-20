import socket
import webbrowser
from datetime import datetime

def get_local_ip():
    """Get the local IP address of the computer"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google's public DNS
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception:
        return "127.0.0.1"

def check_port_open(ip, port):
    """Check if a port is open and accepting connections"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0

def main():
    print("\n" + "="*50)
    print("  >>> Local Network Server Access Tool")
    print("="*50)
    
    port = 5000  # Default Flask port
    local_ip = get_local_ip()
    
    print(f"\n🔍 Checking your setup...")
    print(f"   Local IP Address: {local_ip}")
    print(f"   Port to check: {port}")
    
    if check_port_open(local_ip, port):
        print("\n[SUCCESS] Great! Your local server is accessible on your network.")
        print(f"\n🌐 Access your site from other devices on the same WiFi:")
        print(f"   http://{local_ip}:{port}")
        
        print("\n📱 On your mobile device:")
        print(f"   1. Connect to the same WiFi network as this computer")
        print(f"   2. Open a web browser")
        print(f"   3. Go to: http://{local_ip}:{port}")
        
        print("\n🔒 Security Note: This only works on the same network.")
        
        # Try to open the URL in default browser
        try:
            webbrowser.open(f"http://{local_ip}:{port}")
        except:
            pass
    else:
        print("\n[ERROR] Oops! Couldn't connect to the server.")
        print("\nTroubleshooting steps:")
        print("1. Make sure your Flask app is running")
        print("2. Check if your firewall is blocking port", port)
        print("3. Try running: flask run --host=0.0.0.0")
        
        if "127.0.0.1" not in local_ip:
            print("\n[INFO] Try accessing from this computer first:")
            print(f"   http://localhost:{port} or http://127.0.0.1:{port}")
    
    print("\n" + "="*50)
    print(f"  Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
