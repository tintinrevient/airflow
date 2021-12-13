FROM python:3.8-slim

RUN python -m pip install click==8.0.3 pandas==1.3.5

COPY rank_ratings.py /usr/local/bin/rank
RUN chmod +x /usr/local/bin/rank

ENV PATH="/usr/local/bin:${PATH}"
