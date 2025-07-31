from flask import Flask, request

app = Flask(__name__)

@app.route('/api/callback/', methods=['POST'])
def callback():
    data = request.get_json()
    print("Callback Data:", data)
    return {"ResultCode": 0, "ResultDesc": "Success"}, 200

if __name__ == '__main__':
    app.run(port=8000)