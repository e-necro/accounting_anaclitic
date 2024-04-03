from fastapi import APIRouter, FastAPI, Request, Response, status, HTTPException, Header
import copy

from ..lib.checker import  *
from ..lib.baseClasses import  UserCheck, DeleteRemont, AddRemont
from ..lib.token import *

from mysql.connector import Error
from ..MysqlConnect import MysqlConnect


new_categs = {}
tree = {}
router = APIRouter()

@router.post("/get_my_remonts", status_code = 200)
async def get_my_remonts(userData: UserCheck, response: Response):
  try:
    if (verify_token(userData.token) & (userData.user_id != '') ):
      res = {}
      if (userData.auto_id !=''):
        connection = MysqlConnect.connectDb()  
        mycursor = connection.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM categories WHERE _id in ( SELECT category_id FROM auto_cat WHERE auto_id in ( SELECT _id FROM auto WHERE _id = %s AND user_id = %s)) ORDER BY level, parent_id ASC", (userData.auto_id, userData.user_id))   
        tmp_categories = mycursor.fetchall()
        
        key = 0
        ## for row in tmp_categories:
        ##   new_categs[row['_id']] = row
        
        ## resultTree = copy.deepcopy(new_categs)
        ## # resultTree = createTree(new_categs)
        ## res['categories'] = resultTree



        # res['tmp_categories'] = tmp_categories
        # for row in tmp_categories :
        #   if (key == 0):
        #     key = row['_id']
        #   if row['parent_id'] not in new_categs:
        #     new_categs[row['parent_id']] = {}
        #     new_categs[row['parent_id']][row['_id']] = row
        #   else:
        #     new_categs[row['parent_id']][row['_id']] = row # Добавление работает, но не вписываются уровень что к чему относится
        
        # res['categories'] = new_categs
        # resultTree = createTree(new_categs, new_categs[key])
        # res['tree'] = resultTree
        
        result = []
        for row in tmp_categories:
          if row['parent_id'] == 0:
            result.append([row['_id'], row['name'], None])
          else:
            result.append([row['_id'], row['name'], row['parent_id']])

        res['tree'] = createTree(result)


        mycursor.execute(" SELECT * FROM remonts WHERE _id in (SELECT _id FROM categories WHERE _id in ( SELECT category_id FROM auto_cat WHERE auto_id in ( SELECT _id FROM auto WHERE _id = %s AND user_id = %s))) ORDER BY start_date desc", (userData.auto_id, userData.user_id)) 
        res['remonts'] = mycursor.fetchall()

        connection.close()
      return res
    else:
      return RequestError(response, {'MySQL', 'Token is obsolete'})
      
  except Error as e:
      connection.close()
      return e

def createTree(list_):
  new_list = []
  print(list_)
  for item in list_:
    if item[2] is None:
        new_list.append(item)
    else:
        new_item = [item[0], item[1]]
        print([x for x in list_ if x[2] == item[2]])
        # new_item.append(createTree([x for x in list_ if x[2] == item[2]]))
        new_list.append(new_item)
  return new_list


@router.post("/delete_my_remont", status_code = 200)
async def delete_my_remont(userData: DeleteRemont, response: Response):
  try:
    if (verify_token(userData.token) & (userData.user_id != '') ):
      answer = {'deleted': False}

      if (userData.auto_id !='' and userData.id):
        connection = MysqlConnect.connectDb()  
        mycursor = connection.cursor(dictionary=True)
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


@router.post("/add_my_remont", status_code = 200)
async def add_my_remont(remontData: AddRemont, response: Response):
  try: #TODO: еще не проверено
    if (verify_token(remontData.token) & (remontData.user_id != '') ):
      if (remontData.auto_id != '') & (remontData.name !='') & (remontData.price != 0 ) & (remontData.category_id != ''):
        connection = MysqlConnect.connectDb()  
        mycursor = connection.cursor(dictionary=True)
        mycursor.execute("INSERT INTO remonts ( name, comment, category_id, price, elapced_time, start_date, end_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (remontData.name, remontData.comment, remontData.category_id, remontData.price, remontData.elapced_time, remontData.start_date, remontData.end_date ))   
        connection.commit()
        _id = 0
        _id = mycursor.lastrowid
        connection.close()
        return _id
      else:
        return RequestError(response, {'MySQL', 'Wrong auto_id or name or price or category_id. Check them.'})
    else:
      return RequestError(response, {'MySQL', 'Token is obsolete'})
      
  except Error as e:
      connection.close()
      return e