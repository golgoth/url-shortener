# url-shortener

Base commit for url shortener early structure

To start the server:
Install docker and docker-compose last version (>=1.7.1)
run
`docker-compose -f ./docker-compose.yaml build`
then
`docker-compose -f ./docker-compose.yaml up`

##TESTING

unit test:
make sure to have python and tox installed (pip install tox), then run:
`tox`

integration tests:
run
`docker-compose -f ./docker-compose-test.yaml build`
then
`docker-compose -f ./docker-compose-test.yaml up`

check that the outcome is an exit 0

##RUN WITH LOCAL DATABASE
run
`docker-compose -f ./docker-compose-local.yaml build`
then
`docker-compose -f ./docker-compose-local.yaml up`

go to `http://localhost:5000` and proceed


##RUN WITH AWS DYNAMODB
run
`docker-compose -f ./docker-compose.yaml build`
then
`docker-compose -f ./docker-compose.yaml up`

go to `http://localhost:5000` and proceed
