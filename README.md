# Short10

# Overview:

## Access to the service:

Go to http://www.arrivendel.com/ and enjoy!

## Description:
Short10 is an url shortener (yes, probably the 10000th one).
Users ask the service to shorten a URL, and they receive a short version of it.

## What does it look like?
Inputing `https://www.youtube.com/watch?v=B_2asRONZBM` will return `example.com/2XYJ8Fl`.
`2XYJ8Fl` is the shortened URL computed by the service.
Inputing several time the same URL will return the same short URL. The short url will always be redirecting to the same page, as long as the service lives.

Not that it is up to the user to provide a correct url. While some characters are prevented in the input, a lot of strings can be shorten, the redirection will just behave as if the user input the bad url from the start in his browser.


## How is the short URL computed?
Two main options were possible:
- computing a hash of the URL
- using the storage system to keep track of a counter that would increment for each new entry, and then converting this counter into a string would give back a short URL.

I choose the first option, as I didn't want to depend on a database counter.
The integer of the md5 hexdigest of the url is converted into a base 62 string (string composed of a mix of those values: `0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`).

The first 7 characters are selected and used as the short url. This comes with a drawback: hash are subject to collisions, and I have the birthday paradox telling us that keys will collide, quite fast.

To handle collision, I try to add characters to the short key from the original url hashed string, but to keep it short, I divide the integer of the hexdigest by 2 up to 100 times before giving up. Those cases should be rare, so if it would indeed affect performances, it would not do it often.

## Architecture
To ensure scalability and high availability, I decided to build the app in a stateless way at the server, talking to the database to store and read records. The shorten_url is a service that is shipped on a container, deployed on a AWS ECS auto scaling group, interfaced to the world with an application load balancer, and using DynamoDB as its key-value database.

The choice of DynamoDB is coming from the database strength when it comes to scale and being highly available. The NoSql key-value pattern is perfectly fitting the app, with the short url being the key, allowing fast redirections when a user use a short link.
To help with scalability and lower the costs of DynamoDB, and make the calls faster, a redis cache is introduced as a first storage layer for the service.

Note:
- If Java was choosen for developing the application, DAX, the dynamodb cache system could have been used easily to provide this cache layer. But DAX is not supported by boto3 yet (to my knowledge).

The goal in our architecture is to have this redis cache sharded on a cluster through AWS elasticache. For the local testing and prod until elastic cache is fully operational with our service, a redis cache is deployed in the same service than the url shortener to handle cache locally (The interest is limited in case it scales to many hosts, as the cache is not global to many containers, though it is still a good start).

The AWS architecture is built using terraform (cf https://github.com/golgoth/aws-terraform)

I also created some kubernetes config, in this repo, since I planned to first use kubernetes to orchestrate the containers, struggling with associating my domain name with the kubernetes cluster, I decided to go for ECS instead.

## Development:
To ensure good CI/CD levels, I created a jenkins server hosted on EC2, linked to github, running unit tests (tox/flake8) automatically every time the master branch of this project is changing.

Docker cloud is also plugged in with github to build the image of the service and have it available on the repository `golgothlt/url_shortener`. This is this image that is used when deploying on ECS from terraform.

IT tests are run using docker locally, with the `docker-compose-local` file.

## Improvements possible:
- Depending on the cost impact of having a secondary index on dynamodb, there is a room for performance improvement when linking the long url to a potential pre existing short url. Currently, we compute it and check if it is in the DB, linked to the correct long URL. This leads to several calls to the DB in case of hash collisions, as we need to go through several short url before finding the correct long one.
- There is space for url sanitizing (removing `https`... blocks)
- Currently dynamodb is not set up to scale automatically but could easily be (for simplicity and costs limitation)
- More cloud watch alarms could be set up for auto scaling policies

# Building the service:
Install docker and docker-compose last version (>=1.7.1)

## Running IT tests

unit test:
make sure to have python 3.6 and tox installed (pip install tox), then run:
`tox`

integration tests:
run
`docker-compose -f ./docker-compose-test.yaml build`
then
`docker-compose -f ./docker-compose-test.yaml up`

check that the outcome is an exit 0

## RUN WITH LOCAL DATABASE
run
`docker-compose -f ./docker-compose-local.yaml build`
then
`docker-compose -f ./docker-compose-local.yaml up`

go to `http://localhost:5000` and proceed


## RUN WITH AWS DYNAMODB (need aws credentials)
run
`docker-compose -f ./docker-compose.yaml build`
then
`docker-compose -f ./docker-compose.yaml up`

go to `http://localhost:5000` and proceed
