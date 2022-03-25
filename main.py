# main.py

# Python
from typing import Optional, List, Dict

# Pydantic
from pydantic import BaseModel

# Import Module
from fastapi import FastAPI, Body, Path, Query
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

import uuid

# Instance of FastAPI
app = FastAPI()

# TODO: Move to /models
# Models

class User(BaseModel):
  id : Optional[str] = uuid.uuid4()
  first_name: str
  last_name: str
  age: int
  title: str
  # is_married: bool
  is_married : Optional[bool] = None

users = []

@app.get("/") # Path
def home():
  return RedirectResponse(
    url="/greetings",
    status_code=HTTP_303_SEE_OTHER
  )

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
def greetings_name_repeat(
  name: str,
  repeat: int = 1
):
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
# * If two endpoints have the same path and query params, the first one will be used
@app.get("/users/search")
def search_users(
  fullname: Optional[str] = Query(
    None,
    min_length = 1,
    max_length = 50,
    title = "Full Name of the user",
    description = "This is the First name and Last name of the user. It's between 1 and 50 characters"
  ), 
  age: int = Query(
    ...,
    gt = 0,
    lt = 100,
    title = "Age of the user", # * Unsupported on Swagger UI, but works on Redoc
    description = "This is the age of the user. It's required"
  ) # ! (...) is Required (to test)
):
  return { fullname: age }

# Path Params (Validations)
@app.get("/users/{user_id}")
def get_user(
  user_id: str = Path(
    ...,
    title = "ID of the user",
    description = "This is the ID of the user. It's required"
  )
):
  return {
    "user": next((user for user in users if user.id == user_id), None)
  }

# Run (with hot reloading)
# uvicorn main:app --reload
