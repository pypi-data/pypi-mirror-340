import pytest
from tradevps import Client
from tradevps.exceptions import AuthenticationError

def test_login_success(mocker):
    client = Client()
    
    mock_response = {
        "success": True,
        "message": "Login success",
        "data": {
            "user": {
                "name": "Test User",
                "email": "test@tradevps.net"
            },
            "token": "test-token",
            "token_type": "Bearer"
        }
    }
    
    mocker.patch.object(
        client,
        '_request',
        return_value=mock_response
    )
    
    response = client.login("test@tradevps.net", "password")
    
    assert response.token == "test-token"
    assert response.user.name == "Test User"
    assert response.user.email == "test@tradevps.net"

def test_login_failure(mocker):
    client = Client()
    
    mock_response = {
        "success": False,
        "message": "Invalid email or password",
        "data": None
    }
    
    mocker.patch.object(
        client,
        '_request',
        return_value=mock_response
    )
    
    with pytest.raises(AuthenticationError) as exc:
        client.login("test@tradevps.net", "wrong-password")
    
    assert str(exc.value) == "Invalid email or password"

def test_logout_success(mocker):
    client = Client(api_key="test-token")
    
    mock_response = {
        "ok": True,
        "msg": "Logout successfully",
        "data": None
    }
    
    mocker.patch.object(
        client,
        '_request',
        return_value=mock_response
    )
    
    result = client.logout()
    assert result is True

def test_logout_failure(mocker):
    client = Client(api_key="test-token")
    
    mock_response = {
        "ok": False,
        "msg": "Invalid token",
        "data": None
    }
    
    mocker.patch.object(
        client,
        '_request',
        return_value=mock_response
    )
    
    result = client.logout()
    assert result is False

