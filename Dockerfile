FROM safakcirag/fbprophet

COPY . .

RUN python app.py
