from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from dotenv import load_dotenv
import os



load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')



@app.route('/')
def home():
    return render_template("home.html")




def get_max_id(table_name):
    conn = sqlite3.connect('user.db')  # Replace with your database file path
    cursor = conn.cursor()

    query = f"SELECT MAX(id) FROM {table_name};"
    cursor.execute(query)
    row_count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return row_count


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Password and Confirm Password don't match", 'danger')
            return redirect(url_for('register'))




        hashed_password = generate_password_hash(password, method='sha256')




         # Connect to the database
        conn = sqlite3.connect('User.db')
        cursor = conn.cursor()


        cursor.execute('SELECT EXISTS ( SELECT 1 FROM User WHERE username = ?)', (username,))

        exists = cursor.fetchone()[0]

        if(exists):
            flash('Username already exists. Choose another username.', 'failure')
            return redirect(url_for('register'))


        index = get_max_id("User") + 1
        data = (index, username, hashed_password)

        cursor.execute('INSERT INTO User VALUES (?, ?, ?)', data)

        # Save the changes and close the connection
        conn.commit()
        conn.close()



        # flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('User.db')
        cursor = conn.cursor()


        cursor.execute('SELECT * FROM User WHERE username = ?', (username, ))

        rows = cursor.fetchall()

        print("\n\n\nRows:", rows)

        conn.close()

        if len(rows) == 0:
            flash("User does not exist.", "danger")
            return redirect(url_for('login'))


        if check_password_hash(rows[0][2], password):
            # flash('Login successful.', 'success')
            return redirect(url_for('dashboard', name=username))
        else:
            print("Invalid")
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/dashboard/<name>', methods=['GET', 'POST'])
def dashboard(name):

    # if request.method == 'POST':


    return render_template('dashboard.html', user=name)






def get_person_index_by_username(username):
    # Connect to the database
    conn = sqlite3.connect('User.db')
    cursor = conn.cursor()

    # Define the SQL query to retrieve the index based on username
    query = f'SELECT id FROM User WHERE username = ?;'

    # Execute the query with the username as a parameter
    cursor.execute(query, (username,))

    # Fetch the result
    result = cursor.fetchone()

    # Close the connection
    conn.close()

    if result:
        return result[0]  # Return the index (ID) of the person
    else:
        return None  # Return None if username not found









@app.route('/dashboard/addContact/<name>', methods=['GET', 'POST'])
def addContact(name):



    if request.method == 'POST':
        cname = request.form['name']
        email = request.form['email']
        phone = request.form['phone']


        # Connect to the database
        conn = sqlite3.connect('User.db')
        cursor = conn.cursor()




        id = get_person_index_by_username(name)



        index = get_max_id("Contacts") + 1
        data = (index, cname, email, phone, id)

        print(data)

        cursor.execute('INSERT INTO Contacts VALUES (?, ?, ?, ?, ?)', data)

        # Save the changes and close the connection
        conn.commit()
        conn.close()



        return redirect(url_for('dashboard', name=name))



    return render_template('addContact.html', user=name)



@app.route('/dashboard/deleteContact/<name>', methods=['GET', 'POST'])
def deleteContact(name):

    if request.method == 'POST':
        cname = request.form['name']


        # Connect to the database
        conn = sqlite3.connect('User.db')
        cursor = conn.cursor()


        user_id = get_person_index_by_username(name)

        # Define the SQL query to delete contacts with a specific email
        delete_query = f'DELETE FROM Contacts WHERE name = ? AND user_id = ?;'


        cursor.execute(delete_query, (cname, user_id))


        # Save the changes and close the connection
        conn.commit()
        conn.close()



        return redirect(url_for('dashboard', name=name))


    return render_template('deleteContact.html', user=name)

@app.route('/viewContacts')
def viewContacts():
    return render_template('viewContacts.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))




if __name__ == '__main__':
    app.run()
