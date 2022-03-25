FROM python:3.8-slim-buster

COPY requirements.txt /tmp/

RUN apt-get update && apt-get install -y curl libpq-dev gcc python-dev supervisor nginx && \
  mkdir -p /etc/nginx/ssl/ && \
  openssl req \
          -x509 \
          -subj "/C=US/ST=Massachusetts/L=Cambridge/O=Dis" \
          -nodes \
          -days 365 \
          -newkey rsa:2048 \
          -keyout /etc/nginx/ssl/nginx.key \
          #-addext "subjectAltName=DNS:localhost" \
          -out /etc/nginx/ssl/nginx.cert && \
  chmod -R 755 /etc/nginx/ssl/ && \
  pip install --upgrade pip && \
  pip install gunicorn && \
  pip install --upgrade --force-reinstall -r /tmp/requirements.txt -i https://pypi.org/simple/ --extra-index-url https://test.pypi.org/simple/ &&\
  groupadd -r -g 55020 appuser && \
  useradd -u 55020 -g 55020 --create-home appuser

# Supervisor to run and manage multiple apps in the same container
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy code into the image
COPY --chown=appuser . /home/appuser

RUN rm -f /etc/nginx/sites-enabled/default && \
    rm -f /etc/service/nginx/down && \
    mkdir -p /data/nginx/cache && \
    mv /home/appuser/webapp.conf.example /etc/nginx/conf.d/webapp.conf && \
    chown appuser /etc/ssl/certs && \
    chown appuser /etc/ssl/openssl.cnf && \
    chown -R appuser /var/log/nginx && \
    chown -R appuser /var/lib/nginx && \
    chown -R appuser /data && \
    chown -R appuser /run

WORKDIR /home/appuser
USER appuser

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
