import re
def validate_phone_number(phone_number):

    patterns = [
        r'\d{10}',
        r'\d{3}-\d{3}-\d{4}',
        r'\(\d{3}\)\s\d{3}-\d{4}'
    ]

    for pattern in patterns:
        if re.match(pattern, phone_number):
            return True
    return False