<p align="center">
  <img src="https://github.com/Jonqora/VibeCheckMyProf/blob/doc-update/scratch/image_files/lambda.png" width="50" height="50" />
</p> 

## Lambda and API Gateway

The following steps ensure correct setup of the containerized lambda that serves as the backend computing layer of the project. If you encounter any problems with these steps, reach out to `Ellen` with questions. 

## Containerized Lambda

### Build Container

1. Make sure you are on main branch and have pulled recent changes.
2. Navigate to the `/request_lambda` directory and make sure Docker is running
3. Build the container
```
docker build -t vibe-check-my-prof .
```

### Store in ECR
1. Navigate to ECR console and create a repository called `vibe-check-my-prof`.
2. Use the URI from the repository, tag your container and push. E.g.
```
docker tag vibe-check-my-prof 345594593730.dkr.ecr.ca-central-1.amazonaws.com/vibe-check-my-prof:latest

docker push 345594593730.dkr.ecr.ca-central-1.amazonaws.com/vibe-check-my-prof:latest
```

### Create Lambda
1. Create a new Lambda and choose Container image option
2. Name it and choose the container image you just uploaded, then create function
3. Deploy
4. You can test the Lambda with the following test events:
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
5. **IMPORTANT** the Invoke URL displayed after deploying is incomplete. You will need to add a slash and the dame of your resource at the end. For example:
    - displayed Invoke URL: https://1x71oeu2ye.execute-api.ca-central-1.amazonaws.com/dev
    - complete: https://1x71oeu2ye.execute-api.ca-central-1.amazonaws.com/dev/vibecheck
6. Note the **complete** Invoke URL and save it somewhere. You will use it for next steps in [WEB.md](WEB.md).