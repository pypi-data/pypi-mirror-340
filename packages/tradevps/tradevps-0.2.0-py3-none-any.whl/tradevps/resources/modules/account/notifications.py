from typing import Optional, Dict, Any
from ....models.notifications import NotificationList, Notification
from ...base import BaseResource

class NotificationsMixin(BaseResource):
    """Notifications management endpoints"""
    
    def notifications(self, unread: bool = False, page: int = 1) -> NotificationList:
        """
        Provide user notifications
        
        Args:
            unread: If True, only fetch unread notifications
            page: Page number for pagination
            
        Returns:
            NotificationList: List of notifications with pagination info
            
        Raises:
            APIError: If API request fails
        """
        params = {
            "page": page
        }
        if unread:
            params["unread"] = "true"
            
        response = self._request(
            method="GET",
            endpoint="/my/account/notifications",
            params=params
        )
        
        return NotificationList(**response)

    def mark_notification_as_read(self, notification_id: str) -> Notification:
        """
        Mark a notification as read
        
        Args:
            notification_id: UUID of the notification
            
        Returns:
            Notification: Updated notification object with read_at timestamp
            
        Raises:
            APIError: If API request fails
        """
        response = self._request(
            method="POST",
            endpoint=f"/my/account/notifications/{notification_id}/read"
        )
        
        return Notification(**response['data'])

    def mark_all_notifications_as_read(self) -> bool:
        """
        Mark all notifications as read
        
        Returns:
            bool: True if successful
            
        Raises:
            APIError: If API request fails
        """
        response = self._request(
            method="POST",
            endpoint="/my/account/notifications/read-all"
        )
        
        return response.get('ok', False)
