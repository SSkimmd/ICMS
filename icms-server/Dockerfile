FROM python
WORKDIR /icms-server
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8081", "webserver:StartWebServer()"]