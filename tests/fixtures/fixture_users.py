import pytest

from tests.utils import random_person, randomword

from backend.repos.all_repositories import AllRepositories
from backend.services.user_services.registration_service import RegistrationService
from backend.schema.user import UserCreate

@pytest.fixture(scope="function")
def unique_user() -> UserCreate:
    person = random_person()
    return UserCreate(
        email=person['email'],
        username=f"{person['first_name']}-{person['last_name']}-{randomword(8)}",
        password=randomword(256, 8)
    ) 

@pytest.fixture(scope="module")
def registration_service(database: AllRepositories) -> RegistrationService:
    return RegistrationService(db=database)