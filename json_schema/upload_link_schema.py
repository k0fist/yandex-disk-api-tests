upload_link_schema = {
    "type": "object",
    "properties": {
        "operation_id": {"type": "string"},
        "href": {
            "type": "string",
            "format": "uri"
        },
        "method": {
            "type": "string",
            "enum": ["PUT"]
        },
        "templated": {"type": "boolean"},
    },
    "required": [
        "operation_id",
        "href",
        "method",
        "templated",
    ],
    "additionalProperties": True,
}