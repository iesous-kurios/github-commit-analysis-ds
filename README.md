# Github Commit Analysis API

## What is it

The Github Commit Analysis API allows users to access metrics of github user repositories. With databasing techniques and feature engineering you can fully realise the many facets of a repositories activity.  

## Main Features

Here are some details of the API

* Restful API
* Accepts post requests
* Outputs summary of given repository
* Utilizes Flask And AWS
* Built with Python

## Where to access the API 

The Endpoint to access the API is available here:
Base: [Gitstats](http://gitstatsdev-env.eba-cvhgzmsw.us-west-1.elasticbeanstalk.com/)

Endpoint for intial load of pull requests into database: http://gitstatsdev-env.eba-cvhgzmsw.us-west-1.elasticbeanstalk.com/updatePRs/<username>/<reponame>

To get a list of pull requests stored in the database for a repository: http://gitstatsdev-env.eba-cvhgzmsw.us-west-1.elasticbeanstalk.com/getPRs/<username>/<reponame>
 
For processed/summary output: http://gitstatsdev-env.eba-cvhgzmsw.us-west-1.elasticbeanstalk.com/summarize/<username>/<reponame>

## Interacting with the API

To interact with the API please send a post request to the endpoint url listed above with username and repository name. 
