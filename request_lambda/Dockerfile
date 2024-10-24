FROM public.ecr.aws/lambda/python:3.8

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["app.app.lambda_handler"]
