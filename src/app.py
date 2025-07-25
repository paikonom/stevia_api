from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Helloooooo from Flask!"})

if __name__ == '__main__':
    app.run(debug=True)

#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