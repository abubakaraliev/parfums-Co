import pytest


@pytest.mark.usefixtures('auth_obj')
class TestAuthenticate:

    def test_create_salt_and_hashed_password(self, auth_obj):
        test_password = '123456789'
        first_password = auth_obj.create_salt_and_hashed_password(plaintext_password=test_password)
        second_password = auth_obj.create_salt_and_hashed_password(plaintext_password=test_password)
        assert first_password.password is not second_password.password