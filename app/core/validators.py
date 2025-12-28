import os
import sys

def validate_environment():
    """Validate that all required environment variables are set"""
    required_vars = {
        "MONGO_URI": "MongoDB connection string",
        "SECRET_KEY": "JWT secret key for token signing",
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_vars.append(f"  - {var}: {description}")
    
    if missing_vars:
        error_msg = "❌ Missing required environment variables:\n" + "\n".join(missing_vars)
        print(error_msg, file=sys.stderr)
        print("\n💡 Set these variables in your Vercel project settings or .env file", file=sys.stderr)
        return False
    
    print("✅ All required environment variables are set")
    return True
