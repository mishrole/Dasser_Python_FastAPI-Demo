# main.py

# Python
from typing import Optional, List, Dict

# Pydantic
from pydantic import BaseModel

# Import Module
from fastapi import FastAPI, Body, Query
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
  users.append(user)
  return user

# Query Params (Validations)
@app.get("/users/search")
def search_users(
  fullname: Optional[str] = Query(None, min_length=1, max_length=50, title="Full Name of the user", description="First name and Last name of the user"), 
  age: int = Query(..., gt=0, lt=100, description="Age of the user") # ! (...) is Required (to test)
):
  return { fullname: age}

# Run (with hot reloading)
# uvicorn main:app --reload
