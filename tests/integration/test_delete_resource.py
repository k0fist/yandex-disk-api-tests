import uuid
import time


def test_delete_uploaded_file(api_client, temp_file):
    file_name, local_file = temp_file
    remote_path = f"disk:/{file_name}"

    try:
        upload_resp = api_client.upload_file(
            local_path=str(local_file),
            remote_path=remote_path,
            overwrite=True,
        )
        assert upload_resp.status_code == 201

        delete_resp = api_client.delete_resource(remote_path)
        assert delete_resp.status_code in (202, 204)

        for _ in range(5):
            meta_resp = api_client.get_resource(remote_path)

            if meta_resp.status_code == 404:
                break

            time.sleep(1)

        assert meta_resp.status_code == 404
    finally:
        api_client.delete_resource(remote_path)


def test_delete_nonexistent_resource_returns_404(api_client):
    remote_path = f"disk:/missing_{uuid.uuid4().hex}.txt"

    resp = api_client.delete_resource(remote_path)

    assert resp.status_code == 404