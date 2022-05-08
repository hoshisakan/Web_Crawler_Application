FROM nginx

RUN cd / && ln -sf /usr/share/zoneinfo/Asia/Taipei /etc/localtime
RUN rm /etc/nginx/conf.d/default.conf
# COPY define/proxy_params /etc/nginx/
COPY uwsgi_params /etc/nginx/