# 🚀 **Guia de Deploy - GitHub Data API**

## 📋 **Visão Geral**

Este guia detalha como fazer deploy da GitHub Data API em diferentes ambientes, incluindo configurações de cache, monitoramento e performance.

## 🐳 **Deploy com Docker**

### **Pré-requisitos**

- Docker e Docker Compose instalados
- Git configurado

### **Desenvolvimento Local**

```bash
# Clone o repositório
git clone <seu-repositorio>
cd git_api

# Executar com cache em memória
docker-compose -f docker-compose.dev.yml up

# Executar com Redis (opcional)
docker-compose -f docker-compose.dev.yml --profile redis-dev up
```

### **Produção**

```bash
# Build da imagem
docker build -t github-data-api .

# Execução simples
docker run -p 8000:8000 github-data-api

# Execução com docker-compose (recomendado)
docker-compose up -d
```

### **Variáveis de Ambiente**

Crie um arquivo `.env` ou configure as variáveis:

```bash
# Configurações básicas
HOST=0.0.0.0
PORT=8000
DEBUG=false

# Cache
USE_REDIS_CACHE=true
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your_secure_password
CACHE_TTL=300

# GitHub (opcional)
GITHUB_TOKEN=your_github_token

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
```

## ☁️ **Deploy na Render.com**

### **Configuração Automática**

O projeto inclui configuração completa para Render.com:

1. **render.yaml** - Define serviços e configurações
2. **Procfile** - Comando de inicialização
3. **runtime.txt** - Versão do Python

### **Passos para Deploy**

1. **Conecte seu repositório**:

   - Acesse [render.com](https://render.com)
   - Conecte sua conta GitHub
   - Selecione o repositório

2. **Configure o serviço**:

   - Tipo: Web Service
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Variáveis de ambiente**:

   ```bash
   HOST=0.0.0.0
   PORT=8000
   DEBUG=false
   USE_REDIS_CACHE=false
   CACHE_TTL=300
   RATE_LIMIT_PER_MINUTE=60
   ```

4. **Health Check**:
   - Path: `/api/v1/health`
   - Interval: 30s
   - Timeout: 10s

### **Redis na Render (Opcional)**

Para usar Redis na Render:

1. Crie um serviço Redis:

   - Tipo: Redis
   - Plano: Free (ou pago para produção)

2. Configure as variáveis:
   ```bash
   USE_REDIS_CACHE=true
   REDIS_HOST=<redis-service-url>
   REDIS_PORT=6379
   REDIS_PASSWORD=<redis-password>
   ```

## 🔧 **Deploy Manual**

### **VPS/Server**

```bash
# Instalar dependências
sudo apt update
sudo apt install python3 python3-pip redis-server

# Clone e configure
git clone <repositorio>
cd git_api
pip3 install -r requirements.txt

# Configurar Redis
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Executar com systemd
sudo cp github-data-api.service /etc/systemd/system/
sudo systemctl enable github-data-api
sudo systemctl start github-data-api
```

### **Arquivo systemd (github-data-api.service)**

```ini
[Unit]
Description=GitHub Data API
After=network.target redis.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/git_api
Environment=PATH=/path/to/git_api/venv/bin
ExecStart=/path/to/git_api/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## 📊 **Monitoramento**

### **Health Check**

```bash
# Verificar status da API
curl https://your-api.render.com/api/v1/health

# Verificar cache
curl https://your-api.render.com/api/v1/cache/stats
```

### **Logs**

```bash
# Logs da aplicação
tail -f logs/app.log

# Logs de erro
tail -f logs/error.log

# Logs de performance
tail -f logs/performance.log
```

### **Métricas**

- **Tempo de resposta**: Headers `X-Response-Time`
- **Cache hit/miss**: Endpoint `/api/v1/cache/stats`
- **Status da API**: Endpoint `/api/v1/health`

## 🔒 **Segurança**

### **Produção**

1. **HTTPS**: Sempre use HTTPS em produção
2. **Rate Limiting**: Configure limites apropriados
3. **CORS**: Restrinja origens permitidas
4. **Tokens**: Use tokens GitHub apenas quando necessário

### **Variáveis Sensíveis**

```bash
# Nunca commite estas variáveis
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
REDIS_PASSWORD=your_secure_password
SECRET_KEY=your_secret_key
```

## 🚨 **Troubleshooting**

### **Problemas Comuns**

1. **API não inicia**:

   ```bash
   # Verificar logs
   docker logs <container-id>

   # Verificar portas
   netstat -tulpn | grep 8000
   ```

2. **Cache não funciona**:

   ```bash
   # Verificar Redis
   redis-cli ping

   # Verificar configurações
   curl /api/v1/cache/stats
   ```

3. **Health check falha**:

   ```bash
   # Verificar endpoint
   curl /api/v1/health

   # Verificar logs
   tail -f logs/error.log
   ```

### **Performance**

1. **Cache**: Monitore hit/miss ratio
2. **Logs**: Verifique tempo de resposta
3. **Rate Limiting**: Ajuste conforme necessário

## 📈 **Escalabilidade**

### **Horizontal Scaling**

- Use load balancer
- Configure múltiplas instâncias
- Use Redis compartilhado

### **Vertical Scaling**

- Aumente recursos da máquina
- Otimize configurações de cache
- Monitore uso de memória

## 🔄 **CI/CD**

### **GitHub Actions**

```yaml
name: Deploy to Render
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        uses: johnbeynon/render-deploy-action@v0.0.1
        with:
          service-id: ${{ secrets.RENDER_SERVICE_ID }}
          api-key: ${{ secrets.RENDER_API_KEY }}
```

## 📞 **Suporte**

Para problemas ou dúvidas:

1. Verifique os logs da aplicação
2. Teste localmente primeiro
3. Consulte a documentação da API
4. Abra uma issue no repositório
