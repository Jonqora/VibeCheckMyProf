<p align="center">
    <img src="https://github.com/Jonqora/VibeCheckMyProf/blob/doc-update/scratch/image_files/RDS.png" width="50" height="50" />
</p> 

##  Database and Security

If you encounter any problems with the steps in this document, reach out to `Colleen` with questions. 


## Database: AWS RDS Database

The following steps ensure the correct set up for your AWS RDS Database.

The `infra` directory contains Terraform scripts that will create an AWS RDS Database. For more information about the 
configuration variables used in the scripts, see Terraform's [documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_instance)
on the `aws_db_instance` resource.

### Prerequisites
1. Install [Terraform](https://developer.hashicorp.com/terraform/install) version 1.9.8.
   - **macOS**: Install via `brew tap hashicorp/tap | brew install hashicorp/tap/terraform`
   - **Windows**: Install via `chocolatey install terraform`
   - **Linux**: Download the binary from Terraform's [official site](https://developer.hashicorp.com/terraform/install#linux).

2. Ensure AWS credentials are configured:
   - Via your AWS credentials file `~/.aws/credentials`
   - Or by exporting the following environment variables by running these commands in your terminal (for Linux/macOS):
```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_SESSION_TOKEN="your-access-token"
```

### Create the DB Instance with Terraform
Now you're ready to use Terraform!

#### 1. Initialize Terraform
Move (cd) into the directory containing the `main.tf` file, and run the following command to initialize Terraform:
```bash
terraform init
```
This will download the AWS provider and set up your working directory.

#### 2. Plan the Terraform Execution
You can see what Terraform will do _before_ making changes by running:
```bash
terraform plan
```
This will output all the actions Terraform will take to create the RDS instance. **Upon execution, you will be prompted to 
provide values for the following variables:**
- `cidr_block`: Your IP address so your local machine can communicate with the created database. 
  - e.g. `38.13.78.95/32`
- `database_password`: Master password you want to set for authenticating to the database. 
  - Minimum constraints: At least 8 printable ASCII characters. Can't contain any of the following symbols: / ' " @

These variable values will be automatically applied to the instance configuration upon execution.

#### 3. Apply the Terraform Configuration
To create the RDS instance, run:
```bash
terraform apply
```
See the above information about the prompted variable values. Terraform will ask for confirmation before applying the changes. Type `yes` to proceed.

Once Terraform has finished applying the configuration, it will output the **RDS endpoint**. You can use this endpoint 
to connect to the database. Note: it may take a few minutes for this step to complete.

### Cleanup (Optional)
If you want to destroy the RDS instance, you can use:
```bash
terraform destroy
```
This will remove **all** the resources created by Terraform, including the RDS instance and security group.

### Terraform FAQ
[This documentation](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/aws-build) provides more 
information about the aws resource build executed by Terraform. It also contains helpful commands you can use to debug or 
leverage more of Terraform's available tooling.

#### Terraform is getting frozen with no output
You can enable detailed logs to appear on stderr which is helpful for debugging by setting the following environment variable:
```bash
export TF_LOG=trace
```

#### Error: Failed to load plugin schemas
You may need to grant exec permissions to the providers with something similar to the following command (for example):
```bash
chmod +x .terraform/providers/registry.terraform.io/hashicorp/aws/5.32.1/darwin_amd64/terraform-provider-aws_v5.32.1_x5
```
This [stackoverflow](https://stackoverflow.com/questions/70407525/terraform-gives-errors-failed-to-load-plugin-schemas)
QA may be helpful to resolve the issue.

#### Error: timeout while waiting for plugin to start
This could be due to the Terraform plugin cache becoming full or corrupted. 
Try clearing the plugin cache and forcing Terraform to download the specified version of the plugins by running:
```bash
terraform init -upgrade
```

## Security
### Secrets Manager
Our application leverages [AWS Secrets Manager](https://ca-central-1.console.aws.amazon.com/secretsmanager/landing?region=ca-central-1)
to encrypt and securely store the password for authentication to the RDS database. 

Terraform will create a username and password, which our application services can fetch 
for authenticating to the rds database. This prevents us from having to hard-code secret values in the application code. 

Below is sample code you can add to your function to fetch and use the database password from the secret manager:
```python
import boto3
from botocore.exceptions import ClientError


def get_secret():

    secret_name = "my-super-db-secret" # Replace with the secret name
    region_name = "ca-central-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']

    # The rest of your code goes here.
```
### IAM Roles
IAM roles are defined and assigned to policies throughout our application. They define how different resources are 
allowed to interact with each other (e.g. such as reading from the database, writing, etc.). 
- `lambda-rds-access-role`: IAM role for lambda function to access RDS database.
- `ec2-rds-access-role`: IAM role for EC2 to access RDS database.
- `lambda-s3-access-role`: IAM role for Lambda to retrieve and put objects in S3 storage bucket.

The appropriate role should be applied to your portion of the application service.