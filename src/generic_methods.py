from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify(user_password: str,actual_password: str) -> bool:
    return pwd_context.verify(user_password,actual_password)