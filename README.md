<p align="center">
  <img src="https://github.com/Jonqora/VibeCheckMyProf/blob/main/scratch/image_files/vcmp_logo.png" />
</p>

**VibeCheckMyProf** is a service that performs sentiment analysis on reviews for professors on the site **ratemyprofessors.com**, providing users with an appealing visual summary of recent reviews without having to scroll and read all of them. Users can compare the VibeCheck score with numerical ratings on the ratemyprofessors site and can also view a visualization of VibeCheck comment scores over time.


### Use Cases:
- A first year anxious student cannot decide which Math Professor to take a math course with, they learn about VibeCheckMyProf to get an overview of each professor’s reviews without having to read any comments.
- A CPSC professor wants to know what recent students think of them, so they use VibeCheckMyProf at the beginning of the semester and at the end to track how feedback has shifted over time.
- A student in their final year realizes they need an elective outside of their major, with limited time and familiarity with other department's professors, they use VibeCheckMyProf to compare overall scores of potential professors, making quick decisions without having to read individual comments.


## User Guide
[**WebGuide.md**](https://github.com/Jonqora/VibeCheckMyProf/blob/doc-update/SET-UP/WebGuide.md): This visual guide features images to walk you through using the application once it has been set up. For setup instructions from scratch, scroll down to [VibeCheckMyProf Setup](#vibecheckmyprof-setup).


## Team Members

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
This section provides step-by-step instructions to setting up VibeCheckMyProf. It outlines the prerequisites, the necessary AWS services, and the steps to get everything up and running smoothly. Follow the instructions carefully to ensure successful deployment of the application.


## Prerequisites
Before you begin, ensure of the following:
- You will require an AWS account
- Access to the following AWS Services: Lambda, S3, RDS, ECR, CloudFront, ...
- A minimum budget of $ $ ... to cover AWS costs  


## Steps
1. Set Up Database: Follow the instructions in [**DATABASE.md**](https://github.com/Jonqora/VibeCheckMyProf/blob/doc-update/SET-UP/DATABASE.md).
    * Documentation related to the database setup and management
2. Deploy Lambda Function: Refer to [**LAMBDA.md**](https://github.com/Jonqora/VibeCheckMyProf/blob/doc-update/SET-UP/LAMBDA.md)
    * Instructions for setting up and deploying the backend AWS Lambda function.
3. Host frontend web files: See [**WEB.md**](https://github.com/Jonqora/VibeCheckMyProf/blob/doc-update/SET-UP/WEB.md)
    * Instructions on how to set up and host the frontend web files.


After successfully following the set-up steps outlined, you will have a fully-functional copy of the application. We encourage you to explore VibeCheckMyProf, understand its features, and utilize its insights to enhance your own academic experience.


