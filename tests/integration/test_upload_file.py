import uuid
from jsonschema import validate, FormatChecker
from json_schema.upload_link_schema import upload_link_schema


def test_get_upload_link(api_client):
    remote_path = f"disk:/test_{uuid.uuid4().hex}.txt"

    resp = api_client.get_upload_link(remote_path=remote_path)

    assert resp.status_code == 200

    validate(
        instance=resp.json(),
        schema=upload_link_schema,
        format_checker=FormatChecker(),
    )


def test_uploaded_file_exists(api_client, temp_file):
    file_name, local_file = temp_file

    remote_path = f"disk:/{file_name}"

    try:
        resp = api_client.upload_file(
            local_path=str(local_file),
            remote_path=remote_path,
            overwrite=True,
        )

        assert resp.status_code == 201

        meta_resp = api_client.get_resource(remote_path)
        assert meta_resp.status_code == 200

        body = meta_resp.json()
        assert body["name"] == file_name
        assert body["path"] == remote_path
        assert body["type"] == "file"
    finally:
        api_client.delete_resource(remote_path)


def test_get_upload_link_without_path_returns_400(api_client):
    resp = api_client.get_upload_link_without_params()

    assert resp.status_code == 400


def test_get_upload_link_for_existing_file_without_overwrite_returns_error(api_client, temp_file):
    file_name, local_file = temp_file
    remote_path = f"disk:/{file_name}"

    try:
        first_upload_resp = api_client.upload_file(
            local_path=str(local_file),
            remote_path=remote_path,
            overwrite=True,
        )
        assert first_upload_resp.status_code == 201

        link_resp = api_client.get_upload_link(
            remote_path=remote_path,
            overwrite=False,
        )

        assert link_resp.status_code in (409, 412)

    finally:
        api_client.delete_resource(remote_path)