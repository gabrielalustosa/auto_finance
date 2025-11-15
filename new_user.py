import re

def senha_forte(senha):
    """Valida se a senha é forte."""
    if len(senha) < 8:
        return False
    if not re.search(r"[A-Z]", senha):
        return False
    if not re.search(r"[a-z]", senha):
        return False
    if not re.search(r"[0-9]", senha):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
        return False
    return True

def email_valido(email):
    """Valida formato básico de e-mail."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)
