[![Build Status](https://travis-ci.org/sdbenezra/streetartseattle-app-api.svg?branch=master)](https://travis-ci.org/sdbenezra/streetartseattle-app-api)
# streetartseattle-app-api
SAS app api source code

This is the backend api for a Django based database to keep track of artwork. This database is currently in use for the Street Art Seattle website https://www.streetartseattle.com.

This database uses Docker and Docker-Compose. You must have both Docker and Docker-Compose installed on your machine in order to use this code. This backend was deployed using AWS Elastic Beanstalk for the API and an AWS S3 to store images. Use a .env file to store your AWS access key and secret access key, as well as the name of your S3 bucket (and don't forget to enter the .env file in your .gitignore file). 

The following actions are supported by this API (append the following paths to your base url):

* **GET /api/work/works/** Shows all works in the database.

* **POST /api/work/works/** Posts a new work to the database.
  * Title field is required.
  * Other allowed fields are artist, category, about, media, measurements, date, location, imagecredit, and tags.
  
* **POST /api/work/works/<WORK_ID>/upload-images/** Adds a new image to a work denoted by the WORK_ID.
  * Requires a binary image file.
* **PATCH /api/work/works/<WORK_ID>/** Updates information in the database.
  * Allowed fields are fields are artist, category, about, media, measurements, date, location, imagecredit, and tags.
