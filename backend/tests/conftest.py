import pytest
from users import auth_service


@pytest.fixture(scope="class")
def auth_obj():
    return auth_service