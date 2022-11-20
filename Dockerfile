FROM mongo

ADD mongo-init.js /docker-entrypoint-initdb.d/
EXPOSE 27017
