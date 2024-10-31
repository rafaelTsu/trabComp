FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt 

ENV DB_URL="sqlite:///usersdb.sqlite3"
ENV ADMIN_USER="brivaldo"
ENV SECRET_KEY="d5zmAsUt3bZdZrBjhcpJ7T2ocQgmVXfM"

EXPOSE 8080

CMD python3 app.py