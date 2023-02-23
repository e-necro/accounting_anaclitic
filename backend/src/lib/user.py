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