# main.py

# Python
from typing import Optional, List, Dict

# Pydantic
from pydantic import BaseModel

# Import Module
from fastapi import FastAPI, Body
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

# Instance of FastAPI
app = FastAPI()

# TODO: Move to /models
# Models

class User(BaseModel):
  first_name: str
  last_name: str
  age: int
  title: str
  # is_married: bool
  is_married : Optional[bool] = None

users = []

@app.get("/") # Path
def home():
  return RedirectResponse(url="/greetings", status_code=HTTP_303_SEE_OTHER)

@app.get("/greetings") # Path
def greetings():
  return {
    "greetings": "Hello World"
  }

@app.get("/greetings/{name}") # Path param
def greetings_name(name: str):
  greeting = "Hello %s" % (name)
  return {
    "greetings": greeting
  }

@app.get("/greetings/{name}/repeat")
def greetings_name_repeat(name: str, repeat: int = 1):
  repeated = ("Hello %s " % (name)) * repeat
  return {
    "greetings": repeated.rstrip()
  }

@app.get("/users")
def list_users():
  return {
    "users": users
  }

@app.post("/users")
def create_user(user: User = Body(...)): # ! with Body(...) model is Required
  return user

# Run (with hot reloading)
# uvicorn main:app --reload
