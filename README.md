<p align="center">
  <img src="https://github.com/Jonqora/VibeCheckMyProf/blob/main/scratch/image_files/vcmp_logo.png" />
</p>

VibeCheckMyProf is a service that performs sentiment analysis on reviews for professors on the site **ratemyprofessors.com**, providing users with an appealing visual summary of recent reviews without having to scroll and read all of them. Users can compare the VibeCheck score with numerical ratings on the ratemyprofessors site and can also view a visualization of VibeCheck comment scores over time.


Use Cases:
1. A first year anxious student cannot decide which Math Professor to take a math course with, they learn about VibeCheckMyProf to get an overview of each professor’s reviews without having to read any comments.
2. A CPSC professor wants to know what recent students think of them, so they use VibeCheckMyProf at the beginning of the semester and at the end to track how feedback has shifted over time.
3. A student in their final year realizes they need an elective outside of their major, with limited time and familiarity with other department's professors, they use VibeCheckMyProf to compare overall scores of potential professors, making quick decisions without having to read individual comments.


Visual Guide: link...


## Team

- Ellen Lloyd `API/web scraping` `front end` `documentation`
- Allison Luna `front end` `data viz` `report writing`
- Simon Liang `API/web scraping` `sentiment analysis` `database`
- Sadia Khan Durani `sentiment analysis` `data viz` `documentation` `report writing`
- Colleen Rideout `database` `data viz` `security`

### Role specializations
1. `API/web scraping` Ellen, Simon
2. `sentiment analysis` Simon, Sadia
3. `database` Colleen, Simon
4. `front end` Ellen, Allison
5. `data viz/dashboards` Colleen, Allison, Sadia
6. `security & extras` Colleen
7. `documentation` Ellen, Sadia
8. `report writing` Sadia, Allison

# VibeCheckMyProf Setup
Introductory text

## Prerequisites
- an AWS account
- ...

## Steps
- Steps go here, provision AWS resources, use files, etc.

## Sentiment Lambda
### Dummy function set up
- create a new Lambda
- in Code source, copy and paste the contents of `/lambda_sentiment/dummy.py`
- Deploy
- you can test the Lambda with the following test events:
```
{
  "url": "https://www.ratemyprofessors.com/professor/12345"
}
```
```
{
  "url": "https://www.NOTratemyprof.com/professor/12345"
}
```

### API Gateway setup
- Go to API Gateway and click Create API
- Click on Build next to REST API
- give the API a name and click Create API
- under Resources in the left panel, select Create Resource
- name the resource (e.g. sentiment) and create
- with your new resource selected, select Create Method
- select POST from the dropdown and choose Lambda function
- choose the correct region and the Lambda function from earlier
- leave the other defaults and Save
- click on your Resource again and Enable CORS under Resource Details
- select the checkbox for POST and click Save
- click on Deploy API
- choose \[New Stage\] and name the stage (e.g. dev or prod)
- click Deploy
- Note the Invoke URL and save it for later

## Web Hosting: S3 Option
### Prerequisites
- know the Invoke URL of the first API gateway you are using for the project 

### Set up web files
- create a file called config.js inside the /web folder
- paste the following into the file 
```
// config.js

// eslint-disable-next-line no-unused-vars
const config = {
    apiUrl: 'https://your-api-gateway-url.amazonaws.com/prod/vibecheck' // Replace with your actual API Gateway URL
};
```
- change the URL to match the first API gateway used for the project. Don't forget the Stage and Resource
- it should look like (for example) https://mr3pw5hn93.execute-api.ca-central-1.amazonaws.com/dev/sentiment


### Configure S3 bucket
- create a new S3 bucket
- turn off "Block public access" on the bucket permissions 
- upload all files in /web into the bucket
- go to the bucket, click on Properties and scroll down to the Static Website Hosting section. Click Edit
- Enable and enter 'index.html` under Index document. 
- Click Save changes.

### Make files public
- go to S3 bucket permissions tab
- Scroll to Bucket Policy and click Edit
- add the following policy (replace `your-bucket-name` with the S3 bucket name)
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}
```

### Get the S3 website URL
- go to Properties tab of the S3 bucket
- Under Static Website Hosting, find the endpoint URL. It should look something like
```
http://your-bucket-name.s3-website-region.amazonaws.com
```
- copy this URL and paste it into the browser to visit the website
- verify that the website loads and responds when the button is pressed

## Web Hosting: EC2 Option
### Prerequisites
- know the Invoke URL of the first API gateway you are using for the project 
### Next steps
Steps here...

## Database: AWS RDS Database
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
