from fastapi import APIRouter, FastAPI, Request, Response, status, HTTPException, Header

from ..lib.checker import  *
from ..lib.baseClasses import UserReg, UserLogin, UserCheck, AddAuto, DeleteAuto, UpdateAuto
from ..lib.token import *

from mysql.connector import Error
from ..MysqlConnect import MysqlConnect




router = APIRouter()

@router.post("/get_my_remonts", status_code = 200)
async def get_my_remonts(userData: UserCheck, response: Response):
  try:
    if (verify_token(userData.token) & (userData.user_id != '') ):
      connection = MysqlConnect.connectDb()  
      mycursor = connection.cursor(dictionary=True)
      if (userData.auto_id !=''):
        mycursor.execute("SELECT * FROM categories WHERE _id in ( SELECT category_id FROM auto_cat WHERE auto_id in ( SELECT _id FROM auto WHERE _id = %s AND user_id = %s)) ORDER BY start_date, level", (userData.auto_id, userData.user_id))   
      res = mycursor.fetchall()
      connection.close()
      return res
    else:
      return RequestError(response, {'MySQL', 'Token is obsolete'})
      
  except Error as e:
      connection.close()
      return e