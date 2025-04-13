FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD=1234
ENV MYSQL_DATABASE=mydb

VOLUME ["/var/lib/mysql"]

# Copy entrypoint script to multiple locations for redundancy
COPY entrypoint.sh /entrypoint.sh
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /entrypoint.sh && chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 3306

ENTRYPOINT ["/entrypoint.sh"]

CMD ["mysqld"]
