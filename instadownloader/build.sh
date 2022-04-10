#!/bin/bash

docker image rm localhost:1035/tingkai/instadownloader:latest
pipenv lock -r > requirements.txt
docker build . --tag=localhost:1035/tingkai/instadownloader &&
docker push localhost:1035/tingkai/instadownloader &&
docker image rm localhost:1035/tingkai/instadownloader:latest &&
docker pull localhost:1035/tingkai/instadownloader
