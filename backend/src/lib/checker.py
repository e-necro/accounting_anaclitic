# проверить пришедшие данные при регистрации
def checkRegister(userData):
  if (userData.user['username'] == ''):
    return False, {'name error':'Write your name'}
  elif (userData.user['email'] == ''):
    return False, {'email':'Write email'}
  elif (userData.user['password'] == ''):
    return False, {'password':'no pass'}
  else:
    return True,'all good'

# Добавление/изменения записи машины
def checkAutoData(autoData):
  if (autoData.name == ''):
    return False, {'name error':'Write your name'}
  elif (autoData.comment == ''):
    return False, {'description error':'Fill your description'}
  elif (autoData.date == ''):
    return False, {'date error':'when your auto is buyed?'}
  else:
    return True,'all good'

'''
  возврат статуса и ошибки
  ошибка в виде:
  {'MySQL', 'User already registered'}
'''
def RequestError(response, error, status_code = 419):
  response.status_code = status_code  # вывод ошибок, точнее формат сделать нормальным! 
  errors = { 'errors': error
  }
  return errors