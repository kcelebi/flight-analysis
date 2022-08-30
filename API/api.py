from flask import Flask, request
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
    app.run(debug=True, port=5000)