from fastapi import APIRouter, FastAPI, Request, Response, status, HTTPException, Header

from ..lib.checker import  *
from ..lib.baseClasses import UserReg, UserLogin, UserCheck, AddAuto, DeleteAuto, UpdateAuto
from ..lib.token import *

from mysql.connector import Error
from ..MysqlConnect import MysqlConnect




router = APIRouter()

@router.post("/get_my_auto", status_code = 200)
async def get_my_auto(userData: UserCheck, response: Response):
  try:
    if (verify_token(userData.token) & (userData.user_id != '') ):
      connection = MysqlConnect.connectDb()  
      mycursor = connection.cursor(dictionary=True)
      if (userData.auto_id !=''):
        mycursor.execute("SELECT * FROM auto WHERE user_id = %s AND _id = %s", (userData.user_id, userData.auto_id,))  
      else:  
        mycursor.execute("SELECT * FROM auto WHERE user_id = %s", (userData.user_id,))
      res = mycursor.fetchall()
      connection.close()
      return res
    else:
      return RequestError(response, {'MySQL', 'Token is obsolete'})
      
  except Error as e:
      connection.close()
      return e


@router.post("/add_my_auto", status_code = 200)
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
      connection.rollback()
      connection.close()
      return RequestError(response, {'error', e})
      

@router.post("/delete_my_auto", status_code = 200)
async def delete_my_auto(userData: DeleteAuto, response: Response):
  try:
    if (verify_token(userData.token) & (userData.user_id != '') & (userData.id !='') ):
      connection = MysqlConnect.connectDb()  
      mycursor = connection.cursor(dictionary=True)
      mycursor.execute("SELECT _id, user_id FROM auto WHERE _id=%s AND user_id = %s" , (userData.id, userData.user_id,))
      res = mycursor.fetchall()
      if (len(res) > 0):  
        mycursor.execute("DELETE FROM auto WHERE _id=%s",(userData.id,))
        connection.commit()
        rowCount = mycursor.rowcount
        connection.close()
        if (rowCount > 0):
          return {'deleted': True}
        else:
          return {'deleted': False}
      else:
        connection.close()
        return {'deleted': 'no_data'}
    else:
      return RequestError(response, {'MySQL', 'Token is obsolete'})
      
  except Error as e:
      connection.rollback()
      connection.close()
      return {'deleted': 'have_data', 'errors': e}


@router.post("/upd_my_auto", status_code = 200)
async def upd_my_auto(userData: UpdateAuto, response: Response):
  try:
    # TODO: как тут с ошибкой вывалится, остается заблоченным компонент редактирования именно этой строки
    if (verify_token(userData.token) & (userData.user_id != '') & (userData.auto_id !='') ):
      connection = MysqlConnect.connectDb()  
      mycursor = connection.cursor(dictionary=True)
      mycursor.execute("SELECT _id, user_id FROM auto WHERE _id=%s AND user_id = %s" , (userData.auto_id, userData.user_id,))
      res = mycursor.fetchall()
      if (len(res) > 0):  
        mycursor.execute("UPDATE auto SET name=%s, comment=%s, date_create=%s WHERE _id=%s",(userData.name, userData.comment, userData.date, userData.auto_id,))
        connection.commit()
        rowCount = mycursor.rowcount
        connection.close()
        if (rowCount > 0):
          return {'updated': True}
        else:
          return {'updated': False}
      else:
        connection.close()
        return {'updated': 'no_data'}
    else:
      return RequestError(response, {'MySQL', 'Token is obsolete'})
      
  except Error as e:
      connection.rollback()
      connection.close()
      return {'updated': 'Can\'t update', 'errors': e}