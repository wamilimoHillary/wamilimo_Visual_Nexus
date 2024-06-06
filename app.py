from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'wamilimo'  # secret key for session management

# Connecting to my MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="webgallary"
)
# print if the connection is successful
if db.is_connected():
    print("Successful connection to the web gallery database")


# my cursor object for query execution
cursor = db.cursor()

# index routing
@app.route('/')
def index():
    return render_template('index.html')

# home page routing
@app.route('/home.html')
def home():
    username = session.get('username')  # Get the username from the session
    return render_template('home.html', username=username)



# FOODS CATEGORY TEMPLATE ROUTING
@app.route('/foods_gallery.html')
def foods():
    # Fetch images with their corresponding table names
    cursor.execute("SELECT * FROM foods")
    images = cursor.fetchall()

    # checking if it's the admin logged in for delete button display
    is_admin = 'admin_name' in session and session['admin_logged_in']
    if is_admin:
        return render_template('images.html', images=images, is_admin=is_admin)
    else:
        # just return the images page without delete button
        return render_template('images.html', images=images)


# PLAYER CATEGORY TEMPLATE ROUTING
@app.route('/players_gallery.html')
def players():
    # Fetch images with their corresponding table names
    cursor.execute("SELECT * FROM players")
    images = cursor.fetchall()

    # checking if it's the admin logged in for delete button display
    is_admin = 'admin_name' in session and session['admin_logged_in']
    if is_admin:
        return render_template('images.html', images=images, is_admin=is_admin)
    else:
        # just return the images page without delete button
        return render_template('images.html', images=images)

# ABOUT TEMPLATE ROUTING
@app.route('/about.html')
def about():
    # Check if the user is logged in
    if 'logged_in' in session and session['logged_in']:
        # Pass a parameter to indicate that the about page is accessed after logging in
        return render_template('about.html', logged_in=True)
    else:
        # Render the about page without setting session variable
        return render_template('about.html')

# CONTACT TEMPLATE ROUTING
@app.route('/contact.html')
def contact():
    #return about page
    return render_template('about.html')


# PASSWORD TEMPLATE ROUTING
@app.route('/reset_password.html')
def reset_password():
    #return reset page
    return render_template('reset_password_request.html')

# users table TEMPLATE ROUTING inn admin dashbord
@app.route('/users.html')
def users():
    # querying user table
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()  # fetch all users

    '''#Print user data to terminal
    for user in users:
        print("User ID:", user[0])
        print("User Name:", user[1])
        print("Email:", user[2])
        print("User Password:", user[3])'''

    # Render to users html template
    return render_template('users.html', users=users)


# DELETE USER ROUTING
@app.route('/delete_user', methods=['POST'])
def delete_user():
    if 'admin_name' in session and session['admin_logged_in']:
        user_id = request.form['user_id']

        # Delete the user from the database
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        db.commit()

        # Redirect to the users page after deletion
        return redirect(url_for('users'))
    else:
        # Redirect to login page if admin is not logged in
        return redirect(url_for('index'))

# logout routing
@app.route('/logout.html')
def logout():
    # Clear the session data
    session.clear()
    # Perform any logout actions (e.g., clearing session, etc.)
    # Then redirect the user back to the home page
    return redirect(url_for('index'))

# USERS LOGIN ROUTING AND AUTHENTICATION
@app.route('/login', methods=['POST'])
def user_login():
    username = request.form['username'] # I am storing username input from form into my variable
    password = request.form['password'] # I'm storing password input  from form into my variable

    # Query the database to check if the username and password match
    cursor.execute("SELECT * FROM users WHERE user_name = %s AND user_password = %s", (username, password))
    user = cursor.fetchone()

    if user:
        # Set the username in the session
        session['username'] = username
        # Set session variable to indicate authentication
        session['logged_in'] = True  # Explicitly set to True after successful login
        # Authentication successful, redirect to home page
        return redirect(url_for('home'))
    else:
        # Authentication failed, set error message
        error_message = "Invalid username/password."
        # Pass error message to log in form
        return render_template('index.html', error_message=error_message)

# ADMIN LOGIN ROUTING AND AUTHENTICATION
@app.route('/admin', methods=['post'])
def admin_login():
    admin_username = request.form['username']
    password = request.form['password']

    # Query the database to check if the  admin username and password match
    cursor.execute("SELECT * FROM admin WHERE admin_username=%s AND password= %s",(admin_username, password))
    admin=cursor.fetchone()

    if admin:
        session['admin_name'] = admin_username
        session['admin_logged_in'] = True

        # Count number of users
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]

        # Pass is_admin flag to the template
        return render_template('admin_dashboard.html', admin_name=admin_username, user_count=user_count, is_admin=True)

    else:
        # Authentication failed, set admin error message
        admin_error_message= "wrong admin password/username"
        # Pass error message to admin form
        return render_template('index.html', admin_error_message=admin_error_message)


# back to admin page
@app.route('/admin.html')
def admin_page():
    if 'admin_name' in session and session['admin_logged_in']:
        # Your existing code...
        user_count = None
        if 'admin_name' in session and session['admin_logged_in']:
            # Count number of users
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]

        return render_template('admin_dashboard.html', admin_name=session['admin_name'], user_count=user_count, is_admin=True)  # Pass is_admin=True for admin users
    else:
        # Redirect to login page if admin is not logged in
        return redirect(url_for('index'))

# USERS SING UP AND ROUTING
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username'].strip().lower()  # Convert to lowercase and remove spaces
    email = request.form['email']
    password = request.form['password']

    # Check if user with the same email already exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()  #fetchone

    if existing_user:
        signup_error = "User with Email already exists."
        return render_template('index.html', signup_error=signup_error)

    # Insert new user into the database
    cursor.execute("INSERT INTO users (user_name, email, user_password) VALUES (%s, %s, %s)", (username, email, password))
    db.commit()  # Commit the transaction

    # Set a variable to indicate successful signup
    signup_success = True

    # Redirect to the index page
    return render_template('index.html', signup_success=signup_success)

# user update in home page
@app.route('/update', methods=['POST'])
def update():
    if 'username' in session:
        new_username = request.form['new_username']
        new_email = request.form['new_email']
        new_password = request.form['new_password']

        # Update user details in the database
        cursor.execute("UPDATE users SET user_name = %s, email = %s, user_password = %s WHERE user_name = %s",
                       (new_username, new_email, new_password, session['username']))
        db.commit()

        # Optionally, updating the username in the session
        session['username'] = new_username

        return redirect(url_for('home'))
    else:
        # Redirect to login page if user is not logged in
        return redirect(url_for('index'))

# route to handle search requests across multiple tables
@app.route('/search')
def search():
    query = request.args.get('query')
    all_images = []

    # Query the foods table for matching images
    cursor.execute("SELECT * FROM foods WHERE name LIKE %s OR description LIKE %s", ('%' + query + '%', '%' + query + '%'))
    all_images.extend(cursor.fetchall())

    # Query the players table for matching images
    cursor.execute("SELECT * FROM players WHERE name LIKE %s OR description LIKE %s", ('%' + query + '%', '%' + query + '%'))
    all_images.extend(cursor.fetchall())

    # Pass all matching image data to  HTML images template for rendering
    return render_template('images.html', images=all_images)

@app.route('/add_image', methods=['POST'])
def add_image():
    if 'admin_name' in session and session['admin_logged_in']:

        table_name = request.form['table_name']  # Get the table name from the form
        name = request.form['name']  # Get the image name from the form
        description = request.form['description']  # Get the image description from the form
        # Formulating file path based on the image name
        file_path = f"http://localhost/static/images/{name}"  # Assuming images are stored in this format

        # Insert image data into the chosen table
        cursor.execute(f"INSERT INTO {table_name} (name, description, file_path) VALUES (%s, %s, %s)",
                       (name, description, file_path))
        db.commit()

        #Set added_success to True
        added_success = True

        # Redirect to the admin page after successful insertion
        return redirect(url_for('admin_page', added_success=added_success))
    else:
        # Redirect to login page if admin is not logged in
        return redirect(url_for('index'))
# DELETE IMAGE ROUTING
@app.route('/delete_image', methods=['POST'])
def delete_image():
    if 'admin_name' in session and session['admin_logged_in']:
        image_id = request.form['image_id']
        table_name = request.form['table_name']  # Get the table name from the form data

        # Delete the image from the appropriate table based on the table name
        cursor.execute(f"DELETE FROM {table_name} WHERE image_id = %s", (image_id,))
        db.commit()

        # checking if it's the admin logged in for delete button display
        is_admin = 'admin_name' in session and session['admin_logged_in']
        if is_admin:
            cursor.execute("SELECT * FROM foods")
            images = cursor.fetchall()
            return render_template('images.html', images=images, is_admin=is_admin)

    else:
        # Redirect to login page if admin is not logged in
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
