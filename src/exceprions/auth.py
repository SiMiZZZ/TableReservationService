from fastapi import HTTPException


unauthorized_exc = HTTPException(status_code=401, detail="invalid email or password")

