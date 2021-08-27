import flask
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='./templates', static_url_path='')


@app.route('/')
def hello_world():
    f = open("alarm.txt", "r")
    alarm = f.read(1)
    print(alarm)

    if "1" in alarm:
        return app.send_static_file('index.html')
    elif "2" in alarm:
        return app.send_static_file('index2.html')
    else:
        return app.send_static_file('index3.html')


@app.route('/data')
def query_example():
    # if key doesn't exist, returns None
    temperature = request.args.get('temp')
    luminosity = request.args.get('lumi')
    humidity = request.args.get('hum')

    return 'temp is {0}, luminosity is {1}, and humidity is {2}'.format(temperature, luminosity, humidity)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
