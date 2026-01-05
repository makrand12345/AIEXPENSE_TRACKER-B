from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _truncate_to_72_bytes(password: str) -> bytes:
    """Encode to UTF-8 and truncate to 72 bytes (bcrypt limit).

    Truncating by characters can still exceed 72 bytes when using
    multi-byte Unicode characters, so we truncate the encoded bytes.
    """
    return password.encode("utf-8")[:72]

def hash_password(password: str) -> str:
    pw_bytes = _truncate_to_72_bytes(password)
    return pwd_context.hash(pw_bytes)

def verify_password(password: str, hashed_password: str) -> bool:
    pw_bytes = _truncate_to_72_bytes(password)
    return pwd_context.verify(pw_bytes, hashed_password)
