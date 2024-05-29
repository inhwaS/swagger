## Overview of project
This project is designed to practice using Swagger with FastAPI. To facilitate better API communication, I have implemented JWT authentication with mock data.

## How to run the project
Run FastAPI and Vue project

![Picture1](https://github.com/inhwaS/swagger/assets/66104189/fedaf59a-fa6b-41d3-9439-30fedaba6480)

The web automatically redirects to login page

![2](https://github.com/inhwaS/swagger/assets/66104189/841bc980-d094-4324-a2bb-eb230da05f46)

Successfully log in with Token

![3](https://github.com/inhwaS/swagger/assets/66104189/e0ea2345-9689-411e-8ab1-acf2346eaf56)

When successfully log in, response contains token

![4](https://github.com/inhwaS/swagger/assets/66104189/8cb839da-3825-491e-9f5e-d272ea88769b)

Then, next request also contains token in the header

![5](https://github.com/inhwaS/swagger/assets/66104189/dabb4989-b3ea-40ed-864b-b5f6e595e4ed)

## Code details
FastAPI implementation - `main.py`
```
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
```

Create Token when user login in
```
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
```

Whenever user login, verify user with token
```
@app.get("/users/me", response_model=UserInResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    # Assuming `current_user` is a dict or model you can update/transform
    user_response = UserInResponse(
        username=current_user.username,
        current_time=datetime.now()  # Populate current time
    )
    return user_response
```

## Swagger
General view

![222](https://github.com/inhwaS/swagger/assets/66104189/db8e5502-6e43-4a26-a7ad-0daf0ca1cdda)
 
Detailed API explanation

![444](https://github.com/inhwaS/swagger/assets/66104189/e66e6d23-a4fd-4e2a-8f6d-fc3981161a00)

![555](https://github.com/inhwaS/swagger/assets/66104189/93117f18-4ab0-4726-a5d5-b9a569db1072)

