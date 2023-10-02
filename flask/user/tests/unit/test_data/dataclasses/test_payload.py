from datetime import datetime


def generate_valid_data() -> dict:
    return {
        "id": "sdafdsafa",
        "session_id": "sdfadsf",
        "is_admin": True,
        "is_refresh": True,
        "exp": datetime.now(),
        "token": "dfgafhnj4154325423lj",
    }


def generate_none_id_data() -> dict:
    return {
        "id": None,
        "session_id": "sdfadsf",
        "is_admin": True,
        "is_refresh": True,
        "exp": datetime.now(),
        "token": "dfgafhnj4154325423lj",
    }


def generate_none_session_id_data() -> dict:
    return {
        "id": "sdafdsafa",
        "session_id": None,
        "is_admin": True,
        "is_refresh": True,
        "exp": datetime.now(),
        "token": "dfgafhnj4154325423lj",
    }


def generate_none_is_admin_data() -> dict:
    return {
        "id": "sdafdsafa",
        "session_id": "sdfadsf",
        "is_admin": None,
        "is_refresh": True,
        "exp": datetime.now(),
        "token": "dfgafhnj4154325423lj",
    }


def generate_none_is_refresh_data() -> dict:
    return {
        "id": "sdafdsafa",
        "session_id": "sdfadsf",
        "is_admin": True,
        "is_refresh": None,
        "exp": datetime.now(),
        "token": "dfgafhnj4154325423lj",
    }


def generate_none_exp_data() -> dict:
    return {
        "id": "sdafdsafa",
        "session_id": "sdfadsf",
        "is_admin": True,
        "is_refresh": True,
        "exp": None,
        "token": "dfgafhnj4154325423lj",
    }


def generate_none_token_data() -> dict:
    return {
        "id": "sdafdsafa",
        "session_id": "sdfadsf",
        "is_admin": True,
        "is_refresh": True,
        "exp": datetime.now(),
        "token": None,
    }
