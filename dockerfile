FROM python:3.14-slim
WORKDIR /app


COPY requiremets.txt .
RUN pip install  --no-cache-dir -r requiremets.txt

COPY . .

CMD ["python", "main.py"]