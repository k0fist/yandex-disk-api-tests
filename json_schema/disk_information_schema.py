disk_information_schema = {
    "type": "object",
    "properties": {
        "total_space": {"type": "integer"},
        "used_space": {"type": "integer"},
        "trash_size": {"type": "integer"},
        "is_paid": {"type": "boolean"},
        "revision": {"type": "integer"},
        "user": {
            "type": "object",
            "properties": {
                "uid": {"type": "string"},
                "login": {"type": "string"},
                "display_name": {"type": "string"},
                "country": {"type": "string"},
                "is_child": {"type": "boolean"},
                "reg_time": {
                    "type": "string",
                    "format": "date-time"
                }
            },
            "required": ["uid", "login", "display_name", "country", "is_child", "reg_time"],
            "additionalProperties": True
        }
    },
    "required": [
        "total_space",
        "used_space",
        "trash_size",
        "is_paid",
        "revision",
        "user"
    ],
    "additionalProperties": True
}