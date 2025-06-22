FROM python:3.11-slim

WORKDIR /app

RUN pip install psycopg2-binary

COPY load_data.py .
COPY products_list.csv .
COPY purchases.csv .

CMD ["python3", "load_data.py"]