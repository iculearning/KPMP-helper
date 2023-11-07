from dotenv import dotenv_values
import os


def get_key(key: str, path=""):
    """Gets key from the environment or from a .env file"""

    # first try to get the key if saved as an environment variable
    result = os.environ.get(key)
    if result:
        return result
    # if the key is not found in the environment variables, then search for it in a .env file
    else:
        return get_key_dotenv(key)


def get_key_dotenv(key: str, path=""):
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


if __name__ == "__main__":
    r1 = get_key("PINECONE_API_KEY")
    print("Done")
