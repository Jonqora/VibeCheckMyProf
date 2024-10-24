FROM public.ecr.aws/lambda/python:3.8

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY __init__.py .
COPY app.py .
COPY database.py .
COPY frontend.py .
COPY rmp_api.py .
COPY sentiment.py .

CMD ["app.lambda_handler"]
