from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import random
load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = "mysecretkey"

# Flask-Mail Configuration (Elastic Email via SMTP)
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

mail = Mail(app)

db = SQLAlchemy(app)

from datetime import datetime

class Users(db.Model):
     serial_number = db.Column(db.Integer,primary_key=True)
     First_Name = db.Column(db.String(15), nullable=False)
     Last_Name = db.Column(db.String(10))
     Email = db.Column(db.String(50),nullable=False,unique=True)
     Password = db.Column(db.String(),nullable=False)
     is_admin = db.Column(db.Boolean, default=False)
     vlogs = db.relationship('Vlogs', backref='author', lazy=True, cascade='all, delete-orphan')

class Vlogs(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(100), nullable=False)
     description = db.Column(db.Text, nullable=False)
     content = db.Column(db.Text, nullable=False)
     cover_image_url = db.Column(db.String(500), nullable=True, default='')
     created_at = db.Column(db.DateTime, default=datetime.utcnow)
     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
     author_id = db.Column(db.Integer, db.ForeignKey('users.serial_number'), nullable=False)

class ContactMessage(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(100), nullable=False)
     email = db.Column(db.String(100), nullable=False)
     subject = db.Column(db.String(200), nullable=False)
     message = db.Column(db.Text, nullable=False)
     email_sent = db.Column(db.Boolean, default=False)
     created_at = db.Column(db.DateTime, default=datetime.utcnow)
     
@app.context_processor
def inject_user():
    if "user" in session:
        current_user = Users.query.filter_by(Email=session["user"]).first()
        return dict(user=current_user)
    return dict(user=None)

with app.app_context():
    db.create_all()
    # Make the owner an admin
    owner = Users.query.filter_by(Email='admin@gmail.com').first()
    if owner:
        owner.is_admin = True
        db.session.commit()

@app.route('/')
def home():
    return render_template('index.html')




@app.route('/login', methods=["GET","POST"])
def login():
    if request.method=="POST":
         Email = request.form.get("Email")
         Password = request.form.get("Password")
         user = Users.query.filter_by(Email=Email).first()
         if user:
              if check_password_hash(user.Password,Password):
                   session["user"] = Email
                   return redirect(url_for("dashboard"))
              else:
                    return render_template("login.html",error = "The password you entered is incorrect")

         else:
              return render_template("login.html",error = "Account does not exist")
    return render_template("login.html")

@app.route('/forget_password',methods=["GET","POST"])
def forget_password():
    if request.method=="POST":
        email = request.form.get("Email")
        # session.pop('email')
        session['email'] = email
        try:
            session.pop('otp')
        except:

            otp = random.randint(000000,999999)
            # msg = Message(
            # 'Password Reset OTP',
            # recipients=[email],
            # body=f'your one time password is {otp}'
            # )
            msg = Message(
        subject='Password Reset OTP',
        recipients=[email],
        html=f"""

        <div style="
            background:#fff8e1;
            padding:50px 20px;
            font-family:Arial,sans-serif;
        ">

            <div style="
                max-width:560px;
                margin:auto;
                background:white;
                border-radius:24px;
                overflow:hidden;
                box-shadow:0 15px 40px rgba(255,193,7,0.25);
                border:2px solid #ffe082;
            ">

                <!-- Header -->
                <div style="
                    background:linear-gradient(135deg,#facc15,#f59e0b);
                    padding:40px;
                    text-align:center;
                ">

                    <h1 style="
                        margin:0;
                        color:#1f2937;
                        font-size:32px;
                        font-weight:bold;
                    ">
                        🔐 Password Reset
                    </h1>

                    <p style="
                        margin-top:12px;
                        color:#3f3f46;
                        font-size:15px;
                    ">
                        Secure One-Time Password Verification
                    </p>

                </div>

                <!-- Body -->
                <div style="
                    padding:45px 35px;
                    text-align:center;
                ">

                    <h2 style="
                        color:#111827;
                        margin-bottom:10px;
                        font-size:26px;
                    ">
                        Your Verification Code
                    </h2>

                    <p style="
                        color:#52525b;
                        font-size:15px;
                        line-height:1.8;
                        margin-bottom:30px;
                    ">
                        Use the OTP below to continue resetting your password.
                        This code is valid for a short time only.
                    </p>

                    <!-- OTP Box -->
                    <div style="
                        background:#fef3c7;
                        border:3px dashed #f59e0b;
                        border-radius:18px;
                        padding:28px;
                        margin-bottom:30px;
                    ">

                        <div style="
                            font-size:46px;
                            font-weight:bold;
                            letter-spacing:12px;
                            color:#b45309;
                            font-family:monospace;
                        ">
                            {otp}
                        </div>

                    </div>

                    <p style="
                        color:#78716c;
                        font-size:14px;
                        line-height:1.8;
                    ">
                        ⚠ Never share this OTP with anyone.<br>
                        Our support team will never ask for your verification code.
                    </p>

                </div>

                <!-- Footer -->
                <div style="
                    background:#fffbeb;
                    border-top:1px solid #fde68a;
                    padding:20px;
                    text-align:center;
                    font-size:12px;
                    color:#a16207;
                ">
                    © 2026 Secure Authentication System
                </div>

            </div>

        </div>

        """
    )
            mail.send(msg)
            session['otp'] = str(otp)
            return redirect(url_for('verify_forgot_otp'))
    return render_template("forgot_password.html")
    
@app.route('/verify_forgot_otp',methods=["GET","POST"])
def verify_forgot_otp():
    if request.method=="POST":
        user_otp = request.form.get('user_otp')
        if user_otp == session.get('otp'):
            return redirect(url_for('reset_password'))
        else:
            return "Wrong OTP"
    return render_template("verify_forgot_otp.html")

@app.route('/reset_password',methods=["GET","POST"])
def reset_password():
    if request.method=="POST":
        Password = request.form.get("Password")
        ConfirmPassword = request.form.get("ConfirmPassword")
        hash_password = generate_password_hash(Password)
        print(Password)
        print(ConfirmPassword)
        if Password == ConfirmPassword: 
            user = Users.query.filter_by(Email=session.get('email')).first()
            if user:
                user.Password = hash_password
                db.session.commit()
                print("sab chal rha hai")
                print(Password)
                return render_template("login.html",error="Your Password is changed now you can Login")
            else:
                return render_template("forgot_password.html",error="User Not Found")
        else:
            return render_template("reset_password.html",error="Please Use same Passwords")
    return render_template("reset_password.html")

@app.route('/signup', methods=["GET","POST"])
def signup():
    if request.method=="POST":
            First_Name = request.form.get("First_Name")
            Last_Name = request.form.get("Last_Name")
            Email = request.form.get("Email")
            Password = request.form.get("Password")
            hash_password=generate_password_hash(Password)
            Conform_Password = request.form.get("Conform_Password")
            existing_user = Users.query.filter_by(Email=Email).first()

            if existing_user:
                return render_template(
                    "signup.html",
                    error="Email already registered"
                )
            if Password == Conform_Password:
                is_admin_user = (Email == 'admin@gmail.com')
                session['First_Name'] = First_Name
                session['Last_Name'] = Last_Name
                session['Email'] = Email
                session['Password'] = hash_password
                session['is_admin'] = is_admin_user
                otp = random.randint(000000,999999)
                session['otp']=str(otp)
                print("Email : ",Email)
                msg = Message(
                    subject='Verification Code',
                    recipients=[Email],
                    html=f"""

                    <div style="
                        background:#f4f7fb;
                        padding:40px 20px;
                        font-family:Arial,sans-serif;
                    ">

                        <div style="
                            max-width:520px;
                            background:white;
                            margin:auto;
                            border-radius:16px;
                            overflow:hidden;
                            box-shadow:0 10px 25px rgba(0,0,0,0.08);
                        ">

                            <div style="
                                background:linear-gradient(135deg,#4F46E5,#7C3AED);
                                padding:30px;
                                text-align:center;
                            ">

                                <h1 style="
                                    color:white;
                                    margin:0;
                                    font-size:28px;
                                ">
                                    Secure Verification
                                </h1>

                            </div>

                            <div style="padding:40px;text-align:center;">

                                <h2 style="
                                    color:#222;
                                    margin-bottom:10px;
                                ">
                                    Your OTP Code
                                </h2>

                                <p style="
                                    color:#666;
                                    font-size:16px;
                                    line-height:1.6;
                                ">
                                    Use the verification code below to continue.
                                </p>

                                <div style="
                                    background:#f3f4f6;
                                    padding:20px;
                                    border-radius:12px;
                                    margin:30px 0;
                                    letter-spacing:10px;
                                    font-size:36px;
                                    font-weight:bold;
                                    color:#4F46E5;
                                ">
                                    {otp}
                                </div>

                                <p style="
                                    color:#777;
                                    font-size:14px;
                                    line-height:1.7;
                                ">
                                    
                                    Never share your OTP with anyone.
                                </p>


                            </div>

                            <div style="
                                background:#fafafa;
                                padding:20px;
                                text-align:center;
                                border-top:1px solid #eee;
                                color:#999;
                                font-size:12px;
                            ">
                                © 2026 Secure Authentication System
                            </div>

                        </div>

                    </div>

                    """
                
                )
                print("mail likh gayi")
                mail.send(msg)
                return redirect(url_for('verification'))
            else:
                 return render_template("signup.html",error = "Passwords do not match")
    return render_template("signup.html")
 
@app.route('/verification',methods=["GET","POST"])
def verification():
    if request.method=="POST":
        if 'user' in session:
            return redirect(url_for('dashboard'))
        else:
            user_otp = request.form.get('user_otp')
            if user_otp == session['otp']:
                add_user = Users(

                    First_Name = session.get('First_Name'),
                    Last_Name = session.get('Last_Name'),
                    Email = session.get('Email'),
                    Password = session.get('Password'),
                    is_admin = session.get('is_admin')

                )

                db.session.add(add_user)
                db.session.commit()
                session["user"] = session.get('Email')
                return redirect(url_for('dashboard'))
            else:
                return render_template("signup.html",error="Wrong OTP")
            
    return render_template("verification.html")

@app.route('/dashboard')
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    user = Users.query.filter_by(Email=session["user"]).first()
    query = request.args.get('q', '').strip()

    if query:
        from sqlalchemy import case, or_
        # Priority: title > description > content
        title_match = Vlogs.title.ilike(f'%{query}%')
        desc_match = Vlogs.description.ilike(f'%{query}%')
        content_match = Vlogs.content.ilike(f'%{query}%')

        search_filter = or_(title_match, desc_match, content_match)

        # Assign weights: title=0, description=1, content=2 for priority ordering
        relevance = case(
            (title_match, 0),
            (desc_match, 1),
            else_=2
        )

        all_vlogs = Vlogs.query \
            .filter(search_filter) \
            .order_by(relevance, Vlogs.created_at.desc()) \
            .all()
    else:
        all_vlogs = Vlogs.query.order_by(Vlogs.created_at.desc()).all()

    return render_template('dashboard.html', user=user, vlogs=all_vlogs, query=query)


@app.route('/vlog/new', methods=["GET", "POST"])
def create_vlog():
    if "user" not in session:
        return redirect(url_for("login"))

    user = Users.query.filter_by(Email=session["user"]).first()

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        content = request.form.get("content")
        cover_image_url = request.form.get("cover_image_url")

        if not title or not description or not content:
            return render_template('vlog_form.html', user=user, error="Title, description, and content are required.")

        new_vlog = Vlogs(
            title=title,
            description=description,
            content=content,
            cover_image_url=cover_image_url or '',
            author_id=user.serial_number
        )
        db.session.add(new_vlog)
        db.session.commit()

        return redirect(url_for("dashboard"))

    return render_template('vlog_form.html', user=user, vlog=None)


@app.route('/vlog/<int:vlog_id>')
def view_vlog(vlog_id):
    if "user" not in session:
        return redirect(url_for("login"))

    user = Users.query.filter_by(Email=session["user"]).first()
    vlog = Vlogs.query.get_or_404(vlog_id)

    return render_template('vlog_view.html', user=user, vlog=vlog)


@app.route('/vlog/<int:vlog_id>/edit', methods=["GET", "POST"])
def edit_vlog(vlog_id):
    if "user" not in session:
        return redirect(url_for("login"))

    user = Users.query.filter_by(Email=session["user"]).first()
    vlog = Vlogs.query.get_or_404(vlog_id)

    if vlog.author_id != user.serial_number and not user.is_admin:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        vlog.title = request.form.get("title")
        vlog.description = request.form.get("description")
        vlog.content = request.form.get("content")
        vlog.cover_image_url = request.form.get("cover_image_url") or ''
        db.session.commit()

        return redirect(url_for("view_vlog", vlog_id=vlog.id))

    return render_template('vlog_form.html', user=user, vlog=vlog)


@app.route('/vlog/<int:vlog_id>/delete', methods=["POST"])
def delete_vlog(vlog_id):
    if "user" not in session:
        return redirect(url_for("login"))

    user = Users.query.filter_by(Email=session["user"]).first()
    vlog = Vlogs.query.get_or_404(vlog_id)

    if vlog.author_id != user.serial_number and not user.is_admin:
        return redirect(url_for("dashboard"))

    db.session.delete(vlog)
    db.session.commit()

    return redirect(url_for("dashboard"))


@app.route('/explore')
def explore():
    all_vlogs = Vlogs.query.order_by(Vlogs.created_at.desc()).all()
    return render_template('explore.html', vlogs=all_vlogs)


@app.route('/trending')
def trending():
    all_vlogs = Vlogs.query.order_by(Vlogs.created_at.desc()).all()
    return render_template('trending.html', vlogs=all_vlogs)


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.route('/terms')
def terms():
    return render_template('terms.html')


@app.route('/contact', methods=["GET", "POST"])
def contact():
    success = False
    error = None
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        subject = request.form.get("subject", "")
        message = request.form.get("message", "")

        if not name or not email or not subject or not message:
            error = "Please fill in all fields."
        else:
            # Always save to database first
            contact_msg = ContactMessage(
                name=name,
                email=email,
                subject=subject,
                message=message,
                email_sent=False
            )
            db.session.add(contact_msg)
            db.session.commit()

            # Try sending email
            if mail.username and mail.password:
                try:
                    msg = Message(
                        subject=f"[VlogVerse Contact] {subject}",
                        recipients=[mail.username],
                        reply_to=email,
                        body=f"""New Contact Form Submission

From: {name} ({email})
Subject: {subject}

Message:
{message}
"""
                    )
                    mail.send(msg)
                    contact_msg.email_sent = True
                    db.session.commit()
                except Exception as e:
                    app.logger.error(f"Contact form email error: {str(e)}")

            success = True

    return render_template('contact.html', success=success, error=error)


@app.route('/admin')
def admin_panel():
    if "user" not in session:
        return redirect(url_for("login"))

    user = Users.query.filter_by(Email=session["user"]).first()
    if not user or not user.is_admin:
        return redirect(url_for("dashboard"))

    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    all_vlogs = Vlogs.query.order_by(Vlogs.created_at.desc()).all()
    all_users = Users.query.order_by(Users.serial_number.asc()).all()
    error = request.args.get('error', '')

    return render_template('admin.html', user=user, messages=messages, vlogs=all_vlogs, users=all_users, error=error)


@app.route('/admin/user/add', methods=["POST"])
def admin_add_user():
    if "user" not in session:
        return redirect(url_for("login"))

    admin_user = Users.query.filter_by(Email=session["user"]).first()
    if not admin_user or not admin_user.is_admin:
        return redirect(url_for("dashboard"))

    first_name = request.form.get("first_name", "")
    last_name = request.form.get("last_name", "")
    email = request.form.get("email", "")
    password = request.form.get("password", "")

    if not first_name or not email or not password:
        return redirect(url_for("admin_panel", error="First name, email and password are required."))

    existing = Users.query.filter_by(Email=email).first()
    if existing:
        return redirect(url_for("admin_panel", error="Email already registered."))

    new_user = Users(
        First_Name=first_name,
        Last_Name=last_name,
        Email=email,
        Password=generate_password_hash(password)
    )
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("admin_panel"))


@app.route('/admin/user/<int:user_id>/delete', methods=["POST"])
def admin_delete_user(user_id):
    if "user" not in session:
        return redirect(url_for("login"))

    admin_user = Users.query.filter_by(Email=session["user"]).first()
    if not admin_user or not admin_user.is_admin:
        return redirect(url_for("dashboard"))

    target = Users.query.get_or_404(user_id)
    if target.is_admin:
        return redirect(url_for("admin_panel"))

    # Delete their vlogs first, then the user
    Vlogs.query.filter_by(author_id=target.serial_number).delete()
    db.session.delete(target)
    db.session.commit()

    return redirect(url_for("admin_panel"))


@app.route('/admin/vlog/<int:vlog_id>/delete', methods=["POST"])
def admin_delete_vlog(vlog_id):
    if "user" not in session:
        return redirect(url_for("login"))

    user = Users.query.filter_by(Email=session["user"]).first()
    if not user or not user.is_admin:
        return redirect(url_for("dashboard"))

    vlog = Vlogs.query.get_or_404(vlog_id)
    db.session.delete(vlog)
    db.session.commit()

    return redirect(url_for("admin_panel"))


@app.route('/messages')
def view_messages():
    if "user" not in session:
        return redirect(url_for("login"))

    user = Users.query.filter_by(Email=session["user"]).first()
    if not user or not user.is_admin:
        return redirect(url_for("dashboard"))

    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('messages.html', user=user, messages=messages)


@app.route('/messages/<int:msg_id>/delete', methods=["POST"])
def delete_message(msg_id):
    if "user" not in session:
        return redirect(url_for("login"))

    user = Users.query.filter_by(Email=session["user"]).first()
    if not user or not user.is_admin:
        return redirect(url_for("dashboard"))

    msg = ContactMessage.query.get_or_404(msg_id)
    db.session.delete(msg)
    db.session.commit()
    return redirect(url_for("view_messages"))


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/logout')
def logout():

    session.pop("user", None)

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True, port=5001)
