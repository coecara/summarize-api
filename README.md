# python3-mecab-neologd-dockerfile

Dockerfile for Python3.6, Mecab, Neologd.


## Getting Started

1. build image  
`$ docker build -t container:1.0 .`  

2. run container  
`$ docker run -it -p 8888:8888 -v ~/Desktop/lexrank-summarize-sample:/home container:1.0`  

NOTE: You can change `container` to your container name.

## Stop and Delete
1. stop container
`$ docker stop`
2. delete container
`$ docker rm containerID`
3. delete image
`$ docker rmi imageID`

## Check Image and Container
1. check docker container
`$ docker ps -a`
2. check docker images
`$ docker images -a`

You can use `$python3` .

Reference  
https://qiita.com/oreyutarover/items/909d614ca3b48d2c9e16

Docker Reference  
https://qiita.com/shisama/items/48e2eaf1dc356568b0d7
