# Stage 1 - Build do Frontend
FROM node:18-alpine as build
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2 - Nginx
FROM nginx:stable-alpine

RUN rm -rf /etc/nginx/conf.d/nginx.conf
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

# ⬇️ Ajuste aqui conforme seu build (dist ou build)
COPY --from=build ./frontend/out: /usr/share/nginx/html

EXPOSE 80
