FROM movecrew/one4ubot:alpine-latest

RUN mkdir /claire && chmod 777 /claire
ENV PATH="/claire/bin:$PATH"
WORKDIR /claire

RUN git clone https://github.com/kevinhhg/claire -b sql-extended /claire

#
# Copies session and config(if it exists)
#
COPY ./sample_config.env ./userbot.session* ./config.env* /claire/

#
# Make open port TCP
#
EXPOSE 80 443

#
# Finalization
#
CMD ["python3","-m","userbot"]
