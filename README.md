# API de Gerenciamento de Estoque com JWT e Flask

Esta é uma API RESTful para gerenciar usuários, produtos e notas fiscais eletrônicas, com autenticação via tokens JWT. Desenvolvida com Flask, Flask-RESTful e Flask-JWT-Extended, ela oferece funcionalidades essenciais de um sistema de estoque, como cadastro, edição, exclusão e listagem de produtos. Além disso, a API integra dados de notas fiscais eletrônicas para automatizar a entrada de produtos no estoque.
## Funcionalidades

* Autenticação JWT: Tokens JWT para garantir segurança nas rotas protegidas.
* Gerenciamento de usuários: Registro, login, listagem e logout.
* Gerenciamento de produtos: Listagem, criação, edição e exclusão de produtos.
* Integração com notas fiscais: Busca e inserção de produtos via URL de notas fiscais.
* Proteção de rotas: Acesso restrito a rotas sensíveis, garantindo integridade do sistema.

---

## Requisitos

Crie um ambiente virtual para instalar as dependências do projeto:

Windows:
```
python -m venv venv
```
macOS e Linux:
```
python3 -m venv venv
```

Ative o ambiente virtual:

Windows:
```
venv\Scripts\activate
```
macOS e Linux:
```
source venv/bin/activate
```

Instale as dependências do projeto:

```
pip install -r requirements.txt
```

Não esqueça de fazer um arquivo `.env` na pasta raiz.

---

## Configuração

O projeto utiliza um banco de dados SQLite, então não há necessidade de configurações adicionais. Porém, para uso em produção, recomenda-se alterar para um banco de dados mais robusto, como PostgreSQL ou MySQL.

## Funcionalidades
Aqui está a documentação gerada para sua API com base no código fornecido. A estrutura segue o padrão OpenAPI (Swagger), e o esquema apresentado já utiliza o decorador `@app.get` e `@app.post` do Flask OpenAPI.

### **API Documentation**
---

**Title**: API Token  
**Version**: 1.0.0  
**Description**: API para gerenciar acesso.

### **Tags**

- **Documentação**: Seleção de documentação (Swagger)
- **Autentificação**: Rotas para autentificação (Login, Logout)
- **Nota fiscal**: Rota para consultar produtos de nota fiscal (API Externa)
- **Produto**: Rotas para manipulação de produtos
- **Usuário**: Rotas para manipulação de usuários

### **Security Schemes**

**Bearer Token**:
- Type: HTTP
- Scheme: Bearer
- Bearer Format: JWT

---

### **Endpoints**

---

#### **Home**  
`GET /`

**Description**: Redireciona para a documentação da API Swagger.  
**Tags**: Documentação  

---

#### **Login**  
`POST /login`

**Description**: Endpoint para autentificação de usuários. Retorna um token de acesso e o nível de usuário.  
**Tags**: Autentificação  
**Request Body**:  
- login (string) - Obrigatório  
- senha (string) - Obrigatório  

**Response**:  
- **200 OK**: Retorna o login, o token de acesso e o nível de usuário.  
- **400 Bad Request**: Erro ao efetuar o login.  

---

#### **Register**  
`POST /register`

**Description**: Cria um novo usuário.  
**Tags**: Usuário  
**Request Body**:  
- login (string) - Obrigatório  
- senha (string) - Obrigatório  
- nivel (int) - Obrigatório  
- email (string) - Obrigatório  

**Response**:  
- **201 Created**: Usuário criado com sucesso.  
- **400 Bad Request**: Erro ao criar o usuário.  

---

#### **Logout**  
`POST /logout`

**Description**: Faz logout do usuário, invalidando o token.  
**Tags**: Autentificação  
**Response**:  
- **200 OK**: Usuário saiu com sucesso.  
- **500 Server Error**: Erro ao processar o logout.

---

#### **Verificar Token**  
`GET /protected`

**Description**: Verifica se o token JWT é válido ou expirado.  
**Tags**: Autentificação  
**Security**: Bearer Token  
**Responses**:  
- **200 OK**: Token válido.  
- **401 Unauthorized**: Token expirado ou inválido.  

---

#### **Listar Usuários**  
`GET /usuarios`

**Description**: Retorna todos os usuários cadastrados.  
**Tags**: Usuário  
**Security**: Bearer Token  
**Responses**:  
- **200 OK**: Lista de usuários.  
- **401 Unauthorized**: Token inválido ou expirado.  
- **500 Server Error**: Erro interno no servidor.

---

#### **Listar Produtos**  
`GET /produtos`

**Description**: Retorna todos os produtos cadastrados.  
**Tags**: Produto  
**Security**: Bearer Token  
**Responses**:  
- **200 OK**: Lista de produtos.  
- **401 Unauthorized**: Token inválido ou expirado.  
- **500 Server Error**: Erro interno no servidor.

---

#### **Cadastrar Produtos de Nota Fiscal**  
`POST /nota_url`

**Description**: Recebe a URL de uma nota fiscal e cadastra os produtos associados.  
**Tags**: Nota fiscal  
**Request Body**:  
- nota_url (string) - Obrigatório  

**Security**: Bearer Token  
**Responses**:  
- **201 Created**: Produtos cadastrados com sucesso.  
- **400 Bad Request**: O campo 'nota_url' não foi preenchido.  
- **500 Server Error**: Erro ao processar a leitura da nota fiscal.

---

#### **Deletar Produto**  
`DELETE /produto/{id}`

**Description**: Deleta um produto existente.  
**Tags**: Produto  
**Path Parameter**:  
- id (int) - ID do produto a ser deletado.  

**Security**: Bearer Token  
**Responses**:  
- **200 OK**: Produto deletado com sucesso.  
- **404 Not Found**: Produto não encontrado.  
- **500 Server Error**: Erro ao deletar o produto.

---

#### **Atualizar Produto**  
`PUT /produto/{id}`

**Description**: Atualiza as informações de um produto existente.  
**Tags**: Produto  
**Path Parameter**:  
- id (int) - ID do produto a ser atualizado.  

**Request Body**:  
- nome (string) - Nome do produto.  
- descricao (string) - Descrição do produto.  
- preco (float) - Preço do produto.  
- quantidade (int) - Quantidade do produto.  

**Security**: Bearer Token  
**Responses**:  
- **200 OK**: Produto atualizado com sucesso.  
- **404 Not Found**: Produto não encontrado.  
- **500 Server Error**: Erro ao atualizar o produto.

---

## Executando o projeto

Para iniciar o servidor de desenvolvimento, execute:

```
python app.py
```

O servidor será iniciado em `http://localhost:5001`.

---

# Docker

### 1. Criar a rede manualmente:
Você pode criar a rede antes de subir os containers usando o comando abaixo:

```bash
docker network create my_custom_network
```

### 2. Definir os containers no `docker-compose.yml`:

Depois, no arquivo `docker-compose.yml`, associe os containers a essa rede criada:

```yaml
version: '3'
services:
  flask-1:
    image: docker-1-flask-app-service
    container_name: flask-1
    ports:
      - "5001:5000"
    networks:
      - my_custom_network

  flask-2:
    image: docker-2-flask-app-service
    container_name: flask-2
    ports:
      - "5002:5000"
    networks:
      - my_custom_network

  flask-3:
    image: docker-3-flask-app-service
    container_name: flask-3
    ports:
      - "5003:5000"
    networks:
      - my_custom_network

networks:
  my_custom_network:
    external: true
```

### Explicação:
- **`networks`:** Aqui estamos indicando que a rede `my_custom_network` já existe (`external: true`), ou seja, ela foi criada previamente e não será gerada automaticamente pelo Docker Compose.

### 3. Subir os containers:
Com a rede criada, você pode subir os containers normalmente:

```bash
docker-compose up -d
```

### Verificar os containers na rede:
Você pode verificar se os containers estão corretamente conectados à rede com o seguinte comando:

```bash
docker network inspect my_custom_network
```

Dessa forma, você cria uma rede separada e coloca os containers dentro dela para que possam se comunicar.

# Estrutura

![alt text](image.png)
