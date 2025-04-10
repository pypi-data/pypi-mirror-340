from typing import Dict, Any
from ..models.auth import AuthResponse, LoginResponse
from ..exceptions import AuthenticationError
from .base import BaseResource

class AuthMixin(BaseResource):
    """Authentication related API endpoints"""

    def login(self, email: str, password: str) -> LoginResponse:
        """
        Authenticate user and get access token
        
        Args:
            email (str): User email
            password (str): User password
            
        Returns:
            LoginResponse: Authentication response containing user info and token
            
        Raises:
            AuthenticationError: If login credentials are invalid
            APIError: If API request fails
        """
        response = self._request(
            method="POST",
            endpoint="/auth/login",
            data={
                "email": email,
                "password": password
            }
        )
        
        auth_response = AuthResponse(**response)
        
        if not auth_response.success:
            raise AuthenticationError(auth_response.message)
            
        return LoginResponse(**auth_response.data)

    def logout(self) -> bool:
        """
        Logout the current user and invalidate the token
        
        Returns:
            bool: True if logout was successful
        
        Raises:
            APIError: If API request fails
        """
        response = self._request(
            method="POST",
            endpoint="/auth/logout"
        )
        
        return response.get('ok', False)

