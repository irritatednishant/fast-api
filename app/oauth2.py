from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import schemas , database , models
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends , HTTPException, status
from sqlalchemy.orm import Session
#Secret key
#Algorithm 
#Expiration time

oauth2_schemes = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "secret_key99584125"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME = 60       #minutes

def create_access_token(data: dict):
    to_encoded = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME) 
    to_encoded.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encoded,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token :str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id : str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data
    
def get_current_user(token: str = Depends(oauth2_schemes),db : Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials!", headers={"WWW-Authenticate" : "Bearer"})
    token = verify_access_token(token , credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
