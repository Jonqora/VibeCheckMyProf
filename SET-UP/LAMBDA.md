<p align="center">
  <img src="https://github.com/Jonqora/VibeCheckMyProf/blob/main/scratch/image_files/lambda.png" width="50" height="50" />
</p> 

## Lambda and API Gateway

The following steps ensure correct setup of the containerized lambda that serves as the backend computing layer of the project. If you encounter any problems with these steps, reach out to `Ellen` with questions. 

## Containerized Lambda

### Download model

**IMPORTANT:** If you are rebuilding from a previous app version, you can move the previously downloaded models from `request_lambda/app/models` to `request_lambda/lambda2/models`.

1. Make sure you are on the main branch and have pulled recent changes.
2. Navigate to the `/request_lambda` directory and find the `download_model.py` script
3. Run the script to download the model (the most recent model we are using is `jitesh/emotion-english`).
4. The models will be saved in the `/request_lambda/lambda2` directory.

### Build Container

1. Create ECR repositories for `vibe-check-my-prof-lambda1` and `vibe-check-my-prof-lambda2`.
2. Make sure you are on main branch and have pulled recent changes.
3. From the project root directory, build containers for lambda 1 and lambda 2:
```
docker build -t vibe-check-my-prof-lambda1 -f request_lambda/lambda1/Dockerfile request_lambda 
```
```
docker build -t vibe-check-my-prof-lambda2 -f request_lambda/lambda2/Dockerfile request_lambda 
```

### Store in ECR
1. Use the Push Commands from each repository to authenticate, tag your containers and push. E.g.
```
docker tag vibe-check-my-prof-lambda1 345594593730.dkr.ecr.ca-central-1.amazonaws.com/vibe-check-my-prof-lambda1:latest

docker push 345594593730.dkr.ecr.ca-central-1.amazonaws.com/vibe-check-my-prof-lambda1:latest
```
3. Tag and push to both repositories

### Create Lambda1
1. Create a new Lambda and choose Container image option

**IMPORTANT:** If rebuilding from a previous version, you can reuse your old lambda that is connected to the API Gateway

2. Name it and choose the `vibe-check-my-prof-lambda1` container image you just uploaded (or upload a new container image)
3. **IMPORTANT** choose arm64 if you are using a mac. Otherwise, leave it on x86_64. Now create the function. Click Deploy
4. Under the `Configuration` tab, select `General configuration` and set the **memory** to 128MB and the **timeout** to 30 seconds. 
5. Under the `Configuration` tab, select `Environment variables` and add all the variables from the project's `infra/config.env` file.
6. Under the `Configuration` tab, select `RDS databases` and `Connect to RDS database`.
   - Use an existing database.
   - In the `RDS database` dropdown, select our project's database (i.e. `vibecheckmyprofdb`).
   - Select `Create`.
   - Wait for AWS to create the necessary security groups and update the lambda function.

**IMPORTANT** If you get an error about "request violates the limit on number of VPC security groups associated with a DB instance" then: 1) remove all security groups from the DB, 2) Attach the Lambda to the DB, 3) re-run `terraform apply`

7. Under the `Configuration` tab, select `VPC` and `Edit`.
   - Under `Subnets` select all available **PRIVATE** subnets 
   - Make sure each subnet has a 0.0.0.0/0 route to a NAT gateway
   - Remove any subnets that are **PUBLIC**
   - In the `Security groups` dropdown, add the one named `vcmp-lambda-sg`.
   - Select `Save` and wait for the lambda function to finish updating.

### Create Lambda2
1. Create a new Lambda and choose Container image option
2. Name it and choose the `vibe-check-my-prof-lambda2` container image
3. **IMPORTANT** choose arm64 if you are using a mac. Otherwise, leave it on x86_64. Now create the function. Click Deploy
4. Under the `Configuration` tab, select `General configuration` and set the **memory** to 3008MB and the **timeout** to 3 minutes. 
5. Under the `Configuration` tab, select `Environment variables` and add all the variables from the project's `infra/config.env` file.
6. Do `Connect to RDS database`folowing instructions above for the previous lambda
7. Edit the VPC and subnets following instructions above for the previous lambda

#### Add Amazon Comprehend Permissions
1. Open the IAM console in AWS.
2. Select **Roles** from the sidebar on the left.
3. In the search bar, type the name of the Lambda2 function you just created. Click on the role name to open it.
5. On the new page, go to the **Permissions** tab, click **Add permissions**, and select **Attach policies**.
6. In the search bar, type `ComprehendReadOnly`, check the box next to it, and click **Add permissions**.
7. The permission is now added to the role, allowing the Lambda function to call Amazon Comprehend.

#### Add Lambda invoke permissions
1. Navigate to IAM, roles
2. search for vibe-check-my-prof-lambda1-role (or the name of your first lambda function)
3. Add permissions, create inline policy
4. Select lambda
5. Search for InvokeFunction
6. Resource: specific, add arns
7. Enter ca-central-1 in region and vibe-check-my-prof-lambda2 (or your second function name) in the function name
8. Click Add ARNs and click Next
9. Name the policy and click create policy

## Testing the Lambdas
You can test the first Lambda1 with the following test events. Lambda1 will trigger Lambda2, so you can check CloudWatch logs for Lambda2.

```
{
  "url": "https://ratemyprofessors.com/professor/1835982"
}
```
```
{
  "url": "https://www.ratemyprofessors.com/professor/12345"
}
```
```
{
  "url": "https://www.NOTratemyprof.com/professor/1835982"
}
```
Try other professors to see different responses.

## API Gateway

### Create API Gateway
1. Navigate to API Gateway console and click Create API
2. Click on Build next to REST API
3. give the API a name and click Create API

### Create Resource
1. under Resources in the left panel, select Create Resource
2. name the resource (e.g. vibecheck) and create
3. with your new resource selected, select Create Method
4. select POST from the dropdown and choose Lambda function
5. choose the correct region and choose the Lambda function you built in the previous steps
6. leave the other defaults and Save

### Enable CORS
1. click on your Resource again (above the POST item) and click on Enable CORS under Resource Details
2. select the checkbox for POST and click Save

### Deploy API Gateway
1. click on Deploy API
2. choose \[New Stage\] and name the stage (e.g. dev or prod)
3. click Deploy
4. Note the Invoke URL shown on the page after deploying.
5. **IMPORTANT** the Invoke URL displayed after deploying is incomplete. You will need to add a slash and the name of your resource at the end. For example:
    - displayed Invoke URL: https://1x34oeu2ye.execute-api.ca-central-1.amazonaws.com/dev
    - complete: https://1x34oeu2ye.execute-api.ca-central-1.amazonaws.com/dev/vibecheck
6. Note the **complete** Invoke URL and save it somewhere. You will use it for next steps in [WEB.md](WEB.md).
