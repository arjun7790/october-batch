from flask import Flask, request, render_template_string, session

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

correct_password = "admin123"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Login</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }

        body {
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #141e30, #243b55);
        }

        .login-box {
            width: 360px;
            max-width: 90%;
            padding: 35px;
            background: white;
            border-radius: 18px;
            text-align: center;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        }

        .icon {
            font-size: 48px;
            margin-bottom: 12px;
        }

        h1 {
            color: #243b55;
            margin-bottom: 10px;
        }

        .subtitle {
            color: #777;
            margin-bottom: 25px;
            font-size: 14px;
        }

        label {
            display: block;
            text-align: left;
            margin-bottom: 8px;
            font-weight: bold;
            color: #333;
        }

        input[type="password"] {
            width: 100%;
            padding: 13px;
            border: 1px solid #ccc;
            border-radius: 8px;
            margin-bottom: 18px;
            outline: none;
            font-size: 15px;
        }

        input[type="password"]:focus {
            border-color: #4776e6;
        }

        button {
            width: 100%;
            padding: 13px;
            border: none;
            border-radius: 8px;
            background: #4776e6;
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            background: #315ac4;
        }

        .message {
            margin-top: 20px;
            padding: 12px;
            border-radius: 8px;
            font-size: 14px;
        }

        .success {
            background: #d4edda;
            color: #155724;
        }

        .error {
            background: #f8d7da;
            color: #721c24;
        }

        .locked {
            background: #343a40;
            color: white;
        }

        .attempts {
            margin-top: 16px;
            color: #777;
            font-size: 13px;
        }

        .reset {
            display: inline-block;
            margin-top: 15px;
            color: #4776e6;
            text-decoration: none;
            font-size: 14px;
        }
    </style>
</head>

<body>
    <div class="login-box">
        <div class="icon">🔐</div>

        <h1>Welcome Back!</h1>
        <p class="subtitle">Enter your password to continue</p>

        {% if not session.get('success') and not session.get('locked') %}
        <form method="POST">
            <label for="password">Password</label>

            <input
                type="password"
                id="password"
                name="password"
                placeholder="Enter your password"
                required
                autofocus
            >

            <button type="submit">Login →</button>
        </form>
        {% endif %}

        {% if message %}
            <div class="message {{ status }}">
                {{ message }}
            </div>
        {% endif %}

        {% if not session.get('success') and not session.get('locked') %}
            <p class="attempts">
                Attempts remaining: {{ 3 - session.get('attempts', 0) }}
            </p>
        {% endif %}

        {% if session.get('success') or session.get('locked') %}
            <a class="reset" href="/reset">Start Again</a>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    status = ""

    if "attempts" not in session:
        session["attempts"] = 0

    if session.get("locked"):
        message = "Account Locked 🔒"
        status = "locked"

    elif session.get("success"):
        message = "Login Successful ✅"
        status = "success"

    elif request.method == "POST":
        password = request.form.get("password", "")

        # Your original password-checking logic
        for attempt in range(session["attempts"] + 1, 4):
            if password == correct_password:
                session["success"] = True
                message = "Login Successful ✅"
                status = "success"
                break
            else:
                session["attempts"] = attempt
                message = "Wrong Password ❌"
                status = "error"

                if attempt == 3:
                    session["locked"] = True
                    message = "Account Locked 🔒"
                    status = "locked"

            # One submitted password counts as one attempt
            break

    return render_template_string(
        HTML, message=message, status=status
    )


@app.route("/reset")
def reset():
    session.clear()
    return """
    <meta http-equiv="refresh" content="0;url=/">
    """


if __name__ == "__main__":
    app.run(debug=True)
