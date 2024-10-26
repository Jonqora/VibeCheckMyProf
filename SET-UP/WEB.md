<p align="center">
  <img src="https://github.com/Jonqora/VibeCheckMyProf/blob/doc-update/scratch/image_files/s3.png" width="50" height="50" />
</p> 

## Web Hosting (S3) and CloudFront

The following steps ensure the correct web hosting set up for the application.
If you encounter any problems with these steps, reach out to `Ellen` or `Allison` with questions. 

### Prerequisites
- know the Invoke URL of the API gateway you are using for the project (created from instructions in [LAMBDA.md](LAMBDA.md))

## Config File

### Set up web files
1. Make sure you are on `main` branch and have pulled recent changes.
2. create a file called `config.js` inside the /web folder
3. paste the following into the file 
```
// config.js

// eslint-disable-next-line no-unused-vars
const config = {
    apiUrl: 'https://your-api-gateway-url.amazonaws.com/prod/vibecheck' // Replace with your actual API Gateway URL
};
```
4. change the URL to match the API gateway used for the project. It should look like (for example) https://mr1pw4hn93.execute-api.ca-central-1.amazonaws.com/dev/sentiment
5. **IMPORTANT** (common error alert!) the invoke url must include the stage (e.g. dev or prod) and the name of the resource (e.g. vibecheck) you created for your API gateway.

## S3 Hosting

### Configure S3 bucket
1. create a new S3 bucket
2. turn off "Block public access" on the bucket permissions 
3. upload all files in /web into the bucket
4. go to the bucket, click on Properties and scroll down to the Static Website Hosting section. Click Edit
5. Enable and enter 'index.html` under Index document. 
6. Click Save changes.

### Make files public
1. go to S3 bucket permissions tab
2. Scroll to Bucket Policy and click Edit
3. add the following policy (replace `your-bucket-name` with the S3 bucket name)
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
1. go to Properties tab of the S3 bucket
2. Under Static Website Hosting, find the endpoint URL. It should look something like
```
http://your-bucket-name.s3-website-region.amazonaws.com
```
3. copy this URL and paste it into the browser to visit the website
4. verify that the website loads and responds correctly when the button is pressed

### Done!


## CloudFront

TODO (Allison to write)