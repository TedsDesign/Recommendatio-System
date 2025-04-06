from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/api/data')
def get_data() :
    json_file = jsonify({"message" : "Hello React its Python"})
    print(json_file)
    return json_file;

if __name__ == '__main__':
    app.run(debug=True)