<p align="center">
  <img src="https://github.com/Jonqora/VibeCheckMyProf/blob/main/scratch/image_files/s3.png" width="50" height="50" />
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
2. turn off "Block all public access" on the bucket permissions and acknowledge the warning
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

To add additional security to our S3 bucket and provide quicker and more cost-efficient service to users, we will be using Cloudfront.

1. Open up the CloudFront console in AWS and click "Create distribution"
2. Create your distribution with the following settings:
- **Origin**
  - Origin domain: \<your S3 bucket>
    - After selecting, a yellow popup should show. Select "Use website endpoint"
  - Enable Origin Shield: Yes
    - Origin Shield Region: US West (Oregon)
      - *This provides an additional caching layer for our files that reduces the load on our bucket and can provide faster request responses for users*
- **Web Application Firewall (WAF)**
  - For testing: Do not enable security protections
  - For production: Enable security protections 
    - **NOTE:** This incurs additional charges. Do not enable if you are only creating for testing purposes
    - *This adds additional security such as rules to block traffic from detected bots and requests commonly used to find system vulnerabilities*
- **Settings**
  - Price class: Use only North America and Europe
  - Default root object: index.html
- Leave the rest of the settings as default
3. Click "Create distribution" at the bottom of the page
4. Click to open the details of the newly created distribution. Copy the "ARN" *(e.g. arn:aws:cloudfront::897729115325:distribution/E22K8ZT7YIJADM)*
5. Go to the settings of the S3 bucket you created earlier and go to the Permissions tab.
6. To ensure access to the website only through CloudFront and not through the S3 bucket directly, edit the Bucket Policy and set it as follows, making sure to replace `your-cf-dist-arn` with the distribution domain name we retrieved in Step 4, and `your-bucket-name` with the name of your S3 bucket:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowCloudFrontServicePrincipalReadOnly",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudfront.amazonaws.com"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::your-bucket-name/*",
            "Condition": {
                "StringEquals": {
                    "AWS:SourceArn": "your-cf-dist-arn"
                }
            }
        }
    ]
}
```

7. Go to the URL of your S3 bucket website resources and ensure you do not have access to it and its files anymore. *(i.e. your-bucket-name.s3-website.ca-central-1.amazonaws.com)*
- It may take 10-15 minutes for the new bucket policy to take effect
8. Go to the URL of the cloudfront distribution (You will find it under the "Distribution domain name" field. It will look something like *https://d270q56do57o5x.cloudfront.net*) and ensure you can connect and interact with the website as expected.

### Your website is now ready for viewing!🎉 

