from datetime import datetime
from fastapi import Request
from dotenv import load_dotenv
import os
import json

from functions.crypt.crypt_methods.symmetric_encryption import get_crypt_data, get_decrypt_data



def get_session_token(
        request: Request,

        login_type: str,
        login_value: str,
        password: str,
        registration_date: str
    ) -> bytes:
    """1 session_token"""
    
    load_dotenv()

    if login_type not in ["email", "phone_number", "name"]:
        raise ValueError("login_type must equal 'email' or 'phone_number' in args of get_session_token()")

    token_data = {
        "host_ip": str(request.client.host),
        "user_agent": str(request.headers.get("User-Agent")),
        "registration_date": str(registration_date),
        "timestamp": datetime.now().timestamp(),
        
        "login_type": login_type, # "email" or "phone_number"
        "login_value": login_value,
        "password": password,
    }
    token_string = json.dumps(token_data)
    session_token = get_crypt_data(token_string) # session_token, key

    return session_token


def get_session_data(session_token: str) -> dict:
    
    token_string = get_decrypt_data(session_token)
    session_data = json.loads(token_string)

    return session_data
