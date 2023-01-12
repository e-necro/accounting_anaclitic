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


'''
  возврат статуса и ошибки
  ошибка в виде:
  {'MySQL', 'User already registered'}
'''
def RequestError(response, error):
  response.status_code = 419  # вывод ошибок, точнее формат сделать нормальным! 
  errors = { 'errors': {
      error
    }
  }
  return errors


