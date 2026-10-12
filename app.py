
from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "guess-game-secret-key"

@app.route("/", methods=["GET", "POST"])
def home():
    if "number" not in session:
        session["number"] = random.randint(1, 10)
        session["attempts"] = 3
        session["message"] = "I'm thinking of a number between 1 and 10!"
    if request.method == "POST" and request.form.get("action") == "restart":
       session.clear()
       return render_template(
          "index.html",
          message="New game started!",
          attempts=3,
          finished=False
    )
    if request.method == "POST" and session["attempts"] > 0:
        guess = request.form.get("guess", "").strip()

        if not guess.isdigit() or not 1 <= int(guess) <= 10:
            session["message"] = "Please enter a number from 1 to 10."
        else:
            guess = int(guess)
            session["attempts"] -= 1

            if guess == session["number"]:
                session["message"] = "🎉 Correct! You won!"
                session["attempts"] = 0
                session["finished"] = True
            elif session["attempts"] == 0:
                session["message"] = (
                    f"Game over! The number was {session['number']}."
                )
                session["finished"] = True
            elif guess < session["number"]:
                session["message"] = "📉 Too low! Try again."
            else:
                session["message"] = "📈 Too high! Try again."

    if request.method == "POST" and request.form.get("action") == "restart":
        session.clear()
        return render_template("index.html",
                               message="New game started!",
                               attempts=3, finished=False)

    return render_template(
        "index.html",
        message=session["message"],
        attempts=session["attempts"],
        finished=session.get("finished", False)
    )

if __name__ == "__main__":
    app.run(debug=True)
