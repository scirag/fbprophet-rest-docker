FROM safakcirag/fbprophet

RUN mkdir /service

COPY . /service

EXPOSE 80

CMD python /service/app.py
