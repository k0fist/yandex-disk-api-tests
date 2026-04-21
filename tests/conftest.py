import os
import uuid

import pytest
from dotenv import load_dotenv
import requests

from src.api_client import ApiClient, ApiConfig


load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    base_url = os.getenv("BASE_URL")
    if not base_url:
        raise ValueError("Переменная окружения BASE_URL не задана")
    return base_url


@pytest.fixture(scope="session")
def http_session():
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture(scope="session")
def api_client(base_url, http_session):
    token = os.getenv("YANDEX_DISK_TOKEN")
    if not token:
        raise ValueError("Переменная окружения YANDEX_DISK_TOKEN не задана")
    config = ApiConfig(
        base_url=base_url,
        token=token,
    )
    return ApiClient(config=config, session=http_session)


@pytest.fixture
def temp_file(tmp_path):
    file_name = f"test_{uuid.uuid4().hex}.txt"
    local_file = tmp_path / file_name
    local_file.write_text("hello yandex disk", encoding="utf-8")
    return file_name, local_file
