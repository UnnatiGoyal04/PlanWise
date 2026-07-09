from app.core.security import create_access_token
token = create_access_token(
    subject="1"
)
print(token)