from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _truncate_to_72_bytes(password: str) -> bytes:
    """Encode to UTF-8 and truncate to 72 bytes (bcrypt limit).

    Truncating by characters can still exceed 72 bytes when using
    multi-byte Unicode characters, so we truncate the encoded bytes.
    """
    return password.encode("utf-8")[:72]

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def _truncate_to_72_str(password: str) -> str:
    """Return a UTF-8 string whose encoded form is at most 72 bytes.

    We encode then trim bytes and decode with 'ignore' to avoid
    partial multi-byte characters; this guarantees that when
    passlib re-encodes the string it will be <=72 bytes.
    """
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
