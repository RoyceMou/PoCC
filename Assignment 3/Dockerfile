#Use following command to start docker, change /home/dmccormick to appropriate directory (Directory must be a root directory)
#sudo docker build .
#sudo docker run -it -v /home/ubuntu:/assign3 Dockerfile
FROM ubuntu:latest
RUN apt-get -y update && apt-get install -y python
VOLUME ["/assign3"]
#Change this to appropriate file
CMD python assign3/mapreduce.py assign3/energy-sorted100M.csv