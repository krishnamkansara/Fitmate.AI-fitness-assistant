from flask import Flask, render_template, request,Response, redirect, url_for
import os
import subprocess
import threading
app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/getfit', methods=['GET', 'POST'])
def get_fit():
    if request.method == 'POST':
        exercise_type = request.form.get('exercise')
        return redirect(url_for('exercise_started', exercise=exercise_type))
    return render_template('getfit.html')

from Start import generate_frames
@app.route('/exercise_started', methods=['POST'])
def exercise_started():
    exercise_type = request.form['exercise']
    return Response(generate_frames(exercise_type), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed')
def video_feed():
    # Video streaming route
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
# Dummy function to simulate exercise started
# Route for the Eat Better page
@app.route('/eatbetter')
def eat_better():
    return render_template('eatbetter.html')

# Additional routes can be set up similarly for other pages:
@app.route('/signIn')
def sign_in():
    return render_template('signIn.html')

@app.route('/signUp')
def sign_up():
    return render_template('signUp.html')

@app.route('/myprofile')
def my_profile():
    return render_template('myprofile.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

# Routes for individual recipes
@app.route('/recipe1')
def recipe1():
    return render_template('recipe1.html')

@app.route('/recipe2')
def recipe2():
    return render_template('recipe2.html')

@app.route('/recipe3')
def recipe3():  
    return render_template('recipe3.html')

@app.route('/contact',methods=['GET','POST'])
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
