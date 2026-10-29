
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Your original Python login credentials
inbuilt_user_name = "admin"
inbuilt_user_password = "admin123"

# HTML + CSS + Flask in one file
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Page</title>

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
            background: linear-gradient(135deg, #101d42, #354f8c);
            padding: 20px;
        }

        .login-container {
            width: 100%;
            max-width: 900px;
            min-height: 520px;
            display: flex;
            overflow: hidden;
            border-radius: 20px;
            background: white;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }

        .left-panel {
            width: 50%;
            padding: 55px 40px;
            color: white;
            background: linear-gradient(145deg, #253e80, #101d42);
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .left-panel h1 {
            font-size: 35px;
            margin-bottom: 20px;
        }

        .left-panel p {
            font-size: 15px;
            line-height: 1.8;
            color: #dce5ff;
        }

        .circle {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            border: 2px solid rgba(255,255,255,0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 55px;
            margin-bottom: 30px;
            background: rgba(255,255,255,0.08);
        }

        .right-panel {
            width: 50%;
            padding: 55px 40px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .right-panel h2 {
            font-size: 30px;
            color: #18264a;
            margin-bottom: 10px;
        }

        .subtitle {
            color: #777;
            font-size: 14px;
            margin-bottom: 35px;
        }

        label {
            display: block;
            font-size: 14px;
            font-weight: bold;
            color: #333;
            margin-bottom: 9px;
        }

        input {
            width: 100%;
            padding: 14px;
            border: 1px solid #d5d9e3;
            border-radius: 9px;
            outline: none;
            font-size: 15px;
            margin-bottom: 23px;
            transition: 0.3s;
        }

        input:focus {
            border-color: #365cc9;
            box-shadow: 0 0 0 3px rgba(54,92,201,0.12);
        }

        button {
            width: 100%;
            padding: 15px;
            background: #3157c8;
            color: white;
            border: none;
            border-radius: 9px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }

        button:hover {
            background: #203e9d;
            transform: translateY(-2px);
        }

        .message {
            margin-bottom: 20px;
            padding: 12px;
            border-radius: 8px;
            font-size: 14px;
            text-align: center;
        }

        .success {
            color: #166534;
            background: #dcfce7;
        }

        .error {
            color: #b91c1c;
            background: #fee2e2;
        }

        .footer {
            text-align: center;
            color: #888;
            font-size: 12px;
            margin-top: 25px;
        }

        @media (max-width: 650px) {
            .login-container {
                flex-direction: column;
            }

            .left-panel,
            .right-panel {
                width: 100%;
                padding: 35px 25px;
            }

            .left-panel {
                text-align: center;
                align-items: center;
            }

            .left-panel h1 {
                font-size: 27px;
            }

            .circle {
                width: 85px;
                height: 85px;
                font-size: 40px;
                margin-bottom: 20px;
            }
        }
    </style>
</head>

<body>

    <div class="login-container">

        <div class="left-panel">
            <div class="circle">&#128274;</div>
            <h1>Welcome Back!</h1>
            <p>
                Sign in to access your account.
                Your journey starts here.
                Enter your credentials to continue.
            </p>
        </div>

        <div class="right-panel">
            <h2>Login</h2>
            <p class="subtitle">Enter your details below</p>

            {% if message %}
                <div class="message {{ status }}">
                    {{ message }}
                </div>
            {% endif %}

            <form method="POST" action="/">
                <label for="username">Username</label>
                <input
                    type="text"
                    id="username"
                    name="username"
                    placeholder="Enter your username"
                    autocomplete="username"
                    required
                >

                <label for="password">Password</label>
                <input
                    type="password"
                    id="password"
                    name="password"
                    placeholder="Enter your password"
                    autocomplete="current-password"
                    required
                >

                <button type="submit">Sign In</button>
            </form>

            <div class="footer">
                Secure Login Portal
            </div>
        </div>

    </div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    status = ""

    if request.method == "POST":
        user_name = request.form.get("username", "")
        user_password = request.form.get("password", "")

        if (
            user_name == inbuilt_user_name
            and user_password == inbuilt_user_password
        ):
            message = "Login successful! Welcome, admin."
            status = "success"
        else:
            message = "Invalid username or password."
            status = "error"

    return render_template_string(
        html,
        message=message,
        status=status
    )


if __name__ == "__main__":
    app.run(debug=True)
