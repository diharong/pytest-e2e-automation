from flask import Flask, render_template, request, redirect, url_for, session
from auth import validate_login

app = Flask(__name__)
app.secret_key = 'dev-secret-key' # 데모용(실무는 환경변수로 관리)

@app.get("/")
def home():
    return redirect(url_for("login_get"))

@app.get("/login")
def login_get():
    return render_template("login.html", error=None)

@app.post("/login")
def login_post():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    if validate_login(username, password):
        session["user"] = username
        return redirect(url_for("dashboard"))
    return render_template("login.html", error="로그인 실패: 입력값을 확인하세요.")

@app.get("/dashboard")
def dashboard():
    user = session.get("user")
    if not user:
        return redirect(url_for("login_get"))
    return render_template("dashboard.html", user=user)

@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_get"))

if __name__ == "__main__":
    app.run(debug=True)