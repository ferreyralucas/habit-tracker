from shutil import rmtree

from django.conf import settings

import pytest
from fakeredis import FakeStrictRedis
from pytest_django.fixtures import _set_suffix_to_test_databases
from pytest_django.lazy_django import skip_if_no_django


@pytest.fixture(scope='session', autouse=True)
def remove_media_created_in_tests():
    yield
    rmtree(settings.MEDIA_ROOT, ignore_errors=True)


@pytest.fixture(autouse=True)
def patch_redis(monkeypatch):
    monkeypatch.setattr('core.redis_manager.redis_client', FakeStrictRedis())


@pytest.fixture(scope="session")
def django_db_modify_db_settings_xdist_suffix(request):
    skip_if_no_django()

    xdist_suffix = getattr(request.config, "workerinput", {}).get("workerid")
    if xdist_suffix:
        # Put a suffix like _gw0, _gw1 etc on xdist processes
        _set_suffix_to_test_databases(suffix=xdist_suffix)
