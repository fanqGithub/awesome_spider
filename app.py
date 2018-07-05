from flask import Flask,jsonify,render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('studyrender.html')

@app.route('/api/test1',methods=['Get'])
def test1():
    response={
        'name':'xiaomi',
        'sex':'man'
    }
    return jsonify(response),200


def getUserInfo():
    pass


if __name__ == '__main__':
    app.run()
