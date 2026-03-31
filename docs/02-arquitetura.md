# Documento de Arquitetura
## Sistema MVP Marketplace

---

## 1. Objetivo do Documento

Este documento descreve a **arquitetura técnica** do sistema **MVP Marketplace**, definindo:

- Visão geral da arquitetura
- Tecnologias utilizadas
- Responsabilidades de cada camada
- Forma de comunicação entre os componentes

O objetivo é fornecer uma visão clara de **como o sistema será construído**, sem entrar em detalhes de implementação.

---

## 2. Visão Geral da Arquitetura

O sistema adota uma **arquitetura baseada em frontend desacoplado (SPA) e API REST**, com persistência em banco de dados relacional.

### Visão simplificada

```
[ Frontend - React JS ]
        |
     HTTP / JSON
        v
[ Backend - API REST (Python) ]
        |
       ORM
        v
[ Banco de Dados - PostgreSQL ]
```

Essa arquitetura favorece:

- Simplicidade
- Escalabilidade
- Evolução independente entre frontend e backend

---

## 3. Stack Tecnológica

### Frontend

- **React JS**
- Aplicação do tipo **SPA (Single Page Application)**
- Responsável por interface do usuário e navegação
- Tecnologia de estilização será definida posteriormente, sem impacto na arquitetura

### Backend

- **Python**
- API REST
- Framework para teste das chamadas de API: **Swagger**
- Responsável por:
  - Autenticação de usuários
  - Regras de negócio
  - Exposição de endpoints REST
  - Validação de dados

### Banco de Dados

- **PostgreSQL – Neon** (https://neon.com/)
- Banco de dados relacional
- Utilizado para persistência dos dados do sistema

---

## 4. Arquitetura Interna do Backend

O backend segue uma **arquitetura em camadas**, separando responsabilidades.

```
Controller (API)
   |
Service (Negócio)
   |
Model (Persistência)
   |
Database (PostgreSQL)
```

### Responsabilidade das Camadas

#### Controller (API / Router)

- Receber requisições HTTP
- Validar dados de entrada básicos
- Retornar respostas HTTP adequadas

#### Service

- Conter regras de negócio
- Verificar permissões (ex: dono do anúncio)
- Orquestrar operações entre camadas

#### Model

- Acessar o banco de dados
- Executar operações CRUD
- Isolar o uso do ORM

---

## 5. Segurança

- Autenticação baseada em **token (JWT)**
- Endpoints públicos acessíveis sem autenticação
- Endpoints protegidos exigem usuário autenticado
- Usuários só podem editar ou excluir seus próprios anúncios

---

## 6. Comunicação entre os Componentes

- O frontend se comunica com o backend via **HTTP**
- O backend expõe uma **API REST**
- As trocas de dados utilizam **JSON**
- O banco de dados é acessado exclusivamente pelo backend

---

## 7. Escopo Arquitetural

### Incluído

- Frontend SPA
- API REST
- Persistência relacional
- Estrutura em camadas

### Fora do escopo deste MVP

- Microserviços
- Mensageria
- Cache distribuído
- Integração com gateways de pagamento
- Arquitetura orientada a eventos
