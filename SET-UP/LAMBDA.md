<p align="left">
  <img src="https://github.com/Jonqora/VibeCheckMyProf/blob/doc-update/scratch/image_files/lambda.png" width="600" height="400" />
</p>


The following are ensure the lambda functionality of the project.

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