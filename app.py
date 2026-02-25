from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

# -------------------------
# Database configuration
# -------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///home_service.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -------------------------
# Models
# -------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    requests = db.relationship("Request", backref="user", lazy=True)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    requests = db.relationship("Request", backref="service", lazy=True)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="Pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# -------------------------
# Create database
# -------------------------
with app.app_context():
    db.create_all()

    # Add default services if not exist
    if Service.query.count() == 0:
        db.session.add_all([
            Service(title="نظافت منزل", price=150000),
            Service(title="لوله کشی", price=200000),
            Service(title="برق کاری", price=180000)
        ])
        db.session.commit()

# -------------------------
# Routes
# -------------------------

# Home page
@app.route("/")
def home():
    services = Service.query.all()
    return render_template("home.html", services=services)

# -------------------------
# User Register
# -------------------------
@app.route("/user_register", methods=["GET", "POST"])
def user_register():
    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(email=email).first():
            flash("ایمیل قبلا ثبت شده", "danger")
            return redirect("/user_register")

        new_user = User(full_name=full_name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash("ثبت نام موفقیت آمیز بود", "success")
        return redirect("/user_login")

    return render_template("user_register.html")

# -------------------------
# User Login
# -------------------------
@app.route("/user_login", methods=["GET", "POST"])
def user_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session["user_id"] = user.id
            session["user_name"] = user.full_name
            return redirect("/user_dashboard")
        else:
            flash("اطلاعات اشتباه است", "danger")

    return render_template("user_login.html")

# -------------------------
# User Dashboard
# -------------------------
@app.route("/user_dashboard")
def user_dashboard():
    if "user_id" not in session:
        return redirect("/user_login")

    user_requests = Request.query.filter_by(user_id=session["user_id"]).order_by(Request.created_at.desc()).all()
    services = Service.query.all()
    return render_template("user_dashboard.html", requests=user_requests, services=services)

# -------------------------
# Create new request (User)
# -------------------------
@app.route("/user/new_request", methods=["POST"])
def user_new_request():
    if "user_id" not in session:
        return redirect("/user_login")

    service_id = request.form["service_id"]
    description = request.form.get("description", "")

    new_request = Request(
        user_id=session["user_id"],
        service_id=service_id,
        description=description
    )
    db.session.add(new_request)
    db.session.commit()

    flash("درخواست ثبت شد", "success")
    return redirect("/user_dashboard")

# -------------------------
# User Logout
# -------------------------
@app.route("/user_logout")
def user_logout():
    session.clear()
    return redirect("/")

# -------------------------
# Admin Login
# -------------------------
@app.route("/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin":  # Default admin
            session["admin"] = True
            return redirect("/admin/dashboard")
        else:
            flash("اطلاعات اشتباه است", "danger")

    return render_template("login.html")

# -------------------------
# Admin Dashboard
# -------------------------
@app.route("/admin/dashboard")
def admin_dashboard():
    if "admin" not in session:
        return redirect("/login")

    all_requests = Request.query.order_by(Request.created_at.desc()).all()
    return render_template("admin_dashboard.html", requests=all_requests)

# -------------------------
# Admin update request status
# -------------------------
@app.route("/admin/update_status/<int:req_id>/<string:new_status>")
def update_request_status(req_id, new_status):
    if "admin" not in session:
        return redirect("/login")

    req = Request.query.get(req_id)
    if req:
        req.status = new_status
        db.session.commit()
        flash(f"وضعیت درخواست '{req.user.full_name}' به '{new_status}' تغییر یافت", "success")
    return redirect("/admin/dashboard")

# -------------------------
# Admin delete request
# -------------------------
@app.route("/admin/delete_request/<int:req_id>")
def delete_request(req_id):
    if "admin" not in session:
        return redirect("/login")

    req = Request.query.get(req_id)
    if req:
        db.session.delete(req)
        db.session.commit()
        flash(f"درخواست '{req.user.full_name}' حذف شد", "success")
    return redirect("/admin/dashboard")

# -------------------------
# Admin Logout
# -------------------------
@app.route("/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect("/")

# -------------------------
# Run the app
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)