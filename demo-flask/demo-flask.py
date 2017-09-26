from flask import Flask, render_template

app = Flask(__name__)


@app.route("/", methods=['GET'])
def homeish():
    return render_template('search.html', my_string="Wheeeee!", my_list=[0, 1, 2, 3, 4, 5], title="Home")


if __name__ == '__main__':
    app.run(debug=True, port=8000)
