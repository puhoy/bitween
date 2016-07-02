FROM prosody/prosody

RUN prosodyctl register u1 localhost 12345 && prosodyctl register u2 localhost 12345

RUN chmod 755 /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 80 443 5222 5269 5347 5280 5281
USER prosody
ENV __FLUSH_LOG yes

CMD ["prosody"]