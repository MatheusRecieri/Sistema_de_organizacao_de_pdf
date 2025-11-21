# Etapa 1: Build
FROM node:20 AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Etapa 2: Servindo conteúdo static com Nginx
FROM nginx:alpine

COPY --from=build /app/out ./nginx/nginx.conf:/etc/nginx/nginx.conf

EXPOSE 80
