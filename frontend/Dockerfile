# Stage 1 - Build do Frontend
FROM node:18-alpine as build
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2 - Nginx
FROM nginx:stable-alpine

COPY --from=build /app/out /usr/share/nginx

EXPOSE 80
