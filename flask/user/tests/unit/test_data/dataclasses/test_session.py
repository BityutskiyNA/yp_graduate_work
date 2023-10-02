def generate_valid_data() -> dict:
    return {"user_id": "user_id", "user_agent": "user_agent"}


def generate_none_user_id_data() -> dict:
    return {"user_id": None, "user_agent": "user_agent"}


def generate_none_user_agent_data() -> dict:
    return {"user_id": "user_id", "user_agent": None}
