FROM python:3.10.6

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV PORT=4433

EXPOSE 4433

CMD [ "python3", "kanowatch.py"]