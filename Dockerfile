FROM python:3

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN export $(cat .env | xargs)
RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]
