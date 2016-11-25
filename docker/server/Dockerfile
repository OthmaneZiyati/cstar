FROM tomcat:8.0
MAINTAINER "Craig Trim <craigtrim@gmail.com>"

#ADD settings.xml /home/antony/git/cstar/docker/server
#ADD tomcat-users.xml /home/antony/git/cstar/docker/server


#ADD sample.war /home/antony/git/cstar/docker/server

RUN ["rm", "-fr", "/usr/local/tomcat/webapps/ROOT"]
COPY ./sample.war /usr/local/tomcat/webapps/ROOT.war


CMD ["catalina.sh", "run"]
