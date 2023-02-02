from typing import Dict

from fastapi import FastAPI, Request, Response, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from jose import JWTError, jwt
from pydantic import BaseModel
from datetime import datetime, timedelta
from mysql.connector import Error

from .MysqlConnect import MysqlConnect

from .lib.checker import  *


SECRET_KEY = '3b5fa82a13bdb6c1ed725fcb9e3d20123c48d4889ec41139bcfe3e766c78a5c1'
ALGORITHM = "HS256"
class Token(BaseModel):
    access_token: str
    token_type: str

class UserReg(BaseModel):
  '''
    {
      email,
      username,
      password
    }
  '''
  user: Dict

class UserLogin(BaseModel):
  '''
    {
      username,
      password
    }
  '''
  user: Dict

def create_access_token(userData):
    to_encode = {
        'username': userData.user['username'],
        'password': userData.user['password']
    }
     
    # expire time of the token
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
     
    return encoded_jwt




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

@app.post("/register", status_code = 200)
async def register(userData: UserReg, response: Response):
  # TODO: сгенерить токен, добавить юзера и токен к нему, вернуть данные
  res = checkRegister(userData)
  if (res[0] == True):
    #зарегать юзера и вернуть данные и токен
    try:
      connection = MysqlConnect.connectDb()  
      mycursor = connection.cursor(dictionary=True)
      mycursor.execute("SELECT _id FROM users WHERE email = %s", (userData.user['email'],) )
      res = mycursor.fetchall()
      if (len(res) != 0):
        return RequestError(response, {'MySQL', 'User already registered'})

      userData.user["token"] = create_access_token(userData)
      mycursor.execute(
        'INSERT INTO users (name, email, password, token) VALUES (%s, %s, %s, %s)',
        (userData.user['username'], userData.user['email'], userData.user['password'], userData.user['token'])
      )
      connection.commit()
      _id = mycursor.lastrowid
      connection.close()
      userData.user['_id'] = _id
      del userData.user['password']
      
      return userData
        
    except Error as e:
        response.status_code = 419  # вывод ошибок, точнее формат сделать нормальным! 
        errors = { 'errors': {
            'MySQL': e #  выдает Object object ... wtf?
          }
        }
        return errors

  else:
    # ошибочка
    return RequestError(response, res[1])
    # response.status_code = 419  # вывод ошибок, точнее формат сделать нормальным! 
    # errors = { 'errors': {
    #     res[1]
    #   }
    # }
    # return errors
  #request: Request
  # request.data.user.token = 'token example'

    
  # return await request.json()