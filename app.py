
import os
from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection
app = Flask(__name__)
app.secret_key = "supersecretkey"  # change in production

# Landing Page (Homepage)
@app.route("/")
def landing():
    if "user_id" in session:
        return redirect(url_for("dashboard"))  # logged-in users go to notes
    return render_template("landing.html")

# Home Page
@app.route("/notes")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Clear flag after showing success once
    session.pop("just_logged_in", None)

    query = request.args.get("q")  # get search keyword

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if query:
        cursor.execute("""
            SELECT * FROM notes 
            WHERE user_id=%s AND (title LIKE %s OR content LIKE %s) 
            ORDER BY id DESC
        """, (session['user_id'], f"%{query}%", f"%{query}%"))
    else:
        cursor.execute("SELECT * FROM notes WHERE user_id=%s ORDER BY id DESC", (session['user_id'],))

    notes = cursor.fetchall()
    conn.close()
    return render_template("index.html", notes=notes, query=query)


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, password)
            )
            conn.commit()
            flash("✅ Registration successful! Please login.", "success")
            return redirect(url_for("login"))
        except:
            flash("⚠ Username or Email already exists!", "danger")
        finally:
            conn.close()

    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Fetch form values safely
        email = request.form.get('email')
        password = request.form.get('password')

        # DB connection
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()

        # Check if user exists and password matches
        if user and check_password_hash(user['password'], password):
            # Store session data
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']

            # Flash only once per login
            if not session.get("just_logged_in"):
                flash("✅ Login successful!", "success")
                session["just_logged_in"] = True

            return redirect(url_for('dashboard'))
        else:
            flash("⚠ Invalid email or password!", "danger")

    # If GET request → show login form
    return render_template('login.html')



# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("login"))

# Add Note
@app.route('/add', methods=['POST'])
def add_note():
    if "user_id" not in session:
        return redirect(url_for("login"))

    title = request.form['title']
    content = request.form['content']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (user_id, title, content) VALUES (%s, %s, %s)",
                   (session['user_id'], title, content))
    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))

# Delete Note
@app.route('/delete/<int:note_id>')
def delete_note(note_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id=%s AND user_id=%s", (note_id, session['user_id']))
    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))

# Edit Note - Show Form
@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute("UPDATE notes SET title=%s, content=%s WHERE id=%s AND user_id=%s",
                       (title, content, note_id, session['user_id']))
        conn.commit()
        conn.close()
        return redirect(url_for("dashboard"))

    # If GET request → fetch note data
    cursor.execute("SELECT * FROM notes WHERE id=%s AND user_id=%s", (note_id, session['user_id']))
    note = cursor.fetchone()
    conn.close()

    if note:
        return render_template("edit.html", note=note)
    else:
        flash("⚠ Note not found or unauthorized!", "danger")
        return redirect(url_for("dashboard"))
    
# View Note
@app.route("/view/<int:note_id>")
def view_note(note_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notes WHERE id=%s AND user_id=%s", (note_id, session['user_id']))
    note = cursor.fetchone()
    conn.close()

    if not note:
        flash("⚠ Note not found!", "danger")
        return redirect(url_for("dashboard"))

    return render_template("view.html", note=note)

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
