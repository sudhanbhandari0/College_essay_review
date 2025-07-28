from auth import *

test_user = {
    "sub": "test@example.com",
    "name": "Test User"
}

print("Creating token...")
token = create_access_token(test_user)
print(f"Token created: {token[:50]}...")

print("\nVerifying token...")
payload = verify_token(token)
print(f"Token verified: {payload}")

print("\n✅ Auth system is working!")