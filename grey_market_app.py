from flask import Flask, request, redirect, url_for, render_template_string, send_from_directory
import sqlite3, os

app = Flask(__name__)

# ========== CONFIG ==========
DB_FILE = "app.db"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", None)

if not ADMIN_PASSWORD:
    print("â ï¸ Please set admin password first:\n   export ADMIN_PASSWORD='YourPasswordHere'")
    exit()

print(f"[INFO] App running at: http://127.0.0.1:5000")

# ========== DATABASE ==========
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            father_name TEXT,
            email TEXT,
            dob TEXT,
            marital_status TEXT,
            mobile TEXT,
            aadhaar TEXT,
            pan TEXT,
            password TEXT
        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            aadhaar_front TEXT,
            aadhaar_back TEXT,
            pan_card TEXT,
            bank_stmt TEXT,
            selfie TEXT
        )''')

init_db()

# ========== BASE HTML ==========
HTML_BASE = """
<!DOCTYPE html>
<html>
<head>
    <title>Grey Market</title>
    <style>
        body { font-family: Arial; background: #f5f7fa; margin:0; padding:0; }
        .container { width: 400px; margin: 60px auto; background: #fff; border-radius: 12px; box-shadow: 0 0 10px #ccc; padding: 20px; }
        input, select { width: 100%; padding: 10px; margin: 6px 0; border: 1px solid #ccc; border-radius: 6px; }
        button { width: 100%; background: #1976d2; color: white; padding: 10px; border: none; border-radius: 6px; cursor: pointer; }
        button:hover { background: #0f5fb3; }
        h2 { text-align: center; color: #333; }
        label { font-weight: bold; color:#555; }
        a { text-decoration:none; color:#1976d2; }
        .nav { text-align:center; margin-top:20px; }
    </style>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
"""

# ========== HOME ==========
@app.route('/')
def home():
    return render_template_string(HTML_BASE.replace(
        "{% block content %}{% endblock %}",
        """
        <div class="container" style="text-align:center;">
            <h2>Welcome to Grey Market ð</h2>
            <p>Your trusted trading platform.</p>
            <a href='/signup'><button>Create Account</button></a><br><br>
            <a href='/admin'><button>Admin Panel</button></a>
        </div>
        """
    ))

# ========== SIGNUP ==========
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = (
            request.form['first_name'].capitalize(),
            request.form['last_name'].capitalize(),
            request.form['father_name'].capitalize(),
            request.form['email'],
            request.form['dob'],
            request.form['marital_status'],
            request.form['mobile'],
            request.form['aadhaar'],
            request.form['pan'],
            request.form['password']
        )
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute('''INSERT INTO users
                (first_name, last_name, father_name, email, dob, marital_status, mobile, aadhaar, pan, password)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
        return redirect(url_for('kyc'))

    signup_html = """
    <div class="container">
        <h2>Sign Up</h2>
        <form method="post">
            <label>First Name</label><input name="first_name" placeholder="Enter First Name" required>
            <label>Last Name</label><input name="last_name" placeholder="Enter Last Name" required>
            <label>Father's Name</label><input name="father_name" placeholder="Enter Father's Name" required>
            <label>Email</label><input type="email" name="email" placeholder="Enter Email" required>
            <label>Date of Birth</label><input type="date" name="dob" required>
            <label>Marital Status</label>
            <select name="marital_status" required>
                <option value="">Select</option>
                <option>Married</option>
                <option>Unmarried</option>
                <option>Other</option>
            </select>
            <label>Mobile Number</label><input name="mobile" placeholder="Enter Mobile Number" required>
            <label>Aadhaar Number</label><input name="aadhaar" placeholder="Enter Aadhaar Number" required>
            <label>PAN Number</label><input name="pan" placeholder="Enter PAN Number" required>
            <label>Password</label><input type="password" name="password" placeholder="Enter Password" required>
            <label>Confirm Password</label><input type="password" name="repassword" placeholder="Re-enter Password" required>
            <button type="submit">Next â KYC</button>
        </form>
        <div class="nav"><a href="/">â Back Home</a></div>
    </div>
    """
    return render_template_string(HTML_BASE.replace("{% block content %}{% endblock %}", signup_html))

# ========== KYC UPLOAD ==========
@app.route('/kyc', methods=['GET', 'POST'])
def kyc():
    if request.method == 'POST':
        user_id = get_last_user_id()
        files = {}
        for field in ['aadhaar_front', 'aadhaar_back', 'pan_card', 'bank_stmt', 'selfie']:
            f = request.files[field]
            if f:
                filename = f"{field}_{user_id}.jpg"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                f.save(filepath)
                files[field] = filename

        with sqlite3.connect(DB_FILE) as conn:
            conn.execute('''INSERT INTO documents (user_id, aadhaar_front, aadhaar_back, pan_card, bank_stmt, selfie)
                            VALUES (?, ?, ?, ?, ?, ?)''',
                         (user_id, files.get('aadhaar_front'), files.get('aadhaar_back'),
                          files.get('pan_card'), files.get('bank_stmt'), files.get('selfie')))
        return "<h2 style='text-align:center;'>â KYC Submitted Successfully!</h2><p style='text-align:center;'><a href='/'>Go to Home</a></p>"

    kyc_html = """
    <div class="container">
        <h2>KYC Upload</h2>
        <form method="post" enctype="multipart/form-data">
            <label>Aadhaar Front</label><input type="file" name="aadhaar_front" required>
            <label>Aadhaar Back</label><input type="file" name="aadhaar_back" required>
            <label>PAN Card</label><input type="file" name="pan_card" required>
            <label>Bank Statement</label><input type="file" name="bank_stmt" required>
            <label>Selfie</label><input type="file" name="selfie" required>
            <button type="submit">Submit KYC</button>
        </form>
        <div class="nav"><a href="/">â Back Home</a></div>
    </div>
    """
    return render_template_string(HTML_BASE.replace("{% block content %}{% endblock %}", kyc_html))

# ========== ADMIN PANEL ==========
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            with sqlite3.connect(DB_FILE) as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM users")
                users = cur.fetchall()
                cur.execute("SELECT * FROM documents")
                docs = {d[1]: d for d in cur.fetchall()}
            html = "<div class='container'><h2>Admin Panel</h2><table border=1 width='100%' cellpadding=6>"
            html += "<tr><th>ID</th><th>Name</th><th>Email</th><th>Mobile</th><th>KYC Docs</th></tr>"
            for u in users:
                doc = docs.get(u[0])
                html += f"<tr><td>{u[0]}</td><td>{u[1]} {u[2]}</td><td>{u[4]}</td><td>{u[7]}</td>"
                if doc:
                    html += f"<td><a href='/uploads/{doc[2]}'>Aadhaar Front</a> | <a href='/uploads/{doc[3]}'>Aadhaar Back</a> | <a href='/uploads/{doc[4]}'>PAN</a> | <a href='/uploads/{doc[5]}'>Bank</a> | <a href='/uploads/{doc[6]}'>Selfie</a></td>"
                else:
                    html += "<td>â Not Uploaded</td>"
                html += "</tr>"
            html += "</table><div class='nav'><a href='/'>Logout</a></div></div>"
            return render_template_string(HTML_BASE.replace("{% block content %}{% endblock %}", html))
        else:
            return "<h3 style='text-align:center;color:red;'>Wrong Password</h3>"

    admin_html = """
    <div class="container">
        <h2>Admin Login</h2>
        <form method="post">
            <label>Admin Password</label><input type="password" name="password" required>
            <button type="submit">Login</button>
        </form>
        <div class="nav"><a href="/">â Back Home</a></div>
    </div>
    """
    return render_template_string(HTML_BASE.replace("{% block content %}{% endblock %}", admin_html))

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

def get_last_user_id():
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1")
        result = cur.fetchone()
    return result[0] if result else 0

# ========== RUN APP ==========
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
