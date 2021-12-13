FROM python:3.8-slim

RUN python -m pip install pandas==1.3.5 flask==2.0.2 flask-httpauth==4.5.0 gunicorn==20.1.0

COPY serve_ratings.py /serve_ratings.py
COPY ratings.csv /data/ratings.csv
ENV API_USER="admin"
ENV API_PASSWORD="admin"

EXPOSE 5000
ENTRYPOINT ["gunicorn"]
CMD ["--bind", "0.0.0.0:5000", "serve_ratings:app"]
