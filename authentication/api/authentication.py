"""
Custom JWT authentication using access tokens stored in cookies.
"""

from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    """
    Authenticates users using a JWT access token stored in cookies.
    """

    def authenticate(self, request):
        """
        Retrieves and validates the access token from the request cookies.
        """

        raw_token = request.COOKIES.get("access_token")

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)

        return user, validated_token
