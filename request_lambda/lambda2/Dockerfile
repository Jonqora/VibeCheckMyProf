FROM public.ecr.aws/lambda/python:3.9

COPY lambda2/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY common /var/task/request_lambda/common
COPY lambda2 /var/task/request_lambda/lambda2

CMD ["request_lambda.lambda2.app.lambda_handler"]
