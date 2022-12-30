from mysql.connector import connect, Error
from pydantic import BaseSettings

class MysqlConnect(BaseSettings):
  test: str = '444'

  def connectDb():
    return  connect(
      host="my-host",
      user="user",
      password="password",
      database="myDb"
    )  
