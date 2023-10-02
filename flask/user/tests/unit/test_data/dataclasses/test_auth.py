def generate_valid_data() -> dict:
    return {"login": "test", "password": "test"}


def generate_none_login_data() -> dict:
    return {"login": None, "password": "test"}


def generate_none_password_data() -> dict:
    return {"login": "test", "password": None}


def generate_blank_password_data() -> dict:
    return {"login": "test", "password": ""}


def generate_blank_login_data() -> dict:
    return {"login": "", "password": "test"}
