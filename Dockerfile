FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN mkdir -p /app/logs && chmod 777 /app/logs
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
