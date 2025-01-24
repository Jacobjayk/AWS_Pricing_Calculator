import secrets

# Generate a 50-character long random string
secret_key = secrets.token_urlsafe(50) 

print(secret_key)