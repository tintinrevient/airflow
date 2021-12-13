FROM python:3.8-slim

RUN python -m pip install click==8.0.3 requests==2.26.0

COPY get_ratings.py /usr/local/bin/get
RUN chmod +x /usr/local/bin/get

ENV PATH="/usr/local/bin:${PATH}"
