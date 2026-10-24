
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Quiz App</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #141e30, #243b55);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .quiz-container {
            background: white;
            width: 100%;
            max-width: 520px;
            padding: 35px;
            border-radius: 20px;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .header h1 {
            color: #243b55;
            margin-bottom: 10px;
        }

        .header p {
            color: #777;
        }

        .question {
            background: #f3f6fb;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 12px;
            border-left: 5px solid #4776e6;
        }

        .question h3 {
            color: #243b55;
            margin-bottom: 15px;
        }

        input[type="text"] {
            width: 100%;
            padding: 13px;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 16px;
            outline: none;
        }

        input[type="text"]:focus {
            border-color: #4776e6;
        }

        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #4776e6, #8e54e9);
            color: white;
            border: none;
            border-radius: 9px;
            font-size: 17px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 5px;
        }

        button:hover {
            opacity: 0.9;
        }

        .result {
            margin-top: 20px;
            padding: 15px;
            border-radius: 10px;
            background: #eef4ff;
            color: #243b55;
            line-height: 1.8;
        }

        .footer {
            text-align: center;
            color: #888;
            margin-top: 22px;
            font-size: 13px;
        }
    </style>
</head>

<body>
    <div class="quiz-container">

        <div class="header">
            <h1>🧠 Python Quiz</h1>
            <p>Test your knowledge of Indian states!</p>
        </div>

        <form method="POST">

            <div class="question">
                <h3>1. What is the capital of India?</h3>
                <input
                    type="text"
                    name="q1"
                    placeholder="Enter your answer"
                    value="{{ q1 }}"
                    required
                >
            </div>

            <div class="question">
                <h3>2. What is the capital of Telangana?</h3>
                <input
                    type="text"
                    name="q2"
                    placeholder="Enter your answer"
                    value="{{ q2 }}"
                    required
                >
            </div>

            <button type="submit">Submit Answers →</button>

        </form>

        {% if submitted %}
        <div class="result">
            <h3>📋 Your Results</h3>
            <p>{{ result1 }}</p>
            <p>{{ result2 }}</p>
            <h3>Score: {{ score }}/2</h3>
        </div>
        {% endif %}

        <div class="footer">
            Built with Python, Flask, HTML & CSS
        </div>

    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def quiz():
    q1 = ""
    q2 = ""
    result1 = ""
    result2 = ""
    score = 0
    submitted = False

    if request.method == "POST":
        q1 = request.form.get("q1", "").strip().lower()
        q2 = request.form.get("q2", "").strip().lower()

        if q1 == "delhi":
            result1 = "✅ Question 1: Correct answer!"
            score += 1
        else:
            result1 = "❌ Question 1: Wrong answer. Correct answer: Delhi."

        if q2 in ["hyderabad", "hyderbad"]:
            result2 = "✅ Question 2: Correct answer!"
            score += 1
        else:
            result2 = "❌ Question 2: Wrong answer. Correct answer: Hyderabad."

        submitted = True

    return render_template_string(
        HTML,
        q1=q1,
        q2=q2,
        result1=result1,
        result2=result2,
        score=score,
        submitted=submitted
    )

if __name__ == "__main__":
    app.run(debug=True)
