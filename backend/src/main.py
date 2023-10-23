from fastapi import FastAPI, Request, Response, status, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import json
from mysql.connector import Error
from typing import Union

from .MysqlConnect import MysqlConnect

from .lib.checker import  *
from .lib.baseClasses import UserReg, UserLogin, UserCheck, AddAuto, DeleteAuto
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


@app.get("/user", status_code = 200)
async def user(response: Response, Authorization: Union[str, None] = Header(default=None)):
  try:
    token = Authorization[6:]
    if (verify_token(token)):
      # токен верный, достанем юзера по нему
      connection = MysqlConnect.connectDb()  
      mycursor = connection.cursor(dictionary=True)
      # return "SELECT * FROM users WHERE token = '" + token + "'"
      mycursor.execute("SELECT * FROM users WHERE token = '" + token + "' AND deleted = 0")
      res = mycursor.fetchall()
      if (len(res) == 0):
        return RequestError(response, {'MySQL', 'Token error. Try to relogin'}, 401)
      
      del(res[0]['password'])
      return res

  except Error as e:
    return RequestError(response, {'MySQL', e}, 419)


@app.post("/get_my_auto", status_code = 200)
async def get_my_auto(userData: UserCheck, response: Response):
  try:
    # userData.user_id = 444 # TODO: убрать это
    if (verify_token(userData.token) & (userData.user_id != '') ):
      connection = MysqlConnect.connectDb()  
      mycursor = connection.cursor(dictionary=True)
      mycursor.execute("SELECT * FROM auto WHERE user_id = %s", (userData.user_id,))
      res = mycursor.fetchall()
      connection.close()
      return res
    else:
      return RequestError(response, {'MySQL', 'Token is obsolete'})
      
  except Error as e:
      return e
      

@app.post("/add_my_auto", status_code = 200)
async def add_my_auto(userData: AddAuto, response: Response):
  try:
    res = checkAutoData(userData)
    if (res[0] == True):
      if (verify_token(userData.token) & (userData.user_id != '') ):
        connection = MysqlConnect.connectDb()  
        mycursor = connection.cursor(dictionary=True)
        mycursor.execute("INSERT INTO auto (name, comment, date_create, user_id) VALUES ( %s, %s, %s, %s) ", ( userData.name, userData.comment, userData.date, userData.user_id))
        connection.commit()
        _id = mycursor.lastrowid
        connection.close()
        return {'_id': _id}
      else:
        return RequestError(response, {'MySQL', 'Token is obsolete'})
      
  except Error as e:
      return e
      

@app.post("/delete_my_auto", status_code = 200)
async def delete_my_auto(userData: DeleteAuto, response: Response):
  try:
    if (verify_token(userData.token) & (userData.user_id != '' & (userData._id !='')) ):
      return False
      # TODO: посмотреть как добавляются внешние ключи и как их проверять(точнее что именно отдается если не даст удалить). Сравнивать, думаю, с  auto_cat айдишниками
      # TODO 2: связь есть. Изучть как в мускуле с коммитом и отменой его проходят. Потом выяснить как питон с этим работает. Удалить с добавленным ремонтом, посмотреть что будет без проверок вручную
      # connection = MysqlConnect.connectDb()  
      # mycursor = connection.cursor(dictionary=True)
      # mycursor.execute("DELETE FROM auto WHERE id=%s",(userData._id))
      # connection.commit()
      # _id = mycursor.lastrowid
      # connection.close()
      # return {'_id': _id}
    # else:
    #   return RequestError(response, {'MySQL', 'Token is obsolete'})
      
  except Error as e:
      return e