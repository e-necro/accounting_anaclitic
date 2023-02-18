from fastapi import FastAPI, Request, Response, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from mysql.connector import Error

from .MysqlConnect import MysqlConnect

from .lib.checker import  *
from .lib.user import UserReg, UserLogin
from .lib.token import *


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


@app.post("/login", status_code = 200)
async def login(userData: UserLogin, response: Response):
  try:
    userData.user["token"] = create_access_token(userData)

    connection = MysqlConnect.connectDb()  
    mycursor = connection.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM users WHERE email = %s AND password = %s ", (userData.user['email'],userData.user['password']) )
    res = mycursor.fetchall()
    if (len(res) == 0):
      return RequestError(response, {'MySQL', 'Wrong email/password?'}, 401)

    del(userData.user['password'])
    return userData

  except Error as e:
        response.status_code = 419  # вывод ошибок, точнее формат сделать нормальным! 
        errors = { 'errors': {
            'MySQL': e #  выдает Object object ... wtf?
          }
        }
        return errors
