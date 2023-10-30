from dotenv import dotenv_values


def get_key(key: str, path=""):
    """Gets key from .env file"""
    paths = [
        "../.env",
        "./.env",
        "/Users/samisaf/openai.env",
        "C:/Users/samis/openai.env",
        "C:/Users/samisaf/openai.env",
    ]
    if len(path) > 0:
        return dotenv_values(path)[key]
    else:
        for p in paths:
            if len(dotenv_values(p)) > 0:
                return dotenv_values(p)[key]
    return None
