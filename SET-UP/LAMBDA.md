<p align="center">
  <img src="https://github.com/Jonqora/VibeCheckMyProf/blob/main/scratch/image_files/lambda.png" width="50" height="50" />
</p> 

## Lambda and API Gateway

The following steps ensure correct setup of the containerized lambda that serves as the backend computing layer of the project. If you encounter any problems with these steps, reach out to `Ellen` with questions. 

## Containerized Lambda

### Download model
1. Make sure you are on the main branch and have pulled recent changes.
2. Navigate to the `/request_lambda` directory and find the `download_model.py` script
3. Run the script to download the model (the most recent model has been used in `jitesh/emotion-english`).
4. The model will be saved in the `/request_lambda/app` directory.

### Build Container

1. Make sure you are on main branch and have pulled recent changes.
2. Navigate to the `/request_lambda` directory and make sure Docker is running
3. Build the container
```
docker build -t vibe-check-my-prof .
```

### Store in ECR
1. Navigate to ECR console and create a repository called `vibe-check-my-prof` with default settings.
2. Use the URI from the repository, tag your container and push. E.g.
```
docker tag vibe-check-my-prof 345594593730.dkr.ecr.ca-central-1.amazonaws.com/vibe-check-my-prof:latest

docker push 345594593730.dkr.ecr.ca-central-1.amazonaws.com/vibe-check-my-prof:latest
```
3. You may need to set an access token and/or run the authentication token from "View push commands" before pushing the image.

### Create Lambda
1. Create a new Lambda and choose Container image option
2. Name it and choose the container image you just uploaded
3. **IMPORTANT** choose arm64 if you are using a mac. Otherwise, leave it on x86_64. Now create the function.
3. Deploy
4. Under the `Configuration` tab, select `General configuration` and set the **memory** to 3008MB and the **timeout** to 2 minutes. 
5. Under the `Configuration` tab, select `Environment variables` and add all the variables from the project's `infra/config.env` file
6. Under the `Configuration` tab, select `RDS databases` and `Connect to RDS database`
   - Use an existing database
   - In the `RDS database` dropdown, select our project's database (i.e. `vibecheckmyprofdb`)
   - Select `Create`
   - Wait for AWS to create the necessary security groups and update the lambda function
7. You can test the Lambda with the following test events:

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

## Add Amazon Comprehend Permissions

### Steps to Add Permissions to the IAM Role:
1. Open the IAM console in AWS.
2. Select **Roles** from the sidebar on the left.
3. In the search bar, type the name of the Lambda function you just created.
4. Click on the role name to open it.
5. On the new page, go to the **Permissions** tab, click **Add permissions**, and select **Attach policies**.
6. In the search bar, type `ComprehendReadOnly`, check the box next to it, and click **Add permissions**.
7. The permission is now added to the role, allowing the Lambda function to call Amazon Comprehend.

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
