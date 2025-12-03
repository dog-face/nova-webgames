from datetime import datetime, timedelta
from typing import Optional, Union, Any
from jose import jwt
from app.core.config import settings

# Use bcrypt directly instead of passlib
# 
# Reason: There's a known compatibility issue between passlib 1.7.4 and bcrypt 5.0.0+
# where passlib's wrap bug detection code fails during initialization, even though
# bcrypt 5.0.0+ has the bug fixed. This causes a ValueError during password hashing.
#
# Using bcrypt directly is a valid approach and is actually more straightforward
# for our use case. We only need basic password hashing/verification, so we don't
# lose significant functionality by avoiding passlib's abstraction layer.
#
# Alternative solutions considered:
# - Upgrading passlib: 1.7.4 is the latest version (no fix available yet)
# - Configuring passlib to skip detection: Not easily configurable
# - Using bcrypt directly: Clean, standard, and works reliably
import bcrypt

ALGORITHM = "HS256"

def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a bcrypt hash.
    
    Uses bcrypt directly instead of passlib to avoid the wrap bug detection
    issue that occurs with passlib 1.7.4 and bcrypt 5.0.0+.
    This is a known compatibility issue where passlib's detection code fails
    even though the underlying bcrypt library is secure.
    """
    try:
        password_bytes = plain_password.encode('utf-8') if isinstance(plain_password, str) else plain_password
        hash_bytes = hashed_password.encode('utf-8') if isinstance(hashed_password, str) else hashed_password
        return bcrypt.checkpw(password_bytes, hash_bytes)
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Uses bcrypt directly with 12 rounds (industry standard).
    Returns the hash as a UTF-8 string for database storage.
    """
    password_bytes = password.encode('utf-8') if isinstance(password, str) else password
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')
