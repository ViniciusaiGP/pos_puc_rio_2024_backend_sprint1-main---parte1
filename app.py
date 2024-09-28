from datetime import datetime, timedelta
import hashlib

from flask import jsonify, redirect
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, get_jwt_identity, jwt_required
from flask_openapi3 import OpenAPI, Info, Tag
from flask_restful import Api, reqparse
import requests

from blacklist import BLACKLIST
from model.produto import ProductBody, ProductPath
from schemas.error import ErrorAuthorizationSchema, ErrorSchema, ServerErrorSchema
from schemas.nota import ListagemNotaSchema, NotaSchema
from schemas.produto import DeleteSchema, ListagemProdutosApiSchema, NotFoundSchema
from schemas.usuario import InvalidProtectedSchema, ListagemUsuariosApiSchema, LoginRepSchema
from schemas.usuario import LoginSchema, LogoutSchema, ProtectedSchema, RegisterSchema
from services.nota_fiscal_eletronica import NotaFiscalExtractor

import os
from dotenv import load_dotenv

load_dotenv()

info = Info(title="API Token", version="1.0.0", description="API para gerenciar acesso.")
app = OpenAPI(__name__, info=info)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

api = Api(app)
jwt = JWTManager(app)

CORS(app) 

@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'mesage': 'Você foi desconectado.'}), 401

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger")
auth_tag = Tag(name="Autentificação", description="Rotas para Autentificação")
nota_tag = Tag(name="Nota fiscal", description="Rota para (API EXTERNA)")
produto_tag = Tag(name="Produto", description="Rotas para Produto")
usuario_tag = Tag(name="Usuário", description="Rotas para Usuário")


api_usuario = os.getenv('SERVER1')
api_produto = os.getenv('SERVER2')

security_scheme = {
    "Bearer Token": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    }
}
app.security_schemes = security_scheme

def verificar_token_valido():
    try:
        token_data = get_jwt_identity()
        if 'exp' in token_data:
            exp_time = token_data['exp']
            current_time = datetime.now().timestamp()
            if current_time < exp_time:
                return jsonify({'message': 'Token válido'}), 200
    except:
        pass

    return jsonify({'message': 'Token expirado ou inválido'}), 401

@app.get('/', tags=[home_tag], doc_ui=False)
def home():
    """ Home da aplicação.

        Redireciona para /openapi/swagger, abrindo a documentação da API.
    """
    return redirect('/openapi/swagger')

@app.get('/protected', methods=['GET'], tags=[auth_tag], 
         responses={
                    "200": ProtectedSchema,
                    "401": InvalidProtectedSchema,
                    "500": ServerErrorSchema}, 
        security=[{"Bearer Token": []}])
@jwt_required()
def protected():
    """ Verificador TOKEN.

        Verifica se o token ainda está válido/expirado.
     """
    if verificar_token_valido():
        return jsonify({'message': 'Token valido'}), 200
    else:
        return jsonify({'message': 'Token expirado'}), 401
    
@app.get('/usuarios', methods=['GET'], tags=[usuario_tag], 
         responses={
                    "200": ListagemUsuariosApiSchema, 
                    "400": ErrorSchema, 
                    "401": ErrorAuthorizationSchema, 
                    "500": ServerErrorSchema}, 
        security=[{"Bearer Token": []}])
@jwt_required()
def all_users():
    """ Mostra todos os usuários.

        Retorna todos os usuários registrados se o login for valido.
     """
    url = f"{api_usuario}/api/usuarios"
    
    headers = {
            'Authorization': f'Bearer {create_access_token(identity=get_jwt_identity())}'  
        }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json(), 200
    elif response.status_code == 401:
        return {"error": "Token inválido ou expirado"}, 401
    elif response.status_code == 404:
        return {"error": "Endpoint não encontrado"}, 404
    elif response.status_code == 500:
        return {"error": "Erro interno no servidor"}, 500
    else:
        return {"error": f"Erro inesperado: {response.status_code}"}, response.status_code

@app.get('/produtos', methods=['GET'], tags=[produto_tag], 
        responses={
                    "200": ListagemProdutosApiSchema, 
                    "400": ErrorSchema, 
                    "401": ErrorAuthorizationSchema, 
                    "500": ServerErrorSchema}, 
        security=[{"Bearer Token": []}])
@jwt_required()
def all_products():
    """ Mostra todos os produtos.

        Retorna todos os produtos cadastrados.
     """
    url = f"{api_produto}/api/produtos"
    
    headers = {
            'Authorization': f'Bearer {create_access_token(identity=get_jwt_identity())}'  
        }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json(), 200
    elif response.status_code == 401:
        return {"error": "Token inválido ou expirado"}, 401
    elif response.status_code == 404:
        return {"error": "Endpoint não encontrado"}, 404
    elif response.status_code == 500:
        return {"error": "Erro interno no servidor"}, 500
    else:
        return {"error": f"Erro inesperado: {response.status_code}"}, response.status_code

@app.post('/login', tags=[auth_tag], responses={"200": LoginRepSchema, "400": ErrorSchema, "500":ServerErrorSchema})
def login(body:LoginSchema):
    """ Autentificação para o usuário.

        Está sendo usado o JWT para a segurança dos endpoints, o retorno será um token e o login.
    """
    atributos = reqparse.RequestParser()
    atributos.add_argument('login', type=str, required=True)
    atributos.add_argument('senha', type=str, required=True)
    dados = atributos.parse_args()

    senha_hash = hashlib.sha256(dados['senha'].encode()).hexdigest()
    url = f"{api_usuario}/api/verifica_senha"
    
    body_envio= {
                 'login':dados['login'],
                 'senha': senha_hash
                 }
    
    response = requests.post(url, json=body_envio)

    if response.status_code == 201:
        token_de_acesso = create_access_token(identity=response.json())  
        data = response.json()  
        nivel = data.get('nivel') 
        return {
            'login': dados['login'],
            'access_token': token_de_acesso,
            'nivel':nivel
        }, 200
    else:
        return {'message': 'Erro ao efetuar o login.'}, 400
    
@app.post('/register', tags=[usuario_tag], responses={"201": LoginRepSchema, "400": ErrorSchema, "500":ServerErrorSchema})
def register(body:RegisterSchema):
    """ Cria um novo usuário.

        Cria um usuário caso tenha a chave de acesso.
    """
    
    atributos = reqparse.RequestParser()
    atributos.add_argument('login', type=str, required=True)
    atributos.add_argument('senha', type=str, required=True)
    atributos.add_argument('nivel', type=int, required=True)
    atributos.add_argument('email', type=str, required=True)
    dados = atributos.parse_args()
    
    url = f"{api_usuario}/api/registrar"
    
    envio = {
        'login': dados['login'],
        'senha': dados['senha'],
        'nivel': dados['nivel'],
        'email': dados['email']
    }
   
    response = requests.post(url, json=envio)
    
    if response.status_code == 201:
        return response.json(), 201
    else: 
        return response.json(), 400
    
@app.post('/nota_url', tags=[nota_tag], responses={"201": ListagemNotaSchema, "400": ErrorSchema, "401": ErrorAuthorizationSchema, "500":ServerErrorSchema}, security=[{"Bearer Token": []}])
@jwt_required()
def post_nota(body: NotaSchema):
    """ Busca os produtos da nota.

        Recebe as informações da nota fiscal e cadastra os produtos.
    """
    atributos = reqparse.RequestParser()
    atributos.add_argument('nota_url', type=str, required=True)
    dados = atributos.parse_args()

    if not dados['nota_url'] or dados['nota_url'] is None:
        return {"mesage": "O campo 'nota_url' precisa estar preenchido."}, 400

    try:
        nota_fiscal_extractor = NotaFiscalExtractor(url=dados['nota_url'])
        nota_fiscal = nota_fiscal_extractor.extract()
        
        dados_t_list = []
        empresa = nota_fiscal["Empresa"]["Nome da Empresa"]

        for item in nota_fiscal["Itens"]:
            dados_t = {
                'nome': item["Produto"],
                'descricao': empresa,
                'preco': float(item["Vl. Total"].replace(",", ".")),
                'quantidade': int(item["Qtde"])
            }
            dados_t_list.append(dados_t)

        headers = {
            'Authorization': f'Bearer {create_access_token(identity=get_jwt_identity())}'
        }

        for dados in dados_t_list:
            body_env = {
                'nome': dados['nome'],
                'descricao': dados['descricao'],
                'preco': dados['preco'],
                'quantidade': dados['quantidade']
            }
            url = f"{api_produto}/api/registrar"
            response = requests.post(url, json=body_env, headers=headers)

        return jsonify({"Itens": dados_t_list}), 201
    except Exception as e:
        return {'mesage': 'Ocorreu um erro na leitura'}, 500

@app.post('/logout', tags=[auth_tag], responses={"200": LogoutSchema,"500":ServerErrorSchema}, security=[{"Bearer Token": []}])
@jwt_required()
def logout():
    """ Desconecta o usuário.

        Adiciona na blacklist o token do usuário conectado e faz com que ele seja impossibilitado de usar novamente.
    """
    try:
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'mesage': 'Saiu com sucesso!'}, 200
    except: {'mesage': 'Server error'}, 500
    
@app.delete('/produto/<int:id>', tags=[produto_tag], 
            responses={
                    "200": DeleteSchema, 
                    "400": ErrorSchema, 
                    "404": NotFoundSchema, 
                    "401": ErrorAuthorizationSchema, 
                    "500": ServerErrorSchema},
            security=[{"Bearer Token": []}])
@jwt_required()
def delete_Product(path: ProductPath):
    """ Deleta um produto.

        Remove um produto da outra API.
    """

    headers = {
        'Authorization': f'Bearer {create_access_token(identity=get_jwt_identity())}'  
    }

    url_delete = f"{api_produto}/api/produto/{path.id}"
    response_delete = requests.delete(url_delete, headers=headers)

    if response_delete.status_code == 200:
        return {"message": "Produto deletado com sucesso."}, 200
    elif response_delete.status_code == 404:
        return {"error": "Produto não encontrado para deletar."}, 404
    else:
        return {"error": "Erro ao deletar o produto."}, response_delete.status_code
    
@app.put('/produto/<int:id>', tags=[produto_tag], 
        responses={
                    "200": ProductBody, 
                    "400": ErrorSchema, 
                    "404": NotFoundSchema, 
                    "401": ErrorAuthorizationSchema, 
                    "500": ServerErrorSchema},
        security=[{"Bearer Token": []}])
@jwt_required()
def edit_Product(path: ProductPath, body: ProductBody):
    """Atualizar um usuario
    
       Atualiza o nome, email, senha e nível de um usuário existente.
    """

    headers = {
        'Authorization': f'Bearer {create_access_token(identity=get_jwt_identity())}'  
    }

    body_send = {
        'nome': body.nome,
        'descricao': body.descricao,
        'preco': body.preco,
        'quantidade': body.quantidade,
    }
    
    url_edit = f"{api_produto}/api/produto/{path.id}"
    response_edit = requests.put(url_edit, json=body_send, headers=headers)

    if response_edit.status_code == 200:
        return {"message": "Produto editado com sucesso."}, 200
    elif response_edit.status_code == 404:
        return {"error": "Produto não encontrado para edição."}, 404
    else:
        return {"error": "Erro ao editar o produto."}, response_edit.status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')