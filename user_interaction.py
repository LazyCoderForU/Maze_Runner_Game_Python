from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# Example endpoint for user registration
@app.post("/register")
async def register_user(request: Request):
    data = await request.json()
    return JSONResponse({"status": "User registered", "username": data.get("username")})

# Example endpoint for user login
@app.post("/login")
async def login_user(request: Request):
    data = await request.json()
    return JSONResponse({"status": "User logged in", "username": data.get("username")})