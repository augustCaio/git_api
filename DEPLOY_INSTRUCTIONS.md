# 🚀 **Instruções de Deploy - GitHub Data API**

## 📋 **Visão Geral**

Este documento fornece instruções detalhadas para fazer deploy da GitHub Data API em diferentes ambientes.

## 🎯 **Opções de Deploy**

### 1. 🌐 **Render.com (Recomendado)**

#### **Passo a Passo**

1. **Fork do Repositório**

   ```bash
   # Fork este repositório no GitHub
   # https://github.com/augustCaio/git_api
   ```

2. **Criar Conta no Render**

   - Acesse [render.com](https://render.com)
   - Crie uma conta gratuita
   - Conecte com sua conta GitHub

3. **Criar Novo Web Service**

   - Clique em "New +" → "Web Service"
   - Conecte o repositório forkado
   - Configure as opções:
     - **Name**: `github-data-api`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Configurar Variáveis de Ambiente**

   ```bash
   HOST=0.0.0.0
   PORT=8000
   DEBUG=false
   USE_REDIS_CACHE=false
   CACHE_TTL=300
   RATE_LIMIT_PER_MINUTE=60
   ```

5. **Deploy Automático**
   - Render fará deploy automático
   - URL será: `https://git-api-i3y5.onrender.com`

#### **Vantagens do Render**

- ✅ Deploy gratuito
- ✅ Deploy automático
- ✅ SSL automático
- ✅ Integração com GitHub
- ✅ Logs em tempo real

### 2. 🐳 **Docker + VPS**

#### **Requisitos**

- VPS com Docker instalado
- Domínio (opcional)

#### **Passo a Passo**

1. **Clone o Repositório**

   ```bash
   git clone https://github.com/augustCaio/git_api.git
   cd git-api
   ```

2. **Configurar Variáveis**

   ```bash
   cp config.env.example config.env
   nano config.env
   ```

3. **Build e Deploy**

   ```bash
   # Build da imagem
   docker build -t github-data-api .

   # Executar container
   docker run -d \
     --name github-api \
     -p 80:8000 \
     --env-file config.env \
     github-data-api
   ```

4. **Com Docker Compose**

   ```bash
   # Produção
   docker-compose up -d

   # Desenvolvimento
   docker-compose -f docker-compose.dev.yml up
   ```

### 3. ☁️ **Heroku**

#### **Passo a Passo**

1. **Instalar Heroku CLI**

   ```bash
   # Windows
   winget install --id=Heroku.HerokuCLI

   # macOS
   brew tap heroku/brew && brew install heroku
   ```

2. **Login e Deploy**

   ```bash
   heroku login
   heroku create github-data-api
   git push heroku main
   ```

3. **Configurar Variáveis**
   ```bash
   heroku config:set HOST=0.0.0.0
   heroku config:set PORT=8000
   heroku config:set DEBUG=false
   ```

### 4. 🐙 **GitHub Actions + VPS**

#### **Configuração**

1. **Criar Secrets no GitHub**

   - `SSH_PRIVATE_KEY`
   - `SERVER_HOST`
   - `SERVER_USER`

2. **Workflow GitHub Actions**

   ```yaml
   # .github/workflows/deploy.yml
   name: Deploy to VPS

   on:
     push:
       branches: [main]

   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         - name: Deploy to server
           uses: appleboy/ssh-action@v0.1.5
           with:
             host: ${{ secrets.SERVER_HOST }}
             username: ${{ secrets.SERVER_USER }}
             key: ${{ secrets.SSH_PRIVATE_KEY }}
             script: |
               cd /var/www/git-api
               git pull origin main
               docker-compose up -d --build
   ```

## 🔧 **Configuração de Ambiente**

### **Variáveis de Ambiente**

| Variável          | Padrão      | Descrição                  |
| ----------------- | ----------- | -------------------------- |
| `HOST`            | `127.0.0.1` | Host da aplicação          |
| `PORT`            | `8000`      | Porta da aplicação         |
| `DEBUG`           | `true`      | Modo debug                 |
| `GITHUB_TOKEN`    | -           | Token do GitHub (opcional) |
| `USE_REDIS_CACHE` | `false`     | Usar Redis para cache      |
| `REDIS_HOST`      | `localhost` | Host do Redis              |
| `REDIS_PORT`      | `6379`      | Porta do Redis             |
| `CACHE_TTL`       | `300`       | TTL do cache (segundos)    |

### **Configuração de Cache**

#### **Cache em Memória (Padrão)**

```bash
USE_REDIS_CACHE=false
CACHE_TTL=300
```

#### **Redis (Recomendado para Produção)**

```bash
USE_REDIS_CACHE=true
REDIS_HOST=your-redis-host
REDIS_PORT=6379
REDIS_PASSWORD=your-password
CACHE_TTL=300
```

## 📊 **Monitoramento**

### **Health Check**

```bash
curl https://your-domain.com/api/v1/health
```

### **Logs**

```bash
# Render.com
# Acesse o dashboard do Render

# Docker
docker logs github-api

# VPS
journalctl -u github-api -f
```

### **Métricas**

```bash
# Cache stats
curl https://your-domain.com/api/v1/cache/stats

# Performance headers
curl -I https://your-domain.com/api/v1/health
```

## 🔒 **Segurança**

### **Rate Limiting**

```bash
# Configurar rate limit
RATE_LIMIT_PER_MINUTE=60
```

### **CORS**

```bash
# Configurar CORS
CORS_ORIGINS=["https://your-domain.com"]
```

### **HTTPS**

- Render.com: Automático
- VPS: Configure Nginx + Let's Encrypt
- Heroku: Automático

## 🚨 **Troubleshooting**

### **Problemas Comuns**

#### **1. API não responde**

```bash
# Verificar logs
docker logs github-api

# Verificar health check
curl http://localhost:8000/api/v1/health
```

#### **2. Erro de conexão com GitHub**

```bash
# Verificar token
echo $GITHUB_TOKEN

# Testar API do GitHub
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user
```

#### **3. Cache não funciona**

```bash
# Verificar Redis
redis-cli ping

# Verificar configuração
curl http://localhost:8000/api/v1/cache/stats
```

#### **4. Deploy falha no Render**

```bash
# Verificar build logs
# Acesse o dashboard do Render

# Verificar requirements.txt
pip install -r requirements.txt
```

### **Logs de Debug**

```bash
# Habilitar debug
DEBUG=true

# Ver logs detalhados
tail -f logs/app.log
```

## 📈 **Escalabilidade**

### **Horizontal Scaling**

```bash
# Docker Swarm
docker stack deploy -c docker-compose.yml github-api

# Kubernetes
kubectl apply -f k8s/
```

### **Load Balancer**

```bash
# Nginx
upstream github_api {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}
```

## 🎯 **Próximos Passos**

1. **Configurar domínio personalizado**
2. **Implementar autenticação**
3. **Adicionar métricas avançadas**
4. **Configurar backup automático**
5. **Implementar CI/CD completo**

---

**🎉 Deploy realizado com sucesso!**

Acesse sua API em: `https://your-domain.com`
Documentação: `https://your-domain.com/docs`

**📞 Suporte**: Abra uma issue no GitHub para dúvidas.
