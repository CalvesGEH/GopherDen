from pytest import raises

from repos.all_repositories import AllRepositories
from schema.user import CreateUserRegistration, UserCreate
from services.user_services.registration_service import RegistrationService


class UserCreationTests():
    def test_create_user(self, database:AllRepositories, unique_user:UserCreate) -> None:
        new_user = database.users.create(unique_user)
        assert new_user is not None

        assert new_user.email == unique_user.email
        assert new_user.username == unique_user.username
        assert new_user.password == unique_user.password # This should work because in a testing env, we use FakeHasher
        assert new_user.admin == False

    def test_register_user(self, registration_service:RegistrationService, unique_user:UserCreate) -> None:
        user_registration_form = CreateUserRegistration(
            email=unique_user.email,
            username=unique_user.username,
            password=unique_user.password,
            password_confirm=unique_user.password,
        )

        new_user = registration_service.register_user(user_registration_form)
        assert new_user is not None

        assert new_user.email == unique_user.email.lower()
        assert new_user.username == unique_user.username
        assert new_user.password == unique_user.password # This should work because in a testing env, we use FakeHasher

    def test_register_mismatched_passwords(self, unique_user:UserCreate) -> None:
        with raises(ValueError) as e:
            CreateUserRegistration(
                email=unique_user.email,
                username=unique_user.username,
                password=unique_user.password,
                password_confirm=unique_user.password + "1",
            )
        # This is technically a pydantic error so we have to workaround to get the error message
        assert e.value.errors()[0]['msg'].split(', ')[1] == "passwords do not match"

    def test_register_already_registered_username(self, registration_service:RegistrationService, unique_user:UserCreate) -> None:
        user_registration_form = CreateUserRegistration(
            email=unique_user.email,
            username=unique_user.username,
            password=unique_user.password,
            password_confirm=unique_user.password,
        )

        registration_service.register_user(user_registration_form)
        user_registration_form.email = user_registration_form.email + "salt"
        with raises(Exception) as e:
            registration_service.register_user(user_registration_form)
        assert e.value.status_code == 409
        assert e.value.detail == { "message": "Username already exists" }

    def test_register_already_registered_email(self, registration_service:RegistrationService, unique_user:UserCreate) -> None:
        user_registration_form = CreateUserRegistration(
            email=unique_user.email,
            username=unique_user.username,
            password=unique_user.password,
            password_confirm=unique_user.password,
        )

        registration_service.register_user(user_registration_form)
        user_registration_form.username = user_registration_form.username + "salt"
        with raises(Exception) as e:
            registration_service.register_user(user_registration_form)
        assert e.value.status_code == 409
        assert e.value.detail == { "message": "Email already exists" }

class UserRepoTests():
    def test_get_user_by_username(self, database:AllRepositories, unique_user:UserCreate) -> None:
        database.users.create(unique_user)

        user = database.users.get_by_username(unique_user.username)
        assert user is not None

    def test_get_user_by_email(self, database:AllRepositories, unique_user:UserCreate) -> None:
        database.users.create(unique_user)

        user = database.users.get_by_email(unique_user.email)
        assert user is not None

    