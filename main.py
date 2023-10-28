from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message


app = Flask(__name__)
app.config["SECRET_KEY"] = "mypass"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "rajaachandramohan@gmail.com"
app.config["MAIL_PASSWORD"] = "ivqu cflb cmyd agby"

db = SQLAlchemy(app)
mail = Mail(app)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))

@app.route('/', methods=["GET", "POST"])

def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        occupation = request.form["rad"]
        date_obj= datetime.strptime(date, '%Y-%m-%d')
        print(first_name, last_name, email, date, occupation)

        form= Form(first_name=first_name, last_name=last_name, email=email, date=date_obj, occupation=occupation )
        db.session.add(form)
        db.session.commit()
        flash("The form was successfully submitted", 'success')

        mg = f"Hi {first_name}, your application was successfully received. \n" \
                  f"{first_name} {last_name} \n {date}"
        message=Message(subject="Application Received",
                sender=app.config["MAIL_USERNAME"],
                recipients= [email], # list because it can take multiple email address. In this instance one.
                body=mg)
        mail.send(message)
    return render_template("index.html")

if __name__ == "__main__":
     with app.app_context():
         db.create_all()
app.run(debug=True, port=5001)