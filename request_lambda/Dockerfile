FROM public.ecr.aws/lambda/python:3.9

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY app /var/task/request_lambda/app

CMD ["request_lambda.app.app.lambda_handler"]
