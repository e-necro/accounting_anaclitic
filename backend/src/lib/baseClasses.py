from pydantic import BaseModel
from typing import Dict

class UserReg(BaseModel):
  '''
    {
      email,
      username,
      password
    }
  '''
  user: Dict

class UserLogin(BaseModel):
  '''
    {
      email,
      password
    }
  '''
  user: Dict

class UserCheck(BaseModel):
# для проверки токена юзера.
  user_id: str
  token: str
  auto_id: str

class AddAuto(BaseModel):
  # добавление тачки
  user_id: str
  token: str
  name: str
  comment: str
  date: str

class UpdateAuto(BaseModel):
  # обновление тачки
  user_id: str
  token: str
  auto_id: str
  name: str
  comment: str
  date: str

class DeleteAuto(BaseModel):
  # удаление тачки
  user_id: str
  token: str
  id: int

class DeleteRemont(BaseModel):
  # удаление строки ремонта
  user_id: str
  token: str
  id: int
  auto_id: str