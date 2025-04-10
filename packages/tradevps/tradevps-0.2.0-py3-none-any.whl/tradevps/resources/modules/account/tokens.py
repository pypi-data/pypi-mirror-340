from datetime import datetime
from typing import Optional, List
from ....models.tokens import APITokenList, APITokenResponse
from ...base import BaseResource

class TokensMixin(BaseResource):
    """API tokens management endpoints"""
    
    def tokens(self, page: int = 1) -> APITokenList:
        """
        List API tokens
        
        Args:
            page: Page number for pagination
            
        Returns:
            APITokenList: List of API tokens with pagination info
            
        Raises:
            APIError: If API request fails
        """
        response = self._request(
            method="GET",
            endpoint="/my/account/tokens",
            params={"page": page}
        )
        
        return APITokenList(**response)

    def create_token(
        self,
        name: str,
        expires_at: Optional[datetime] = None,
        abilities: Optional[List[str]] = None
    ) -> APITokenResponse:
        """
        Create a new API token
        
        Args:
            name: Token name
            expires_at: Token expiration date (optional)
            abilities: List of token abilities (optional)
            
        Returns:
            APITokenResponse: Created token details
            
        Raises:
            APIError: If API request fails
        """
        data = {"name": name}
        
        if expires_at:
            data["expires_at"] = expires_at.isoformat()
        
        if abilities:
            data["abilities"] = abilities
            
        response = self._request(
            method="POST",
            endpoint="/my/account/tokens",
            data=data
        )
        
        return APITokenResponse(**response["data"])

    def revoke_token(self, token_id: int) -> bool:
        """
        Revoke an API token
        
        Args:
            token_id: ID of the token to revoke
            
        Returns:
            bool: True if token was revoked successfully
            
        Raises:
            APIError: If API request fails
        """
        response = self._request(
            method="DELETE",
            endpoint=f"/my/account/tokens/{token_id}"
        )
        
        return response.get("ok", False)