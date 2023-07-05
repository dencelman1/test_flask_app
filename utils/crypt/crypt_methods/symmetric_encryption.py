from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os




def get_crypt_data(message: str) -> bytes:
    """:return: crypted_byted_data"""
    
    load_dotenv()
    
    key = os.getenv("SECRET_KEY")
    cipher_suite = Fernet(key)

    return cipher_suite.encrypt(message.encode())


def get_decrypt_data(crypted_message: str) -> str:
    """:return: decrypted_str_data"""

    load_dotenv()
    key = os.getenv("SECRET_KEY")
    cipher_suite = Fernet(key)

    return cipher_suite.decrypt(crypted_message).decode("utf-8")



# [1] Функции симметричного (шифрования и расшифрования)
#     для шифрований данных чтобы хранить их в базе данных
