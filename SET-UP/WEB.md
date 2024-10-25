<p align="center">
  <img src="https://github.com/Jonqora/VibeCheckMyProf/blob/doc-update/scratch/image_files/s3.png" width="50" height="50" />
</p> 

## Web Hosting: S3 Option

The following steps ensure the correct web hosting set up for the application.

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