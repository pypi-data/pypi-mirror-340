from typing import Dict, Any, Optional
from ..exceptions import APIError

class BaseResource:
    """Base class for all API resources"""
    
    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to API
        This should be implemented by the main client
        """
        raise NotImplementedError
