
from mysql.connector import connect, Error





try:
  with connect(
    host="dartpuo6.beget.tech",
      user="dartpuo6_auto",
      password="Gbrm%1Kk",
  ) as connection:
      print(connection)
except Error as e:
    print(e)
  # return "Hello, World!!!!"