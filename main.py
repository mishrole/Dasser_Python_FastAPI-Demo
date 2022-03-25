# main.py

# Python
from typing import Optional, List, Dict
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field, EmailStr, HttpUrl

# Import Module
from fastapi import FastAPI, Body, Path, Query
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

import uuid

# Instance of FastAPI
app = FastAPI()

# TODO: Move to /models
# Models

class HairColor(Enum):
  white = "white"
  black = "black"
  brown = "brown"
  blonde = "blonde"
  red = "red"
  gray = "gray"

class Location(BaseModel):
  city: str = Field(
    ...,
    min_length = 2,
    title = "City",
    example = "Lima"
  )
  state: str = Field(
    ...,
    min_length = 2,
    title = "State",
    example = "Lima"
  )
  country: str = Field(
    ...,
    min_length = 2,
    title = "Country",
    example = "Peru"
  )

  # class Config:
  #   schema_extra = {
  #     "example": {
  #       "city": "New York",
  #       "state": "NY",
  #       "country": "USA"
  #     }
  #   }

class User(BaseModel):
  id : Optional[str] = uuid.uuid4()
  first_name: str = Field(
    ...,
    min_length = 1,
    max_length = 50,
    title="First Name"
  )
  last_name: str = Field(
    ...,
    min_length = 1,
    max_length = 50,
    title="Last Name"
  )
  age: int = Field(
    ...,
    gt = 0,
    le = 150,
    title="Age"
  )
  title: str = Field(
    ...,
    min_length = 1,
    max_length = 50,
    title="Job Title"
  )
  hair_color: Optional[HairColor] = Field(default = None)
  is_married : Optional[bool] = Field(default = None)
  site_url: HttpUrl = Field(default = None)
  email: EmailStr = Field(default = None)

  class Config:
    schema_extra = {
      "example": {
        "first_name": "Mitchell",
        "last_name": "Rodríguez",
        "age": 25,
        "title": "Full-Stack Developer",
        "hair_color": "black",
        "is_married": False,
        "site_url": "https://www.linkedin.com/in/mitchellrodriguez",
        "email": "mishrole.dev@gmail.com"
      }
    }

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
def greetings_name(name: str = Path(..., title="Name", example="Mitchell")):
  greeting = "Hello %s" % (name)
  return {
    "greetings": greeting
  }

@app.get("/greetings/{name}/repeat")
def greetings_name_repeat(
  name: str = Path(..., title="Name", example="Mitchell"),
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
    description = "This is the First name and Last name of the user. It's between 1 and 50 characters",
    example = "Mitchell Rodriguez"
  ), 
  age: int = Query(
    ...,
    gt = 0,
    lt = 100,
    title = "Age of the user", # * Unsupported on Swagger UI, but works on Redoc
    description = "This is the age of the user. It's required",
    example = 25
  ) # ! (...) is Required (to test)
):
  return { fullname: age }

# Path Params (Validations)
@app.get("/users/{user_id}")
def get_user(
  user_id: str = Path(
    ...,
    title = "ID of the user (UUID)",
    description = "This is the ID of the user. It's required",
    example = "5e9f8f8f-8f8f-8f8f-8f8f-8f8f8f8f8f8f"
  )
):
  return {
    "user": next((user for user in users if user.id == user_id), None)
  }

# Request Body (Validations)
@app.put("/users/{user_id}")
def update_user(
  user_id: str = Path(
    ...,
    title = "ID of the user (UUID)",
    description = "This is the user ID",
    example = "5e9f8f8f-8f8f-8f8f-8f8f-8f8f8f8f8f8f"
    # gt = 0
  ),
  user: User = Body(...),
  location: Location = Body(...)
):
  results = user.dict()
  results["location"] = location.dict()
  # * Combine
  # results.update(location.dict())
  # ! Unsupported by FastAPI
  # user.dict() & location.dict()
  return results


# Run (with hot reloading)
# uvicorn main:app --reload
