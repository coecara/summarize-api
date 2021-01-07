# lexrank-summarize-sample

This is the sample code for lexRank summarization.

## Prepare

1. build image  
`$ docker build -t container:1.0 .`  

2. run container  
`$ docker run -it -p 8888:8888 -v ~/Desktop/lexrank-summarize-sample:/home container:1.0`  

## Getting Started

`$ cd home/`  
`$ python3 lexrank.py`

It will shows the summuary of my blog.
https://naoki-is.me/archives/92
