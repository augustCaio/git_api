# 🚀 GitHub Data API

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Deploy](https://img.shields.io/badge/Deploy-Render.com-00AD9F.svg)](https://render.com)
[![Tests](https://img.shields.io/badge/Tests-82%20passed-brightgreen.svg)](tests/)

🌐 **URL da API:** https://git-api-i3y5.onrender.com

📚 **Documentação:** https://git-api-i3y5.onrender.com/docs

---

## 📋 **Sobre o Projeto**

API REST completa para acessar dados do GitHub, desenvolvida com FastAPI e recursos avançados de cache, monitoramento e segurança. Ideal para projetos que precisam de dados do GitHub de forma eficiente e confiável.

### ✨ **Principais Funcionalidades**

- 🔍 **Busca de Usuários** - Perfis completos do GitHub
- 📦 **Repositórios** - Dados detalhados de repositórios
- 💻 **Linguagens** - Análise de linguagens por usuário/repositório
- 📊 **Estatísticas** - Métricas avançadas de usuários
- 🔎 **Busca** - Busca em repositórios e usuários
- 🚀 **Cache Inteligente** - Cache em memória e Redis
- 📈 **Monitoramento** - Logs estruturados e health checks
- 🛡️ **Segurança** - CORS, rate limiting e autenticação opcional
- 🐳 **Containerização** - Docker e Docker Compose
- ☁️ **Deploy Automático** - Render.com

### 🛠️ **Tecnologias Utilizadas**

| Categoria       | Tecnologia         | Versão |
| --------------- | ------------------ | ------ |
| **Framework**   | FastAPI            | 0.104+ |
| **Servidor**    | Uvicorn            | 0.24+  |
| **Validação**   | Pydantic           | 2.5+   |
| **HTTP Client** | httpx              | 0.25+  |
| **Cache**       | Redis + cachetools | 5.0+   |
| **Logging**     | loguru             | 0.7+   |
| **Testes**      | pytest             | 7.4+   |
| **Container**   | Docker             | -      |
| **Deploy**      | Render.com         | -      |

---

## 🚀 **Quick Start**

### **1. Clone o Repositório**

```bash
git clone https://github.com/augustCaio/git_api.git
cd git_api
```

### **2. Configure o Ambiente**

```bash
# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### **3. Configure as Variáveis de Ambiente**

```bash
# Copie o arquivo de exemplo
cp config.env.example config.env

# Edite as configurações
nano config.env
```

**Configurações importantes:**

```bash
GITHUB_TOKEN=seu-token-do-github-aqui
DEBUG=true
HOST=127.0.0.1
PORT=8000
```

### **4. Execute a API**

```bash
# Usando o script unificado
python run.py api

# Ou diretamente com uvicorn
uvicorn app.main:app --reload
```

### **5. Acesse a Documentação**

🌐 **API Local:** http://localhost:8000

📚 **Swagger UI:** http://localhost:8000/docs

📖 **ReDoc:** http://localhost:8000/redoc

---

## 📚 **Documentação da API**

### **Endpoints Principais**

| Método   | Endpoint                                 | Descrição                 |
| -------- | ---------------------------------------- | ------------------------- |
| `GET`    | `/api/v1/users/{username}`               | Dados do usuário          |
| `GET`    | `/api/v1/users/{username}/repositories`  | Repositórios do usuário   |
| `GET`    | `/api/v1/users/{username}/languages`     | Linguagens do usuário     |
| `GET`    | `/api/v1/users/{username}/stats`         | Estatísticas do usuário   |
| `GET`    | `/api/v1/repos/{owner}/{repo}`           | Dados do repositório      |
| `GET`    | `/api/v1/repos/{owner}/{repo}/languages` | Linguagens do repositório |
| `GET`    | `/api/v1/search/repositories`            | Buscar repositórios       |
| `GET`    | `/api/v1/search/users`                   | Buscar usuários           |
| `GET`    | `/api/v1/health`                         | Health check              |
| `GET`    | `/api/v1/cache/stats`                    | Estatísticas do cache     |
| `DELETE` | `/api/v1/cache/clear`                    | Limpar cache              |

### **Exemplos de Uso**

#### **Buscar Dados de Usuário**

```bash
curl https://git-api-i3y5.onrender.com/api/v1/users/octocat
```

```json
{
  "id": 583231,
  "login": "octocat",
  "name": "The Octocat",
  "email": null,
  "avatar_url": "https://avatars.githubusercontent.com/u/583231?v=4",
  "bio": "GitHub mascot",
  "location": "San Francisco",
  "company": "@github",
  "public_repos": 10,
  "followers": 100,
  "following": 50
}
```

#### **Buscar Repositórios**

```bash
curl https://git-api-i3y5.onrender.com/api/v1/users/octocat/repositories?page=1&per_page=5
```

#### **Buscar Linguagens**

```bash
curl https://git-api-i3y5.onrender.com/api/v1/users/octocat/languages
```

#### **Health Check**

```bash
curl https://git-api-i3y5.onrender.com/api/v1/health
```

## 🐳 **Docker**

### **Desenvolvimento**

```bash
# Executar com cache em memória
docker-compose -f docker-compose.dev.yml up

# Executar com Redis
docker-compose -f docker-compose.dev.yml --profile redis-dev up
```

### **Produção**

```bash
# Build e execução
docker build -t github-data-api .
docker run -p 8000:8000 github-data-api

# Com docker-compose (inclui Redis)
docker-compose up -d
```

## ☁️ **Deploy na Render.com**

### **Deploy Automático**

1. **Fork este repositório**
2. **Conecte ao Render.com**
3. **Configure as variáveis de ambiente**
4. **Deploy automático será realizado**

### **Variáveis de Ambiente**

```bash
HOST=0.0.0.0
PORT=8000
DEBUG=false
USE_REDIS_CACHE=false
CACHE_TTL=300
RATE_LIMIT_PER_MINUTE=60
```

### **URL de Produção**

🌐 **API**: https://git-api-i3y5.onrender.com

📚 **Documentação**: https://git-api-i3y5.onrender.com/docs

## 🧪 **Testes**

### **Executar Todos os Testes**

```bash
# Usando o script unificado
python run.py test
```

### **Executar Testes Específicos**

```bash
# Testes de modelos
pytest tests/test_models.py -v

# Testes da API
pytest tests/test_api.py -v

# Testes do cliente GitHub
pytest tests/test_github_client.py -v

# Testes com cobertura
python run.py coverage
```

### **Resultados dos Testes**

- ✅ **82 testes passando**
- ✅ **Cobertura completa** dos principais componentes
- ✅ **Testes de integração** incluídos
- ✅ **Testes de cache** e performance

---

## 📊 **Monitoramento e Logs**

### **Health Check**

```bash
curl https://git-api-i3y5.onrender.com/api/v1/health
```

**Resposta:**

```json
{
  "status": "healthy",
  "message": "GitHub Data API está funcionando corretamente",
  "version": "0.1.0",
  "timestamp": "2025-07-29T12:00:00",
  "cache": {
    "memory_cache_size": 1,
    "use_redis": false
  },
  "environment": "production",
  "uptime": 3600.5,
  "memory": {
    "rss": "45.2 MB",
    "heap": "12.8 MB"
  },
  "github_api": "connected"
}
```

### **Logs Estruturados**

A API utiliza logs estruturados em JSON para facilitar o monitoramento:

```json
{
  "timestamp": "2025-07-29T12:00:00",
  "level": "INFO",
  "service": "github-data-api",
  "version": "0.1.0",
  "environment": "production",
  "message": "Request processed",
  "extra": {
    "request_id": "uuid",
    "duration": 0.5,
    "endpoint": "/api/v1/users/octocat"
  }
}
```

---

## 🔧 **Configuração Avançada**

### **Cache**

A API suporta dois tipos de cache:

1. **Cache em Memória** (padrão)

   - Rápido para desenvolvimento
   - Limpo ao reiniciar a aplicação

2. **Redis** (produção)
   - Persistente entre reinicializações
   - Compartilhado entre múltiplas instâncias

### **Rate Limiting**

- **Padrão:** 60 requisições por minuto
- **Configurável** via variável de ambiente
- **Por IP** ou **API Key**

### **CORS**

- **Desenvolvimento:** Todas as origens permitidas
- **Produção:** Apenas origens específicas
- **Configurável** via variável de ambiente

---

## 🤝 **Contribuição**

### **Como Contribuir**

1. **Fork o projeto**
2. **Crie uma branch** para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit suas mudanças** (`git commit -m 'Add some AmazingFeature'`)
4. **Push para a branch** (`git push origin feature/AmazingFeature`)
5. **Abra um Pull Request**

### **Padrões de Código**

- **Black** para formatação
- **Flake8** para linting
- **MyPy** para type checking
- **Pre-commit hooks** configurados

```bash
# Instalar pre-commit hooks
pre-commit install

# Executar manualmente
pre-commit run --all-files
```

---

## 📄 **Licença**

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 🙏 **Agradecimentos**

- **FastAPI** - Framework web moderno e rápido
- **GitHub API** - Dados ricos e bem documentados
- **Render.com** - Plataforma de deploy gratuita
- **Comunidade Python** - Ferramentas e bibliotecas incríveis

---

## 📞 **Contato**

- **GitHub**: [@augustCaio](https://github.com/augustCaio)
- **Projeto**: [GitHub Data API](https://github.com/augustCaio/git_api)

---

**⭐ Se este projeto te ajudou, considere dar uma estrela no repositório!**
