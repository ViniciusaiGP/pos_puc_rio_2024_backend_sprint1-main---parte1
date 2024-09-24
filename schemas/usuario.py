from typing import List, Optional
from pydantic import BaseModel, Field


class LoginSchema(BaseModel):
    """ Define como é a conexão de exemplo de usuário.
    """
    login: str = "teste"
    senha: str = "1234"

class LoginRepSchema(BaseModel):
    """ Define como é a conexão de exemplo de usuário.
    """
    access_token: str 
    message: str
    login: str
    nivel: int 

class LoginRepApiSchema(BaseModel):
    """ Define como é de exemplo de usuário.
    """
    ativado: str
    email: str
    login: str
    nivel: int
    user_id: int

class ListagemUsuariosApiSchema(BaseModel):
    """ Define como uma listagem de usuários será retornada.
    """
    Users:List[LoginRepApiSchema]

class RegisterSchema(BaseModel):
    """ Define como um novo usuário será criado.
    """
    login: str = "teste"
    senha: str = "1234"
    nivel: int = 1
    email: str =  "teste@teste.com"
    
class LinkSchema(BaseModel):
    """ Define o modelo de link.
    """
    link: str 
    

class ListagemUsuariosSchema(BaseModel):
    """ Define como uma listagem de usuários será retornada.
    """
    Users:List[LoginRepSchema]

class LogoutSchema(BaseModel):
    """ Retorno do logout do usuário.
    """
    message: str 

class ProtectedSchema(BaseModel):
    """ Retorno da validação do TOKEN.
    """
    message: str = "Token valido"

class InvalidProtectedSchema(BaseModel):
    """ Retorno da validação do TOKEN.
    """
    msg: str = "Token has expired"
    
class UserPath(BaseModel):
    """ Campo id obrigatorio.
    """
    id: int = Field(..., description='id', json_schema_extra={"Exemplo": 1})

class UserQuery(BaseModel):
    """ Campos opcionais para update
    """
    email: Optional[str] = Field(None, description='email', example='user@example.com')
    senha: Optional[str] = Field(None, description='senha', example='1234')
    nivel: Optional[int] = Field(None, description='nivel de acesso', example=1)
    ativado: Optional[str] = Field(None, description='S ou N', example='S')

class UserBody(BaseModel):
    """ Campos opcionais para update
    """
    email: Optional[str] = Field(None, description='email', example='user@example.com')
    senha: Optional[str] = Field(None, description='senha', example='1234')
    nivel: Optional[int] = Field(None, description='nivel de acesso', example=1)
    ativado: Optional[str] = Field(None, description='S ou N', example='S')