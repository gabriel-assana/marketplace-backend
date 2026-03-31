# Planejamento MVP Marketplace

---

## 1. Estrutura Geral do Projeto

```
mvp-marketplace/
├── frontend/
├── backend/
├── docs/
└── README.md
```

- **frontend/** → React JS  
- **backend/** → API REST em Python  
- **docs/** → Requisitos, Arquitetura, Diagramas  
- **README.md** → Visão geral do projeto

---

## 2. Frontend — React JS

Estrutura simples, escalável e comum no mercado.

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── api/
│   │   └── http.js
│   ├── components/
│   │   ├── ProductCard.jsx
│   │   └── Header.jsx
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── ProductDetails.jsx
│   │   ├── Login.jsx
│   │   ├── Signup.jsx
│   │   └── CreateProduct.jsx
│   ├── services/
│   │   ├── authService.js
│   │   └── productService.js
│   ├── routes/
│   │   └── AppRoutes.jsx
│   ├── App.jsx
│   └── main.jsx
├── package.json
└── README.md
```

### Responsabilidades

- **pages/** → Telas  
- **components/** → Componentes reutilizáveis  
- **services/** → Chamadas à API  
- **api/** → Configuração do client HTTP  
- **routes/** → Controle de rotas

✅ Estrutura alinhada com a API REST definida.

---

## 3. Backend — Python (FastAPI)

Arquitetura em camadas, porém enxuta.

```
backend/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   └── products.py
│   │   └── dependencies.py
│   ├── core/
│   │   ├── security.py
│   │   └── config.py
│   ├── models/
│   │   ├── user.py
│   │   └── product.py
│   ├── schemas/
│   │   ├── user.py
│   │   └── product.py
│   ├── services/
│   │   ├── auth_service.py
│   │   └── product_service.py
│   ├── repositories/
│   │   ├── user_repository.py
│   │   └── product_repository.py
│   ├── database.py
│   └── main.py
├── migrations/
├── requirements.txt
└── README.md
```

### Responsabilidades

- **api/routes/** → Controllers (endpoints REST)  
- **schemas/** → DTOs (entrada e saída)  
- **models/** → Entidades do banco  
- **services/** → Regras de negócio  
- **repositories/** → Acesso ao banco  
- **core/** → Segurança e configurações

✅ Alinhado aos documentos de Requisitos e Arquitetura.

---

## 4. Docs

```
docs/
├── requisitos.md
├── arquitetura.md
└── api.md
```

---

## 5. Como Iniciar o Desenvolvimento

### Ordem recomendada

#### Passo 1 — Backend primeiro
O frontend depende da API.

#### Passo 2 — Fundações do Backend
- Criar projeto FastAPI
- Configurar PostgreSQL
- Criar modelos User e Product
- Definir migrações

🎯 Objetivo: banco e API funcionando.

#### Passo 3 — Autenticação
- Signup
- Login
- JWT
- Proteção de endpoints

⚠️ Impacta todo o sistema.

#### Passo 4 — Produtos
- Listar
- Buscar
- Detalhar
- Criar
- Editar
- Excluir

✅ Validar autenticação e posse do anúncio.

#### Passo 5 — Frontend Básico
- Criar projeto React
- Criar páginas principais
- Integrar com API

👉 Estilo depois, funcionalidade primeiro.

#### Passo 6 — Ajustes finais
- Tratamento de erros
- Permissões
- UX básico

---

## 6. Mapeamento História → Implementação

| História         | Onde implementar                  |
|------------------|-----------------------------------|
| Criar conta      | Backend auth → Frontend Signup    |
| Login            | Backend auth → Frontend Login     |
| Listar produtos  | API products → Home               |
| Buscar produto   | API products → Home               |
| Criar anúncio    | API products → CreateProduct      |
| Editar anúncio   | API products → Edit               |
| Excluir anúncio  | API products → Delete             |
