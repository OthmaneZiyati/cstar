FROM tomcat:8.0
MAINTAINER "Craig Trim <craigtrim@gmail.com>"

ADD settings.xml /home/antony/git/cstar/docker/server
ADD tomcat-users.xml /home/antony/git/cstar/docker/server

CMD ["catalina.sh", "run"]
