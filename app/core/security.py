from passlib.context import CryptContext

# contextul de criptare — folosește bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Primește parola în clar și returnează hash-ul acesteia.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifică dacă parola introdusă (în clar) corespunde hash-ului din DB.
    """
    return pwd_context.verify(plain_password, hashed_password)
