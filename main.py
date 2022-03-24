# main.py
# Import Module
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

# Instance of FastAPI
app = FastAPI()

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

# Run (with hot reloading)
# uvicorn main:app --reload
