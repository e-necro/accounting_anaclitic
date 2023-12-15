from fastapi import APIRouter, FastAPI, Request, Response, status, HTTPException, Header

from ..lib.checker import  *
from ..lib.baseClasses import  UserCheck, DeleteRemont
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
        mycursor.execute("SELECT * FROM categories WHERE _id in ( SELECT category_id FROM auto_cat WHERE auto_id in ( SELECT _id FROM auto WHERE _id = %s AND user_id = %s)) ORDER BY start_date, level desc", (userData.auto_id, userData.user_id))   
      res = mycursor.fetchall()
      connection.close()
      return res
    else:
      return RequestError(response, {'MySQL', 'Token is obsolete'})
      
  except Error as e:
      connection.close()
      return e


# TODO: не готово нихрена
@router.post("/delete_my_remont", status_code = 200)
async def delete_my_remont(userData: DeleteRemont, response: Response):
  try:
    if (verify_token(userData.token) & (userData.user_id != '') ):
      connection = MysqlConnect.connectDb()  
      mycursor = connection.cursor(dictionary=True)
      answer = {'deleted': False}

      if (userData.auto_id !='' and userData.id):
        mycursor.execute("SELECT _id FROM categories WHERE _id = %s AND _id in ( SELECT category_id FROM auto_cat WHERE auto_id in ( SELECT _id FROM auto WHERE _id = %s AND user_id = %s)) ORDER BY start_date, level DESC", (userData.id, userData.auto_id, userData.user_id))   
        res = mycursor.fetchall()
        if (len(res)):
          # ну тупо проверка пройдена, что именно этот ремонтик есть тут. Дальше надо проверить что у него нет дочерних ремонтов.
          mycursor.execute('SELECT _id FROM  categories WHERE parent_id = %s OR top_parent_id = %s', (userData.id, userData.id))
          res = mycursor.fetchall()
          if (len(res) == 0):
            # все пусто, можно удалять
            mycursor.execute("DELETE FROM categories WHERE _id = %s LIMIT 1",(userData.id, )) 
            connection.commit()
            rowCount = mycursor.rowcount
            connection.close()
            if (rowCount > 0):
              answer = {'deleted': True}
      return answer
    else:
      return RequestError(response, {'MySQL', 'Token is obsolete'})
      
  except Error as e:
      connection.close()
      return e