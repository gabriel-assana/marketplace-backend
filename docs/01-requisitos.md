# Documento de Requisitos
## Sistema MVP Marketplace

---

## 1. Premissas

Este sistema visa a construção de um **MVP de Marketplace**, focado em validar rapidamente a ideia de uma plataforma de anúncios entre pessoas.

**Premissas do projeto:**

- O sistema deve ser simples e direto  
- O foco é permitir publicação e visualização de anúncios  
- Funcionalidades avançadas ficam fora do escopo inicial  
- O sistema deve servir como base para evoluções futuras  

---

## 2. Visão Geral do Sistema

O sistema permite que usuários publiquem anúncios de produtos e visualizem anúncios de outros usuários.

### Usuários anônimos podem:
- Visualizar produtos  
- Buscar produtos  
- Criar conta  
- Fazer login  

### Usuários autenticados podem:
- Publicar anúncios  
- Editar seus próprios anúncios  
- Excluir seus próprios anúncios  

### Dados principais

#### Usuário
- Id  
- Nome  
- Email  
- Senha  

#### Produto (Anúncio)
- Id  
- Título  
- Descrição  
- Preço  
- URL da imagem  
- Usuário anunciante  
- Categoria

---

## 3. Modelo Conceitual (simplificado)

- Um **Usuário** pode publicar **vários Produtos**  
- Um **Produto** pertence a **um único Usuário**

---

## 4. Atores

### Usuário Anônimo
- Navega pelos produtos  
- Busca produtos  
- Realiza cadastro  
- Efetua login  

### Usuário Logado
- Publica anúncios  
- Edita anúncios próprios  
- Exclui anúncios próprios  
- Visualiza produtos  

---

## 5. Casos de Uso – Visão Geral

| Caso de Uso         | Descrição                     | Atores           |
|--------------------|--------------------------------|------------------|
| Criar conta        | Cadastrar novo usuário         | Usuário anônimo  |
| Login              | Autenticar usuário             | Usuário anônimo  |
| Consultar produtos | Listar anúncios                | Público          |
| Buscar produtos    | Buscar anúncios pelo nome      | Público          |
| Visualizar produto | Ver detalhes do anúncio        | Público          |
| Publicar anúncio   | Criar novo anúncio             | Usuário logado   |
| Editar anúncio     | Alterar anúncio próprio        | Usuário logado   |
| Excluir anúncio    | Remover anúncio próprio        | Usuário logado   |

---

## 6. Casos de Uso – Detalhamento

### 6.1 Criar conta
- **Ator:** Usuário anônimo  
- **Visão geral:** Criar uma conta no sistema  

**Fluxo principal:**
1. Usuário informa nome, email e senha  
2. Sistema cria o usuário  

### 6.2 Login
- **Ator:** Usuário anônimo  
- **Pós-condição:** Usuário autenticado  

**Fluxo principal:**
1. Usuário informa email e senha  
2. Sistema valida credenciais  
3. Sistema autentica o usuário  

### 6.3 Consultar produtos
- **Atores:** Público  
- **Visão geral:** Listar anúncios disponíveis  

**Fluxo principal:**
1. Usuário acessa a tela inicial  
2. Sistema retorna lista de produtos com título, preço e imagem  

### 6.4 Buscar produtos
- **Atores:** Público  
- **Visão geral:** Buscar produtos pelo nome  

**Fluxo principal:**
1. Usuário informa parte do nome  
2. Sistema retorna anúncios filtrados  

### 6.5 Visualizar produto
- **Atores:** Público  
- **Visão geral:** Exibir detalhes de um anúncio  

**Fluxo principal:**
1. Usuário seleciona um produto  
2. Sistema retorna título, descrição, preço e imagem  

### 6.6 Publicar anúncio
- **Ator:** Usuário logado  
- **Visão geral:** Criar um novo anúncio  

**Fluxo principal:**
1. Usuário informa título, descrição, preço e imagem  
2. Sistema salva o anúncio vinculado ao usuário  

### 6.7 Editar anúncio
- **Ator:** Usuário logado  
- **Pré-condição:** Ser dono do anúncio  

**Fluxo principal:**
1. Usuário seleciona um anúncio próprio  
2. Sistema exibe os dados  
3. Usuário altera informações  
4. Sistema salva alterações  

### 6.8 Excluir anúncio
- **Ator:** Usuário logado  
- **Pré-condição:** Ser dono do anúncio  

**Fluxo principal:**
1. Usuário seleciona um anúncio próprio  
2. Sistema remove o anúncio  

---

## 7. API REST – Endpoints

### Convenções
- Base URL: `/api`  
- Formato: JSON  
- Autenticação via token (quando necessário)  

### 7.1 Autenticação

#### Criar conta
```http
POST /api/auth/signup
```

```json
{
  "name": "João Silva",
  "email": "joao@email.com",
  "password": "123456"
}
```

#### Login
```http
POST /api/auth/login
```

```json
{
  "email": "joao@email.com",
  "password": "123456"
}
```

```json
{
  "accessToken": "jwt-token"
}
```

### 7.2 Produtos

#### Listar produtos
```http
GET /api/products
```

#### Buscar produtos
```http
GET /api/products?name=notebook
```

#### Visualizar produto
```http
GET /api/products/{id}
```

#### Criar anúncio 🔒
```http
POST /api/products
```

```json
{
  "title": "iPhone 11",
  "description": "Usado, em bom estado",
  "price": 2500.00,
  "imageUrl": "https://img.com/iphone.jpg",
  "category": "eletronico"
}
```

#### Editar anúncio 🔒 (dono)
```http
PUT /api/products/{id}
```

#### Excluir anúncio 🔒 (dono)
```http
DELETE /api/products/{id}
```

---

## 8. Escopo Explicitamente Fora do MVP

- Pagamentos  
- Carrinho de compras  
- Chat entre usuários  
- Avaliações ou reputação  
- Administração  
- Relatórios  
