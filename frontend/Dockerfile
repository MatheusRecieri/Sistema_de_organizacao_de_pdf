# Stage 1 - Build do Frontend
FROM node:18-alpine as build
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2 - Nginx
FROM nginx:stable-alpine

COPY --from=build /app/out ./nginx/nginx.conf:/etc/nginx/nginx.conf

EXPOSE 80
