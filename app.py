import tornado.ioloop
import tornado.web
import pandas as pd
import json
import datetime
from fbprophet import Prophet

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        else:
            return super(DateTimeEncoder, self).default(obj)

class MainHandler(tornado.web.RequestHandler):
    def post(self):
        params = self.request.body
        if params is not None:
            params_json = json.loads(self.request.body)
            print(params_json)
            if ("ds" not in params_json) or (not isinstance(params_json["ds"], list)):
                self.write("ds array not found!")
                return
            if ("y" not in params_json) or (not isinstance(params_json["y"], list)):
                self.write("y array not found!")
                return

            ds = params_json["ds"]
            y = params_json["y"]

            if len(ds) != len(y):
                self.write("ds vs. y array size mismatch!")
                return

            df = pd.DataFrame({'ds': ds, 'y': y})
            m = Prophet()
            m.fit(df)
            future_data = m.make_future_dataframe(periods=60)
            forecast = m.predict(future_data)
            f = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].reset_index().values.tolist()
            result = {
                "ds": [row[1] for row in f],
                "yhat": [row[2] for row in f],
                "yhat_lower": [row[3] for row in f],
                "yhat_upper": [row[4] for row in f]
            }
            print(result)
            result = json.dumps(result, cls=DateTimeEncoder)
            self.write(result)
        else:
            self.write("invalid input parameter")

    def get(self):
        sample = {
            "ds": ["2007-12-10","2007-12-11","2007-12-12","2007-12-13","2007-12-14"],
            "y": [9.59076113897809, 8.51959031601596, 8.18367658262066, 8.07246736935477, 7.8935720735049]
        }
        self.write(json.dumps({
            "service": "fbprophet-rest",
            "version": "0.3.post2",
            "help": "curl '-d %s' -H \"Content-Type: application/json\" -X POST http://localhost:80/" % json.dumps(sample)
        }))

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(80)
    print("fbprophet service is listening ...")
    tornado.ioloop.IOLoop.current().start()
