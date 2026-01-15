from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _truncate_to_72_bytes(password: str) -> bytes:
    return password.encode("utf-8")[:72]

def _truncate_to_72_str(password: str) -> str:
    return _truncate_to_72_bytes(password).decode("utf-8", "ignore")

def hash_password(password: str) -> str:
    try:
        pw_safe = _truncate_to_72_str(password)
        return pwd_context.hash(pw_safe)
    except Exception as e:
        raise ValueError("Error hashing password") from e

def verify_password(password: str, hashed_password: str) -> bool:
    pw_safe = _truncate_to_72_str(password)
    return pwd_context.verify(pw_safe, hashed_password)
