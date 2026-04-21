copy_file_schema = {
    "type": "object",
    "properties": {
        "href": {
            "type": "string",
            "format": "uri"
        },
        "method": {
            "type": "string",
            "enum": ["GET"]
        },
        "templated": {"type": "boolean"},
    },
    "required": [
        "href",
        "method",
        "templated",
    ],
    "additionalProperties": True,
}