FROM python:3.8-slim
WORKDIR /usr/app

RUN apt-get update \
  && apt-get install -y texlive-pictures texlive-fonts-recommended texlive-latex-extra \
  && python3 -m pip install --upgrade pip setuptools

COPY . /usr/app/
RUN python3 -m pip install .

ENV PYTHONPATH /usr/app
ENTRYPOINT ["perprof"]
