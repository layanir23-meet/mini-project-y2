from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase 

config = {
  "apiKey": "AIzaSyAab6zLfd6yY8EWle-qPsKF4ePq4WONs-k",
  "authDomain": "mini-project-y2.firebaseapp.com",
  "projectId": "mini-project-y2",
  "storageBucket": "mini-project-y2.appspot.com",
  "messagingSenderId": "396035272568",
  "appId": "1:396035272568:web:dd328f8571a45c8d5b228d",
  "measurementId": "G-T8W396QCHX" , "databaseURL" : "https://mini-project-y2-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods = ["GET" , "POST"])
def  signup ():
	error = ""
	if request.method == "POST":
		email= request.form['email']
		password = request.form ['password']
		phone_number = request.form ['phone_number']
        
		try :
			login_session['user'] = auth.create_user_with_email_and_password(email,password)
			user = {"email": email , "password" : password , "phone_number" : phone_number}
			db.child("users").child(login_session['user']['localId']).set(user)

			return redirect ('/signin')

		except:
			error = "Authentication failed"

	return render_template("signup.html")

@app.route ('/signin' , methods =['GET','POST'])
def signin():
	error = ""
	if request.method == "POST":
		email= request.form['email']
		password = request.form ['password']
            
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email,password)
			return redirect('/home')

		except:
			error = "Authentication failed"
	return render_template("signin.html")

	



@app.route ('/home' , methods = ['GET' , 'POST'])
def home_page():
	return render_template ("home.html" ) 








@app.route('/add_comment', methods=['GET', 'POST'])
def add_comment():
    if request.method == "POST":
        commentf =request.form['comment']
        try:
            comment = {"comment" : commentf}
            db.child("comments").push(commentf)
            return redirect(url_for("all_comment"))
        except:
            error = "Authentication failed"
            return render_template("add_comment.html")
        

    else:
        return render_template("add_comment.html")


        
    

 

    

@app.route ('/all_comment' , methods = ['GET', 'POST'])
def all_comment():
     comment = db.child("comments").get().val()
     return render_template ("comment.html", comment = comment )





if __name__ == '__main__':
    app.run(debug=True)