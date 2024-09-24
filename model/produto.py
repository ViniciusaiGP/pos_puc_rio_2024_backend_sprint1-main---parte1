from typing import List, Optional
from pydantic import BaseModel, Field

class RegisterSchema(BaseModel):
    """ Define como um novo produto será criado.
    """
    nome: str = "produto 1"
    descricao: str = "teste"
    preco: float = 1.2
    quantidade: int = 1
    
    
class ProductPath(BaseModel):
    """ Campo id obrigatorio.
    """
    id: int = Field(..., description='id', json_schema_extra={"Exemplo": 1})

class ProductQuery(BaseModel):
    """ Campos opcionais para update
    """
    nome: Optional[str] = Field(None, description='nome', example='produto 1')
    descricao: Optional[str] = Field(None, description='descricao', example='teste')
    preco: Optional[float] = Field(None, description='preco', example=1.2)
    quantidade: Optional[int] = Field(None, description='quantidade', example='5')

class ProductBody(BaseModel):
    """ Campos opcionais para update
    """
    nome: Optional[str] = Field(None, description='nome', example='produto 1')
    descricao: Optional[str] = Field(None, description='descricao', example='teste')
    preco: Optional[float] = Field(None, description='preco', example=1.2)
    quantidade: Optional[int] = Field(None, description='quantidade', example='5')
