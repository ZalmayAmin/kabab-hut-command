from waitress import serve
from app import app

if __name__ == "__main__":
    print("Kabab Hut Central Command is running in PRODUCTION mode...")
    print("Access the Vault at: http://localhost:5001")
    # This runs your app on port 5001 with 4 threads for handling multiple leads at once
    serve(app, host='0.0.0.0', port=5001, threads=4)