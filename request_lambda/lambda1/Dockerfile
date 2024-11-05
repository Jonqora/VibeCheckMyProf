FROM public.ecr.aws/lambda/python:3.9

COPY lambda1/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY common /var/task/request_lambda/common
COPY lambda1 /var/task/request_lambda/lambda1

CMD ["request_lambda.lambda1.app.lambda_handler"]
