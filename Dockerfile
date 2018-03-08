# Docker image for drone launching of digitalocean droplets 

FROM python
COPY ./example.py /bin/example
ENTRYPOINT ["/bin/example"]
