import pytest
from pydantic import ValidationError

from app.modules.auth.schemas import RegisterRequest


def test_register_rejects_role_in_body():
    with pytest.raises(ValidationError):
        RegisterRequest(
            username="budi",
            password="rahasia123",
            name="Budi",
            email="budi@mail.com",
            role="admin",
        )


def test_register_ok_without_role():
    data = RegisterRequest(
        username="budi", password="rahasia123", name="Budi", email="budi@mail.com"
    )
    assert data.username == "budi"