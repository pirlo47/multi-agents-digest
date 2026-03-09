FROM python:3.10-slim 
WORKDIR /app
# Handle dependencies at build time, not runtime
COPY requirements.txt . 
RUN pip install --no cache-dir -r requirements.txt 
COPY app.py . 
CMD ["python", "app.py"]

