# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for
import trigger_exp
import kill_all


app = Flask(__name__)

@app.route("/")
def welcome():
    kill_all.main()
    return render_template('welcome.html')     

@app.route("/launch")
def trigger():
    trigger_exp.main()
    return redirect("http://expedition.int.colorado.edu:8000/account/insecurelogin?username=admin&password=itplab", code=302)    


@app.route("/killall")
def kill():
    kill_all.main()
    print "Stopped"
    return render_template('welcome.html') 

@app.route("/about")
def about():

    """

    This method opens about me page

    """

    return render_template('about.html')





@app.route("/contact")

def contact():

    """

    This method opens contacts page

    """

    return render_template('contact.html')


if __name__ == '__main__':

    app.run(host="0.0.0.0",debug=True)


     
