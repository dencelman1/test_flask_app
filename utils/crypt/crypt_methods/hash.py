import hashlib



def get_hash(message:str ) -> str:

    if type(message) != type(""):
        message = str(message)

    hash_object = hashlib.sha512()
    hash_object.update(message.encode())
    hash_str = hash_object.hexdigest()
    
    return hash_str



# [2] Функции хеширования данных, чтобы передавать по сети захешированые после шифрования данные
#     (1 Шифрование + 2 Хеширование = Для проверки целостности данных)
