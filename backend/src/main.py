from typing import Dict

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
from pydantic import BaseModel
from mysql.connector import Error

from .MysqlConnect import MysqlConnect

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# connection = MysqlConnect().connectDb

@app.get("/")
async def home():
  try:
    connection = MysqlConnect.connectDb()  
    mycursor = connection.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM auto")
    res = mycursor.fetchall()
    connection.close()
    return res
      
  except Error as e:
      return e
  # return "Hello, World!!!!"

class UserReg(BaseModel):
  user: Dict

@app.post("/register")
async def register(userData: UserReg):
  # TODO: сгенерить токен, добавить юзера и токен к нему, вернуть данные
  userData.user['_id'] = 'userId'
  userData.user["token"] = 'token example'
  return userData
  #request: Request
  # request.data.user.token = 'token example'

    
  # return await request.json()