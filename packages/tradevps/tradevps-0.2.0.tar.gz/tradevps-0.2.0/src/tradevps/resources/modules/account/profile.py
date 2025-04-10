from ....models.account import Profile
from ...base import BaseResource

class ProfileMixin(BaseResource):
    """Profile management endpoints"""
    
    def profile(self) -> Profile:
        """
        Provide the current user's profile
        
        Returns:
            Profile: User profile information
            
        Raises:
            APIError: If API request fails
        """
        response = self._request(
            method="GET",
            endpoint="/my/account/profile"
        )
        
        return Profile(**response['data'])
