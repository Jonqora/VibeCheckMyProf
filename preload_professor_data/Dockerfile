# Dockerfile for preload_professor_data

# Use the AWS Lambda Python 3.9 base image
FROM public.ecr.aws/lambda/python:3.9

# Copy shared dependencies and install them
COPY ../shared/requirements.txt .
RUN pip install -r requirements.txt

# Copy the shared code
COPY ../shared /var/task/shared
# Copy preload code
COPY . /var/task/preload_professor_data

# Copy the specific Lambda function code
COPY preload_professor_data/preload.py ${LAMBDA_TASK_ROOT}

# Set the handler
CMD ["preload.lambda_handler"]