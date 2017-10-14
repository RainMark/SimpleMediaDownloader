FROM python:3-alpine
COPY ./ /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "src/SimpleMediaDownloader.py", "-p", "8000"]
