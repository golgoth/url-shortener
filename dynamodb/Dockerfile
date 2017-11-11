FROM openjdk:8-jre
MAINTAINER Adrien Duffy <adrien.duffy@gmail.com>


RUN mkdir -p /app/dynamodb

WORKDIR /app/

COPY . dynamodb

CMD java -Djava.library.path=./dynamodb/DynamoDBLocal_lib -jar ./dynamodb/DynamoDBLocal.jar -sharedDb
