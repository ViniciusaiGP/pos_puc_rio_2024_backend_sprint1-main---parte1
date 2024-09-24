from pydantic import BaseModel, Field
from typing import List, Optional


class NotaSchema(BaseModel):
    """ Exemplo de nota url
    """
    nota_url: str = "http://www.fazenda.pr.gov.br/nfce/qrcode?p=41240411517841002211650050003017141734260606|2|1|2|6E4A8B1F83EAE8EEC741FF1A8AEBB913FD6D9688" 
    
class InformacoesPagamento(BaseModel):
    """ Montagem do modo de pagamento.
    """
    Forma_de_pagamento: str
    Valor_total_pago: float 

class Empresa(BaseModel):
    """ Montagem da informação de compra da empresa.
    """
    # CNPJ: str
    # Endereco: str
    Nome_da_Empresa: str

class Item(BaseModel):
    """ Item de montagem para a lista.
    """
    nome: str
    quantidade: int
    preco: float
    descricao: str
    
class ListagemNotaSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    
    Itens: List[Item]

class NotaPath(BaseModel):
    """ Campo id obrigatorio.
    """
    nota_url: str = Field(..., description='link', json_schema_extra={"Exemplo": 'link'})

class NotaQuery(BaseModel):
    """ Campos opcionais para update
    """
    link: Optional[str] = Field(None, description='link', example='link')