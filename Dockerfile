FROM python:3.10-slim

WORKDIR /src

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "src/main.py"]