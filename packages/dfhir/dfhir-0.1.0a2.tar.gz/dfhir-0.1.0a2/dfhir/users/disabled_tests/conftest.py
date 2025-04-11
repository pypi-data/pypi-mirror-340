"""Pytest configuration for the dfhir app."""

import pytest

from dfhir.users.models import User
from dfhir.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    """Set the media root to a temporary directory."""
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture()
def user(db) -> User:
    """Return a user instance."""
    return UserFactory()
