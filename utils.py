""" Re Useable / Daily : Utilites """


from email.utils import parseaddr


def check_password_strong(passwd):
    """ Checks password strength based on complexity criteria """

    error = ""
    criteria = {
        'length': len(passwd) >= 8,
        'uppercase': any(c.isupper() for c in passwd),
        'lowercase': any(c.islower() for c in passwd),
        'digit': any(c.isdigit() for c in passwd),
        'non_alphanumeric': any(not c.isalnum() for c in passwd)
    }
    missing = [key for key, value in criteria.items() if not value]
    if missing:
        error = ", ".join(missing)
    return error if error else 0


def validate_email(email):
    """ Validates email address format using the email.utils library """
    try:
        # * Attempt to parse email address (raises exception for invalid formats)
        name, addr = parseaddr(email)
        return '@' in addr and len(addr.split('@')) == 2
    except (ValueError, TypeError):
        return False


if __name__ == '__main__':
    pass
