<p align="center">
  <img src="https://github.com/allisonml/VibeCheckMyProf/blob/main/scratch/image_files/vcmp_logo.png" />
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