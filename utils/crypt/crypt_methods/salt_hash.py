import bcrypt




def get_salt_hash(
        string_password: str,
        rounds: int=16
    ) -> bytes:

    salt = bcrypt.gensalt(rounds=rounds)
    return bcrypt.hashpw(string_password.encode("utf-8"), salt)


def is_same_password(
            hashed_password,
            input_password,
    ) -> bool:

    return bcrypt.checkpw(input_password.encode("utf-8"), hashed_password)



# [3*] Функции хеширования с солями (bcrypt python library),
#      чтобы хранить захешированными пароли в базе данных (в User.py (DB_MODEL))
