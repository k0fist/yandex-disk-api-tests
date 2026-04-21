from jsonschema import validate, FormatChecker
from json_schema.disk_information_schema import disk_information_schema

def test_base_url_available(api_client):
    resp = api_client.get_root()
    
    
    assert resp.status_code == 200

    body = resp.json()
    assert body["used_space"] <= body["total_space"]

    validate(
        instance=resp.json(),
        schema=disk_information_schema,
        format_checker=FormatChecker()
    )


