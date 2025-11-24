# Usa a imagem oficial do nginx
FROM nginx:stable-alpine

# Remove possíveis confs padrão do nginx
RUN rm -rf /etc/nginx/conf.d/default.conf

# Copia seu arquivo nginx.conf para dentro da imagem
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copia o build estático do frontend para a pasta padrão do nginx
# (garanta que você gerou seu build antes de rodar docker build)
COPY ./dist/ /usr/share/nginx/html/

# Libera portas
EXPOSE 80
