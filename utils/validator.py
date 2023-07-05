import re
from collections import namedtuple


RegexPatterns = namedtuple("RegexPatterns", ['email', 'phone'])

class Validator:

    regex = RegexPatterns(
        email=r'^[\w\.-]+@[\w\.-]+\.\w+$',
        phone=r"^\+?\d{10,20}$",
    )

    @staticmethod
    def email(email:str) -> bool:
        return re.match(Validator.regex.email, email)

    @staticmethod
    def phone(phone:str) -> bool:
        return re.match(Validator.regex.phone, phone)
