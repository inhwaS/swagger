from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

# Assuming this is your original User model
class User(BaseModel):
    username: str
    email: Optional[str] = None
    disabled: Optional[bool] = None

class UserInResponse(BaseModel):
    username: str
    email: Optional[str] = None
    current_time: datetime

# Define a secret key and algorithm for JWT
SECRET_KEY = "Secret123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# User model for demonstration
class User(BaseModel):
    username: str

# Fake database of users
fake_user = {
    "username": "myuser",
    "full_name": "My User",
    "email": "myuser@gmail.com",
    "hashed_password": "mypassword",
    "disabled": False,
}

# Utility function to verify password (fake verification for demo)
def fake_verify_password(plain_password, hashed_password):
    return plain_password == hashed_password

def authenticate_user(username: str, password: str):
    if username != fake_user["username"]:
        return False
    if not fake_verify_password(password, fake_user['hashed_password']):
        return False
    return fake_user

# Generate JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verify JWT token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    print(f"Token received: {token}")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        print(f"Payload decoded successfully: {payload}")  # Debugging line
        username: str = payload.get("sub")
        if username is None:
            print("Username is None after decoding JWT.")  # Debugging line
            raise credentials_exception
        print(f"Username extracted: {username}")  # Debugging line
        token_data = UserInResponse(username=username, current_time=datetime.now())
    except JWTError as e:
        print(f"JWTError occurred: {e}")  # Debugging line
        raise credentials_exception

    return token_data

# Endpoint to get token
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserInResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    # Assuming `current_user` is a dict or model you can update/transform
    user_response = UserInResponse(
        username=current_user.username,
        current_time=datetime.now()  # Populate current time
    )
    return user_response

# Start the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
