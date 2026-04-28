import pytest
import responses
from responses import matchers

from src.api_client import ApiClient, ApiConfig


@pytest.fixture
def fake_api_client(base_url):
    config = ApiConfig(
        base_url=base_url,
        token="fake-token",
    )
    return ApiClient(config=config)


def test_client_sets_auth_headers(fake_api_client):
    assert fake_api_client.session.headers["Authorization"] == "OAuth fake-token"
    assert fake_api_client.session.headers["Accept"] == "application/json"


def test_url_builds_correctly(fake_api_client):
    assert (
        fake_api_client._url("resources/upload")
        == "https://cloud-api.yandex.net/v1/disk/resources/upload"
    )


@responses.activate
def test_get_upload_link_sends_correct_request(fake_api_client):
    responses.add(
        responses.GET,
        fake_api_client._url("resources/upload"),
        json={
            "operation_id": "123",
            "href": "https://example.com/upload",
            "method": "PUT",
            "templated": False,
        },
        status=200,
        match=[
            matchers.query_param_matcher({
                "path": "disk:/test.txt",
                "overwrite": "true",
            }),
            matchers.header_matcher({
                "Authorization": "OAuth fake-token",
                "Accept": "application/json",
            }),
        ],
    )

    resp = fake_api_client.get_upload_link(
        remote_path="disk:/test.txt",
        overwrite=True,
    )

    assert resp.status_code == 200
    assert resp.json()["method"] == "PUT"
    assert len(responses.calls) == 1