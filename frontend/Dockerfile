# Этап сборки (builder)
FROM node:18-alpine AS builder
WORKDIR /app
RUN npm install -g npm@10.8.1
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build

# Этап Caddy
FROM caddy:2-alpine
WORKDIR /app
COPY --from=builder /app/dist /app/dist
COPY Caddyfile /etc/caddy/Caddyfile
