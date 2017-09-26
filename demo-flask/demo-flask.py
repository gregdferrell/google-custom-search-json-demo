from flask import Flask, render_template

app = Flask(__name__)


@app.route("/", methods=['GET'])
def home():
    return render_template('home.html', my_string="Wheeeee!", my_list=[0, 1, 2, 3, 4, 5], title="Home")


if __name__ == '__main__':
    app.run(debug=True, port=8000)
