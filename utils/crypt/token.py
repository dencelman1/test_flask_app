from crypt_methods.symmetric_encryption import get_crypt_data, get_decrypt_data
import json



def get_data_token(**kwargs) -> list:

    """[1 data_token, 2 key]"""
    
    kwargs = dict(kwargs)
    token_string = json.dumps(kwargs)
    token, key = get_crypt_data(token_string) # session_token, key

    return [token, key]


def get_token_data(token: str, key: str) -> list:

    """{*kwargs}"""
    
    decrypted_string = get_decrypt_data(key, token)
    kwargs = json.loads(decrypted_string)

    return kwargs

