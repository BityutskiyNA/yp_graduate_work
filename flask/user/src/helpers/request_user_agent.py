from flask import request


def get_user_agent():
    return request.user_agent.string
