FROM nginx:latest

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./nginx-dev.conf /etc/nginx/nginx-dev.conf
COPY ./start_nginx.sh /usr/local/bin/start_nginx.sh

RUN chmod +x /usr/local/bin/start_nginx.sh

EXPOSE 80
EXPOSE 443

CMD [ "/usr/local/bin/start_nginx.sh" ]