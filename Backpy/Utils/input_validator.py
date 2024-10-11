from flask import abort

def validate_input(data, required_fields):
    for field in required_fields:
        if field not in data:
            abort(400, f"Missing required field: {field}")
            