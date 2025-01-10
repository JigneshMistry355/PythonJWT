from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from pydantic import BaseModel
from passlib.context import CryptContext 

app = FastAPI()

# URL of users browser is stored in tokenURL
# This parameter declares that the URL /token will be the one that the client should use to get the token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

class User(BaseModel):
    username : str
    email : str | None = None
    full_name : str | None = None
    disabled : bool | None = None

class UserInDB(User):
    hashed_password : str

pwd_context = CryptContext(schemes=["bcrypt"], depricated="auto")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

def fake_decode_token(token):
    return User(
        username = token + "fakedecoded",
        email = 'abc@example.com',
        full_name = 'Jignesh Mistry'
    )

def fake_hashed_password(password : str):
    return "fakehashed" + password

# get_current_user will receive a token as a str from the sub-dependency oauth2_scheme
async def get_current_user(token : Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    return user

async def get_current_active_user(current_user : Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.get("/users/me")
async def read_users_me(current_user : Annotated[str, Depends(get_current_active_user)]):
    return current_user 

# OAuth2PasswordRequestForm is a class dependency that declares a form body with:
    # The username.
    # The password.
    # An optional scope field as a big string, composed of strings separated by spaces.
    # An optional grant_type.

@app.post("/token")
async def login(form_data : Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hashed_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return {"access token": user.username, 'token_type': 'bearer'}

