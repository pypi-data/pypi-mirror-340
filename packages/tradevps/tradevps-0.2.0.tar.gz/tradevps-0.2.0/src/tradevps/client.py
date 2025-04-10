import requests
from typing import Dict, Any, Optional
from .exceptions import APIError
from .resources.base import BaseResource
from .resources.account import ProfileMixin, NotificationsMixin, TokensMixin
from .resources.auth import AuthMixin

class Client(AuthMixin, ProfileMixin, NotificationsMixin, TokensMixin):
    """
    Official Python client for TradeVPS API
    
    Args:
        api_key (str, optional): API key for authentication
        base_url (str, optional): Base URL for API endpoints
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.tradevps.net/v1"
    ):
        self.base_url = base_url.rstrip('/')
        self._session = requests.Session()
        if api_key:
            self.set_api_key(api_key)

    def set_api_key(self, api_key: str) -> None:
        """Set the API key for authentication"""
        self._session.headers.update({
            "Authorization": f"Bearer {api_key}"
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to API"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        response = self._session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            headers=headers
        )
        
        try:
            response_data = response.json()
        except ValueError:
            raise APIError("Invalid JSON response from API")

        if not response.ok:
            raise APIError(
                message=response_data.get('message', 'Unknown error'),
                status_code=response.status_code
            )

        return response_data










