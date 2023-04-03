from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
app = Flask(__name__)
api = Api(app)

class flight_data(Resource):
    
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('depart-date', required = True)
        parser.add_argument('return-date', required = True)
        parser.add_argument('access-date', required = False)
        parser.add_argument('price-min', required = False)
        parser.add_argument('price-max', required = False)
        parser.add_argument('origin', required = True)
        parser.add_argument('dest', required = True)

        args = parser.parse_args()  # parse arguments to dictionary
        # access by ../flight_analysis_app/cached

        data = pd.read_csv()#load

        return {'data': data.to_dict()}, 200  # return data with 200 OK

api.add_resource(flight_data, '/flight-data')


if __name__ == '__main__':
    app.run()


'''from flask import Flask, request
from datetime import date

# create the Flask app
app = Flask(__name__)


'''
    Date in format: YYYY-mm-dd
'''
@app.route('/flight-data', methods = ['GET'])
def flight_data():
    depart_date = request.args.get('depart-date')
    return_date = request.args.get('return-date')
    access_date = date.today() if not request.args.get('access-date') else request.args.get('access-date')
    price_min = 0 if not request.args.get('price-min') else request.args.get('price-min')
    price_max = 1000000000 if not request.args.get('price-max') else request.args.get('price-max')
    origin = request.args.get('origin')
    dest = request.args.get('dest')

    query = [depart_date, return_date, access_date, price_min, price_max, origin, dest]
    return query

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)'''