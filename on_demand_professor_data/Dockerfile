# Dockerfile for on_demand_professor_data

# Use the AWS Lambda Python 3.9 base image
FROM public.ecr.aws/lambda/python:3.9

# Copy shared dependencies and install them
COPY ../shared/requirements.txt .
RUN pip install -r requirements.txt

# Copy the shared code
COPY ../shared /var/task/shared
# Copy on-demand code
COPY . /var/task/on_demand_professor_data

# Copy the specific Lambda function code
COPY on_demand_professor_data/on_demand.py ${LAMBDA_TASK_ROOT}

# Set the handler
CMD ["on_demand.lambda_handler"]