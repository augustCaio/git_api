# 🚀 **GitHub Data API**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Deploy](https://img.shields.io/badge/Deploy-Render.com-00AD9F.svg)](https://render.com/)

Uma API completa e moderna para buscar dados do GitHub de forma eficiente, com cache inteligente, monitoramento avançado e deploy automatizado.

## ✨ **Funcionalidades**

### 👤 **Usuários**

- 📊 Dados completos de perfil
- 📦 Lista de repositórios com paginação
- 🗣️ Linguagens mais utilizadas
- 📈 Estatísticas detalhadas de atividade

### 📦 **Repositórios**

- 🔍 Informações detalhadas
- 📝 Commits, issues e pull requests
- 🗣️ Linguagens utilizadas
- 📊 Eventos e atividades

### 🔍 **Busca Avançada**

- 🔎 Busca de repositórios
- 👥 Busca de usuários
- 📄 Paginação e filtros
- ⚡ Resultados em cache

### 🧠 **Performance**

- 🚀 Cache inteligente (memória + Redis)
- 📊 Métricas de performance
- 🔄 Logs estruturados
- ⚡ Resposta otimizada

## 🛠️ **Tecnologias**

| Tecnologia   | Versão | Descrição                         |
| ------------ | ------ | --------------------------------- |
| **FastAPI**  | 0.104+ | Framework web moderno e rápido    |
| **Pydantic** | 2.5+   | Validação de dados e serialização |
| **httpx**    | 0.25+  | Cliente HTTP assíncrono           |
| **Redis**    | 5.0+   | Cache distribuído (opcional)      |
| **Docker**   | -      | Containerização completa          |
| **Loguru**   | 0.7+   | Logs estruturados                 |

## 🚀 **Quick Start**

### **1. Clone o Repositório**

```bash
git clone https://github.com/seu-usuario/git-api.git
cd git-api
```

### **2. Instale as Dependências**

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### **3. Configure as Variáveis de Ambiente**

```bash
# Copie o arquivo de exemplo
cp config.env.example config.env

# Edite as configurações
nano config.env
```

### **4. Execute a API**

```bash
# Modo interativo (menu)
python run.py

# Modo linha de comando
python run.py api          # Executar apenas a API
python run.py test         # Executar apenas os testes
python run.py all          # Executar testes + API
```

### **5. Acesse a Documentação**

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

## 📚 **Documentação da API**

### **Endpoints Principais**

#### 👤 **Usuários**

| Método | Endpoint                                | Descrição               |
| ------ | --------------------------------------- | ----------------------- |
| `GET`  | `/api/v1/users/{username}`              | Dados de usuário        |
| `GET`  | `/api/v1/users/{username}/repositories` | Repositórios do usuário |
| `GET`  | `/api/v1/users/{username}/languages`    | Linguagens mais usadas  |
| `GET`  | `/api/v1/users/{username}/stats`        | Estatísticas detalhadas |

#### 📦 **Repositórios**

| Método | Endpoint                                 | Descrição                    |
| ------ | ---------------------------------------- | ---------------------------- |
| `GET`  | `/api/v1/repos/{owner}/{repo}`           | Dados do repositório         |
| `GET`  | `/api/v1/repos/{owner}/{repo}/languages` | Linguagens do repositório    |
| `GET`  | `/api/v1/repos/{owner}/{repo}/commits`   | Commits do repositório       |
| `GET`  | `/api/v1/repos/{owner}/{repo}/issues`    | Issues do repositório        |
| `GET`  | `/api/v1/repos/{owner}/{repo}/pulls`     | Pull Requests do repositório |

#### 🔍 **Busca**

| Método | Endpoint                      | Descrição           |
| ------ | ----------------------------- | ------------------- |
| `GET`  | `/api/v1/search/repositories` | Buscar repositórios |
| `GET`  | `/api/v1/search/users`        | Buscar usuários     |

#### 🛠️ **Sistema**

| Método   | Endpoint              | Descrição             |
| -------- | --------------------- | --------------------- |
| `GET`    | `/api/v1/health`      | Health check da API   |
| `GET`    | `/api/v1/cache/stats` | Estatísticas do cache |
| `DELETE` | `/api/v1/cache/clear` | Limpar cache          |

### **Exemplos de Uso**

#### **Buscar Dados de Usuário**

```bash
curl https://github-data-api.onrender.com/api/v1/users/octocat
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
curl https://github-data-api.onrender.com/api/v1/users/octocat/repositories?page=1&per_page=5
```

#### **Buscar Linguagens**

```bash
curl https://github-data-api.onrender.com/api/v1/users/octocat/languages
```

#### **Health Check**

```bash
curl https://github-data-api.onrender.com/api/v1/health
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

🌐 **API**: https://github-data-api.onrender.com

📚 **Documentação**: https://github-data-api.onrender.com/docs

## 🧪 **Testes**

### **Executar Todos os Testes**

```bash
# Usando o script unificado
python run.py test

# Usando pytest diretamente
pytest tests/ -v
```

### **Tipos de Testes**

- ✅ **82 testes** automatizados
- 🧪 **Testes unitários** - Modelos e serviços
- 🔗 **Testes de integração** - Endpoints da API
- 🧠 **Testes de cache** - Funcionalidades de cache
- 📊 **Testes de performance** - Métricas e logs

### **Cobertura de Testes**

```bash
# Executar com cobertura
python run.py coverage
```

## 📊 **Monitoramento**

### **Logs Estruturados**

- 📝 **Aplicação**: `logs/app.log`
- ❌ **Erros**: `logs/error.log`
- ⚡ **Performance**: `logs/performance.log`

### **Métricas de Performance**

- 🕐 **Tempo de resposta**: Headers `X-Response-Time`
- 🧠 **Cache hit/miss**: Endpoint `/api/v1/cache/stats`
- 🔍 **Health check**: Endpoint `/api/v1/health`

### **Headers de Performance**

Todas as requisições incluem:

- `X-Request-ID`: ID único da requisição
- `X-Response-Time`: Tempo de resposta em segundos

## 🔧 **Configuração**

### **Variáveis de Ambiente**

| Variável                | Padrão      | Descrição               |
| ----------------------- | ----------- | ----------------------- |
| `HOST`                  | `127.0.0.1` | Host da aplicação       |
| `PORT`                  | `8000`      | Porta da aplicação      |
| `DEBUG`                 | `true`      | Modo debug              |
| `USE_REDIS_CACHE`       | `false`     | Usar Redis para cache   |
| `REDIS_HOST`            | `localhost` | Host do Redis           |
| `REDIS_PORT`            | `6379`      | Porta do Redis          |
| `CACHE_TTL`             | `300`       | TTL do cache (segundos) |
| `RATE_LIMIT_PER_MINUTE` | `60`        | Rate limit por minuto   |

### **Cache**

A API suporta dois tipos de cache:

1. **Cache em Memória** (padrão)

   - Rápido para desenvolvimento
   - Dados perdidos ao reiniciar

2. **Redis** (opcional)
   - Persistente entre reinicializações
   - Suporte a múltiplas instâncias

## 🚨 **Rate Limiting**

### **Limites da API do GitHub**

- **Sem token**: 60 requisições/hora
- **Com token**: 5000 requisições/hora

### **Configuração**

```bash
# Adicione seu token GitHub
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

## 📈 **Performance**

### **Benchmarks**

| Operação            | Sem Cache | Com Cache | Melhoria  |
| ------------------- | --------- | --------- | --------- |
| Buscar usuário      | ~800ms    | ~1ms      | **99.9%** |
| Listar repositórios | ~1200ms   | ~2ms      | **99.8%** |
| Buscar linguagens   | ~1500ms   | ~3ms      | **99.8%** |

### **Otimizações**

- 🧠 **Cache inteligente** com TTL configurável
- ⚡ **Requisições assíncronas** com httpx
- 📊 **Logs estruturados** para monitoramento
- 🔄 **Headers de performance** para métricas

## 🤝 **Contribuindo**

### **Como Contribuir**

1. **Fork o projeto**
2. **Crie uma branch** (`git checkout -b feature/nova-funcionalidade`)
3. **Commit suas mudanças** (`git commit -am 'Adiciona nova funcionalidade'`)
4. **Push para a branch** (`git push origin feature/nova-funcionalidade`)
5. **Abra um Pull Request**

### **Padrões de Código**

- 📝 **Documentação**: Docstrings em português
- 🧪 **Testes**: Cobertura mínima de 80%
- 🎨 **Formatação**: Black + Flake8
- 📊 **Logs**: Loguru estruturado

## 📄 **Licença**

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 **Agradecimentos**

- **FastAPI** - Framework web incrível
- **GitHub API** - Dados ricos e bem documentados
- **Render.com** - Deploy gratuito e confiável
- **Comunidade Python** - Ferramentas e bibliotecas

## 📞 **Suporte**

- 📧 **Email**: seu-email@exemplo.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/seu-usuario/git-api/issues)
- 📚 **Documentação**: [Swagger UI](https://github-data-api.onrender.com/docs)

---

**Desenvolvido com ❤️ para facilitar o acesso aos dados do GitHub**

[⬆️ Voltar ao topo](#-github-data-api)
