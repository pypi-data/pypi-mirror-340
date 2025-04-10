import pytest
from tradevps import Client
from tradevps.exceptions import APIError
from datetime import datetime
from uuid import UUID

class TestProfileEndpoints:
    def test_profile_success(self, mocker):
        client = Client(api_key="test-token")
        
        mock_response = {
            "ok": True,
            "msg": "Profile fetched",
            "data": {
                "id": "9ddc0e2a-74cc-434c-bb93-1d0a39fdf9c8",
                "name": "Test User",
                "email": "test@example.com",
                "email_verified_at": "2024-12-31T22:36:00.000000Z",
                "plan": 0,
                "status": 0,
                "plan_expires_at": None,
                "created_at": "2024-12-31T22:36:00.000000Z",
                "updated_at": "2024-12-31T22:36:00.000000Z",
                "deleted_at": None,
                "referrer_id": None
            }
        }
        
        mocker.patch.object(client, '_request', return_value=mock_response)
        
        profile = client.profile()
        
        assert isinstance(profile.id, UUID)
        assert profile.id == UUID("9ddc0e2a-74cc-434c-bb93-1d0a39fdf9c8")
        assert profile.name == "Test User"
        assert profile.email == "test@example.com"
        assert isinstance(profile.email_verified_at, datetime)
        assert isinstance(profile.created_at, datetime)
        assert isinstance(profile.updated_at, datetime)
        assert profile.plan == 0
        assert profile.status == 0
        assert profile.plan_expires_at is None
        assert profile.deleted_at is None
        assert profile.referrer_id is None

    def test_profile_api_error(self, mocker):
        client = Client(api_key="test-token")
        
        mocker.patch.object(
            client, 
            '_request',
            side_effect=APIError("Invalid token", status_code=401)
        )
        
        with pytest.raises(APIError) as exc:
            client.profile()
        
        assert exc.value.message == "Invalid token"
        assert exc.value.status_code == 401

class TestNotificationEndpoints:
    def test_notifications_success(self, mocker):
        client = Client(api_key="test-token")
        
        mock_response = {
            "data": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "type": "App\\Notifications\\SomeNotification",
                    "notifiable_id": "user_id",
                    "notifiable_model": "App\\Models\\User",
                    "data": {
                        "key": "value"
                    },
                    "read_at": None,
                    "created_at": "2024-01-19T12:00:00.000000Z",
                    "updated_at": "2024-01-19T12:00:00.000000Z"
                }
            ],
            "pagination": {
                "current_page": 1,
                "last_page": 1,
                "per_page": 15,
                "total": 1,
                "first_page_url": "https://api.tradevps.net/v1/my/account/notifications?page=1",
                "from": 1,
                "last_page_url": "https://api.tradevps.net/v1/my/account/notifications?page=1",
                "next_page_url": None,
                "prev_page_url": None
            }
        }
        
        mocker.patch.object(client, '_request', return_value=mock_response)
        
        notifications = client.notifications(unread=True)
        
        assert len(notifications.data) == 1
        notification = notifications.data[0]
        assert str(notification.id) == "550e8400-e29b-41d4-a716-446655440000"
        assert notification.type == "App\\Notifications\\SomeNotification"
        assert notification.notifiable_id == "user_id"
        assert notification.notifiable_model == "App\\Models\\User"
        assert notification.data == {"key": "value"}
        assert notification.read_at is None
        assert isinstance(notification.created_at, datetime)
        assert isinstance(notification.updated_at, datetime)
        
        # Test pagination
        assert notifications.pagination.current_page == 1
        assert notifications.pagination.total == 1
        assert notifications.pagination.per_page == 15
        assert notifications.pagination.next_page_url is None

    def test_mark_notification_as_read(self, mocker):
        client = Client(api_key="test-token")
        notification_id = "550e8400-e29b-41d4-a716-446655440000"
        
        mock_response = {
            "ok": True,
            "message": "Notification marked as read",
            "data": {
                "id": notification_id,
                "type": "App\\Notifications\\SomeNotification",
                "notifiable_id": "user_id",
                "notifiable_model": "App\\Models\\User",
                "data": {},
                "read_at": "2024-01-20T12:00:00.000000Z",
                "created_at": "2024-01-19T12:00:00.000000Z",
                "updated_at": "2024-01-20T12:00:00.000000Z"
            }
        }
        
        mocker.patch.object(client, '_request', return_value=mock_response)
        
        notification = client.mark_notification_as_read(notification_id)
        
        assert str(notification.id) == notification_id
        assert notification.type == "App\\Notifications\\SomeNotification"
        assert notification.notifiable_id == "user_id"
        assert notification.notifiable_model == "App\\Models\\User"
        assert isinstance(notification.read_at, datetime)
        assert isinstance(notification.created_at, datetime)
        assert isinstance(notification.updated_at, datetime)

    def test_mark_all_notifications_as_read(self, mocker):
        client = Client(api_key="test-token")
        
        mock_response = {
            "ok": True,
            "message": "All notifications marked as read",
            "data": None
        }
        
        mocker.patch.object(client, '_request', return_value=mock_response)
        
        result = client.mark_all_notifications_as_read()
        assert result is True

    def test_mark_all_notifications_as_read_failure(self, mocker):
        client = Client(api_key="test-token")
        
        mock_response = {
            "ok": False,
            "message": "Failed to mark notifications as read",
            "data": None
        }
        
        mocker.patch.object(client, '_request', return_value=mock_response)
        
        result = client.mark_all_notifications_as_read()
        assert result is False

class TestTokenEndpoints:
    def test_list_tokens_success(self, mocker):
        client = Client(api_key="test-token")
        
        mock_response = {
            "ok": True,
            "msg": "API tokens fetched",
            "data": [
                {
                    "id": 12681,
                    "tokenable_type": "App\\Models\\User",
                    "tokenable_id": "9ddc0e2a-74cc-434c-bb93-1d0a39fdf9c8",
                    "name": "API Token",
                    "abilities": ["*"],
                    "last_used_at": "2025-04-04T10:18:06.000000Z",
                    "expires_at": None,
                    "created_at": "2025-04-04T10:07:08.000000Z",
                    "updated_at": "2025-04-04T10:18:06.000000Z"
                }
            ],
            "pagination": {
                "current_page": 1,
                "last_page": 836,
                "per_page": 10,
                "total": 8352,
                "first_page_url": "https://api.tradevps.net/v1/my/account/tokens?page=1",
                "from": 1,
                "last_page_url": "https://api.tradevps.net/v1/my/account/tokens?page=836",
                "next_page_url": "https://api.tradevps.net/v1/my/account/tokens?page=2",
                "prev_page_url": None
            }
        }
        
        mocker.patch.object(client, '_request', return_value=mock_response)
        
        tokens = client.tokens()
        
        assert len(tokens.data) == 1
        token = tokens.data[0]
        assert token.id == 12681
        assert token.name == "API Token"
        assert token.abilities == ["*"]
        assert isinstance(token.last_used_at, datetime)
        assert token.expires_at is None
        
        # Test pagination
        assert tokens.pagination.current_page == 1
        assert tokens.pagination.total == 8352
        assert tokens.pagination.per_page == 10
        assert tokens.pagination.next_page_url == "https://api.tradevps.net/v1/my/account/tokens?page=2"

    def test_create_token_success(self, mocker):
        client = Client(api_key="test-token")
        
        mock_response = {
            "ok": True,
            "msg": "API token generated",
            "data": {
                "token": "12683|ZDiVXbGAkllUTtDRmWazV5XPn2MZhoUKPnaKCkOH5f6b02b2",
                "name": "My API Token"
            }
        }
        
        mocker.patch.object(client, '_request', return_value=mock_response)
        
        expires_at = datetime(2024, 12, 31, 23, 59, 59)
        token = client.create_token(
            name="My API Token",
            expires_at=expires_at,
            abilities=["read", "write", "delete"]
        )
        
        assert token.name == "My API Token"
        assert token.token == "12683|ZDiVXbGAkllUTtDRmWazV5XPn2MZhoUKPnaKCkOH5f6b02b2"

    def test_revoke_token_success(self, mocker):
        client = Client(api_key="test-token")
        
        mock_response = {
            "ok": True,
            "msg": "API token revoked",
            "data": None
        }
        
        mocker.patch.object(client, '_request', return_value=mock_response)
        
        result = client.revoke_token(12683)
        assert result is True










