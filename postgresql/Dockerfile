#
FROM ubuntu:16.04
#
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y vim
RUN apt-get install -y postgresql
#
COPY . /vocal-seagull-aws
#
#WORKDIR /vocal-seagull-aws
#
# psql -d vocal_seagull -U seagull < raw_observation.psql
#ENTRYPOINT ["bin/runner.sh"]
#
USER postgres
#
RUN /etc/init.d/postgresql start1
RUN psql --command "CREATE USER vocal WITH SUPERUSER PASSWORD 'bogus';"
RUN createdb -O vocal vocal_seagull
#
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.5/main/pg_hba.conf
#
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.5/main/postgresql.conf
#
EXPOSE 5432
#
# Add VOLUMEs to allow backup of config, logs and databases
#VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]
#
# Set the default command to run when starting the container
#CMD ["/usr/lib/postgresql/9.5/bin/postgres", "-D", "/var/lib/postgresql/9.5/main", "-c", "config_file=/etc/postgresql/9.5/main/postgresql.conf"]
#