from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    #return "this is hello world from flask app!!"
    return render_template("home.html")

@app.route("/user/<user_name>")
def show_user_name(user_name):
    return "<h1>Hello %s </h1>"% (user_name)

app.run(port=5000)