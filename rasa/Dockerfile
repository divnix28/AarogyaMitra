FROM rasa/rasa:3.6.10-full

USER root

WORKDIR /app

COPY config.yml domain.yml endpoints.yml ./
COPY data/ ./data/
COPY actions/ ./actions/

RUN rasa train nlu --config config.yml --domain domain.yml --data data/

EXPOSE 5005 5055

USER 1001

ENTRYPOINT ["rasa"]
CMD ["run", "--enable-api", "--cors", "*", "--port", "5005"]