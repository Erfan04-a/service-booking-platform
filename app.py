from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///home_service.db'
app.config['SECRET_KEY'] = 'secret123'
db = SQLAlchemy(app)

# -------------------------------------------------
# تنظیمات ایمیل
# -------------------------------------------------

EMAIL_SENDER = "YOUR_EMAIL@gmail.com"
EMAIL_PASS = "YOUR_APP_PASSWORD"

def send_email(to_email, subject, message):
    try:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = EMAIL_SENDER
        msg['To'] = to_email

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL_SENDER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()

        print("Email sent successfully")

    except Exception as e:
        print("Email Error:", e)


# -------------------------------------------------
# مدل‌ها
# -------------------------------------------------

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    price = db.Column(db.Integer)

class RequestService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(200))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    status = db.Column(db.String(20), default="در انتظار")
    service = db.relationship('Service')


# -------------------------------------------------
# صفحه اصلی
# -------------------------------------------------

@app.route('/')
def home():
    services = Service.query.all()
    return render_template('home.html', services=services)


# -------------------------------------------------
# ثبت درخواست
# -------------------------------------------------

@app.route('/request', methods=['GET', 'POST'])
def new_request():
    services = Service.query.all()

    if request.method == 'POST':
        req = RequestService(
            name=request.form['name'],
            phone=request.form['phone'],
            email=request.form['email'],
            service_id=request.form['service']
        )

        db.session.add(req)
        db.session.commit()

        flash("درخواست شما با موفقیت ثبت شد ✔", "success")
        return redirect('/')

    return render_template('request_service.html', services=services)


# -------------------------------------------------
# ورود مدیر
# -------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == "admin" and request.form['password'] == "1234":
            session['admin'] = True
            return redirect('/admin')
        else:
            flash("نام کاربری یا رمز عبور اشتباه است!", "danger")

    return render_template('login.html')


# -------------------------------------------------
# داشبورد مدیریت
# -------------------------------------------------

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin'):
        return redirect('/login')

    search = request.args.get('search')

    if search:
        requests_list = RequestService.query.filter(
            RequestService.name.contains(search)
        ).all()
    else:
        requests_list = RequestService.query.all()

    return render_template('admin_dashboard.html', requests=requests_list, search=search)


# -------------------------------------------------
# آپدیت وضعیت + ارسال ایمیل
# -------------------------------------------------

@app.route('/update_status/<int:req_id>/<string:new_status>')
def update_status(req_id, new_status):
    if not session.get('admin'):
        return redirect('/login')

    req = RequestService.query.get(req_id)

    if req:
        req.status = new_status
        db.session.commit()

        try:
            send_email(
                to_email=req.email,
                subject="وضعیت درخواست شما",
                message=f"کاربر گرامی، وضعیت درخواست شما به '{new_status}' تغییر یافت."
            )
        except Exception as e:
            print("Email Sending Error:", e)

        flash("وضعیت تغییر کرد و ایمیل اطلاع‌رسانی ارسال شد ✔", "success")

    return redirect('/admin')


# -------------------------------------------------
# حذف درخواست
# -------------------------------------------------

@app.route('/delete_request/<int:req_id>')
def delete_request(req_id):
    if not session.get('admin'):
        return redirect('/login')

    req = RequestService.query.get(req_id)

    if req:
        db.session.delete(req)
        db.session.commit()

    flash("درخواست حذف شد ✔", "success")
    return redirect('/admin')


# -------------------------------------------------
# اجرای برنامه
# -------------------------------------------------


# -------------------------
# نمایش لیست خدمات
# -------------------------
@app.route('/services')
def services_page():
    if not session.get('admin'):
        return redirect('/login')

    services = Service.query.all()
    return render_template('services.html', services=services)


# -------------------------
# افزودن خدمت جدید
# -------------------------
@app.route('/add_service', methods=['GET', 'POST'])
def add_service():
    if not session.get('admin'):
        return redirect('/login')

    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']

        new_service = Service(title=title, price=price)
        db.session.add(new_service)
        db.session.commit()

        flash("خدمت جدید با موفقیت اضافه شد ✔", "success")
        return redirect('/services')

    return render_template('add_service.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash("با موفقیت خارج شدید ✔", "success")
    return redirect('/login')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        if Service.query.count() == 0:
            db.session.add_all([
                Service(title="نظافت منزل", price=150000),
                Service(title="لوله کشی", price=200000),
                Service(title="برق کاری", price=180000)
            ])
            db.session.commit()

    app.run(debug=True)
    