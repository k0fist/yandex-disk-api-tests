import uuid
from jsonschema import validate, FormatChecker
from json_schema.copy_file_schema import copy_file_schema


def test_copy_file(api_client, temp_file):
    file_name, local_file = temp_file
    copied_file_name = f"copy_{file_name}"

    source_remote_path = f"disk:/{file_name}"
    copied_remote_path = f"disk:/{copied_file_name}"

    try:
        upload_resp = api_client.upload_file(
            local_path=str(local_file),
            remote_path=source_remote_path,
            overwrite=True,
        )
        assert upload_resp.status_code == 201

        copy_resp = api_client.copy_file(
            from_path=source_remote_path,
            to_path=copied_remote_path,
            overwrite=True,
        )
        assert copy_resp.status_code == 201

        meta_resp = api_client.get_resource(copied_remote_path)
        assert meta_resp.status_code == 200
        assert meta_resp.json()["path"] == copied_remote_path

        validate(
            instance=copy_resp.json(),
            schema=copy_file_schema,
            format_checker=FormatChecker(),
        )

    finally:
        api_client.delete_resource(source_remote_path)
        api_client.delete_resource(copied_remote_path)


def test_copy_nonexistent_file_returns_404(api_client):
    source_remote_path = f"disk:/missing_{uuid.uuid4().hex}.txt"
    copied_remote_path = f"disk:/copy_missing_{uuid.uuid4().hex}.txt"

    resp = api_client.copy_file(
        from_path=source_remote_path,
        to_path=copied_remote_path,
        overwrite=True,
    )

    assert resp.status_code == 404