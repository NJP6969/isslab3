import json
from flask import Flask, render_template_string, request, redirect, url_for, session, render_template
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

app.config['SECRET_KEY'] = 'qeervrvpnmakswplrj562mcrorl104k5n'  # Replace with a strong secret key
app.config['SESSION_COOKIE_PERMANENT'] = True  # Enable persistent cookies
import os

if not os.path.exists('users.txt'):
    with open('users.txt', 'w'):
        pass

@app.route('/main')
def main():
    return render_template('main.html')

    
@app.route('/')  #home page route
def home():
    if 'user_email' in session:
        return 'Welcome back, ' + session['user_email'] + '!'
    else:
        return redirect(url_for('login'))
@app.route('/register', methods=['GET', 'POST']) #home page redirects to register which accepts get and post requests, hashes password and also checks for duplicate email
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)
        user_data = {
            'name': name,
            'email': email,
            'password': hashed_password
        }
        with open('users.txt', 'r') as infile:
            users = infile.readlines()
            for user_json in users:
                existing_user_data = json.loads(user_json)
                if existing_user_data['email'] == email:
                    return 'Email already registered.'

        with open('users.txt', 'a') as outfile:
            json.dump(user_data, outfile)
            outfile.write('\n')
        return 'Registration successful.'

    register_form_html = """
    <!DOCTYPE html>
    <html>
    <body>
    <center><h2>Registration Form</h2></center>
    <center><p>Please fill in this form to create an account.</p></center>
    <center><p>Already have an account? <a href="/login">Login</a>.</p></center>
    <center>
    <form action="/register" method="post">
      *Name:<br>
      <input type="text" name="name" required><br>
      *Email:<br>
      <input type="text" name="email" required><br>
      *Password:<br>
      <input type="password" name="password" required><br>
      <input type="submit" value="Register">
    </form> 
    </center>

    </body>
    </html>
    """
    return render_template_string(register_form_html)

@app.route('/login', methods=['GET', 'POST']) #login page accepts get and post requests, compares hash of password
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        with open('users.txt', 'r') as infile:
            users = infile.readlines()
            for user_json in users:
                user_data = json.loads(user_json)
                if user_data['email'] == email:
                    if check_password_hash(user_data['password'], password):
                        session['user_email'] = email
                        return redirect(url_for('main'))
                    else:
                        return 'Password is incorrect.'
            return 'User not found.'

    login_form_html = """
    <!DOCTYPE html>
    <html>
    <body>
    <center><h2>Login Form</h2></center>
    <center><p>Please fill in this form to login.</p></center>
    <center><p>Don't have an account? <a href="/register">Register</a>.</p></center>
    <center>
    <form action="/login" method="post">
      *Email:<br>
      <input type="text" name="email" required><br>
      *Password:<br>
      <input type="password" name="password" required><br>
      <input type="submit" value="Login">
    </form> 
    </center>

    </body>
    </html>
    """
    return render_template_string(login_form_html)

@app.route('/user/<user_email>', methods=['GET']) #goes to login page and checks for user email
def get_user(user_email):
    with open('users.txt', 'r') as infile:
        users = infile.readlines()
        for user_json in users:
            user_data = json.loads(user_json)
            if user_data['email'] == user_email:
                return f"User details: {user_data}"
        return 'User not found.'
@app.route('/logout')
def logout():
    session.pop('user_email', None)  # Clear the session
    return redirect(url_for('login'))
if __name__ == "__main__":
    app.run(debug=False)

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
