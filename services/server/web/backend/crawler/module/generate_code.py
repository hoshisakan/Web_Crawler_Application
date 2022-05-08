import secrets
import string

def createRandomCode():
    alphabet = string.ascii_letters + string.digits

    while True:
        code = ''.join(secrets.choice(alphabet) for i in range(6))
        if (any(c.islower() for c in code)
                and sum(c.isupper() for c in code) > 1
                and sum(c.isdigit() for c in code) > 1):
            break
    return code
