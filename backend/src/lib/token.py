from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt

#https://www.geeksforgeeks.org/how-to-generate-jwt-tokens-using-fastapi-in-python/
SECRET_KEY = '3b5fa82a13bdb6c1ed725fcb9e3d20123c48d4889ec41139bcfe3e766c78a5c1'
ALGORITHM = "HS256"
class Token(BaseModel):
    access_token: str
    token_type: str



def create_access_token(userData):
    to_encode = {
        'email': userData.user['email'],
        'password': userData.user['password']
    }
     
    # expire time of the token
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
     
    return encoded_jwt

# проверить еще
def verify_token(token: str):
    try:
        # try to decode the token, it will
        # raise error if the token is not correct
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
