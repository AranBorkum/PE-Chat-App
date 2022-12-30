from dotenv import dotenv_values


def get_values(env_filename: str) -> dict:
    return dotenv_values(env_filename)
