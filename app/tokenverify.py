from .models import *
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication

def verify_and_extract_token_data(token):
    try:
        # Decode the token and get the payload
        decoded_token = AccessToken(token)
        payload = decoded_token.payload
        print("-----", payload)
        user_id=payload["user_id"]
        user=User.objects.get(id=user_id)
        return user
    except TokenError as e:
        # Handle token verification errors
        print(f"Token verification failed: {e}")
        return None