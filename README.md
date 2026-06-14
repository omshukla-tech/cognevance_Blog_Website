# 🎬 VlogVerse — Your Story Starts Here

VlogVerse is a full-featured vlogging platform built with Flask. It allows creators to sign up, write and publish vlogs, browse content from others, and manage their work through an intuitive dashboard. An admin panel provides oversight of users, vlogs, and contact form submissions.

---

## ✨ Features

- **User Authentication** — Sign up with email OTP verification, login, and password reset via email
- **Vlog Management** — Create, edit, preview, and delete vlogs with rich HTML content and cover images
- **Search** — Full-text search across vlog titles, descriptions, and content with relevance-based ordering
- **Explore & Trending** — Browse all vlogs or a featured ranking feed
- **Contact Form** — Visitors can send messages; stored in DB and forwarded via email
- **Admin Panel** — Tabbed dashboard for managing messages, vlogs, and users
- **Help Center** — Interactive FAQ with accordion and live search filtering
- **Static Pages** — Privacy Policy, Terms of Service, Contact, and Help pages
- **Responsive UI** — Dark-themed, glassmorphic design with animated backgrounds, floating particles, and scroll-triggered animations
- **Live OTP Timer** — Resend countdown with animated UX feedback during signup

---

## 🧰 Technologies Used

| Layer        | Technology                                                          |
| ------------ | ------------------------------------------------------------------- |
| **Backend**  | Python 3, Flask                                                     |
| **ORM**      | Flask-SQLAlchemy                                                    |
| **Database** | SQLite (`instance/database.db`)                                     |
| **Auth**     | Werkzeug (`generate_password_hash` / `check_password_hash`)         |
| **Email**    | Flask-Mail via SMTP (Elastic Email)                                 |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript (ES6)                               |
| **Icons**    | Font Awesome 6.5                                                    |
| **Fonts**    | Google Fonts (Inter, Space Grotesk)                                 |
| **Templating** | Jinja2                                                            |
| **Config**   | `python-dotenv` for environment variables                           |

---

## 📁 Project Structure

```
VlogVerse/
├── app.py                       # Flask application (routes, models, config)
├── .env                         # Environment variables (MAIL settings, secret key)
├── requirements.txt             # Python dependencies
├── instance/
│   └── database.db              # SQLite database
├── static/
│   ├── css/
│   │   └── style.css            # All custom styles (glassmorphism, animations, responsive)
│   └── js/
│       └── script.js            # Frontend interactivity (particles, counters, mobile menu, etc.)
└── templates/
    ├── base.html                # Base layout (nav, particles, footer, scripts)
    ├── index.html               # Landing / hero page
    ├── login.html               # Login page
    ├── signup.html              # Registration page (with password strength meter)
    ├── verification.html        # OTP verification step (signup)
    ├── forgot_password.html     # Email input to request password reset
    ├── verify_forgot_otp.html   # OTP verification step (password reset)
    ├── reset_password.html      # Set new password
    ├── dashboard.html           # User dashboard (search + vlog cards)
    ├── vlog_form.html           # Create / edit vlog form
    ├── vlog_view.html           # Single vlog detail view
    ├── explore.html             # Browse all vlogs
    ├── trending.html            # Ranked vlog list
    ├── admin.html               # Admin panel (messages, vlogs, users tabs)
    ├── messages.html            # Standalone messages list page
    ├── contact.html             # Contact form page
    ├── help.html                # FAQ accordion with search
    ├── privacy.html             # Privacy policy
    └── terms.html               # Terms of service
```

---

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8+
- pip
- (Optional) Virtual environment (`venv`)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/vlogverse.git
cd vlogverse
```

### 2. Create & Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# or
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install flask flask-sqlalchemy flask-mail werkzeug python-dotenv
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
MAIL_SERVER=smtp.elasticemail.com
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_smtp_password
MAIL_DEFAULT_SENDER=your_email@example.com
FLASK_SECRET_KEY=your_secret_key_here
```

- `MAIL_SERVER`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_DEFAULT_SENDER` — SMTP credentials (Elastic Email or any SMTP provider).
- `FLASK_SECRET_KEY` — Used for session signing (falls back to `"mysecretkey"` in code if not set).

> **Note:** The admin account is auto-assigned to the user with email `admin@gmail.com`. To use this, either create that account via signup or adjust the email check in `app.py`.

### 5. Initialize the Database

The database tables are created automatically when the app starts:

```bash
python app.py
```

Tables (`users`, `vlogs`, `contact_message`) will be created inside `instance/database.db`.

### 6. Run the Application

```bash
python app.py
```

The server starts at `http://0.0.0.0:5001` by default.

Open [http://localhost:5001](http://localhost:5001) in your browser.

---

## 🔌 API Routes

### Authentication

| Method | Route                   | Description                                  |
| ------ | ----------------------- | -------------------------------------------- |
| GET    | `/login`                | Render login page                            |
| POST   | `/login`                | Authenticate user and create session         |
| GET    | `/signup`               | Render signup page                           |
| POST   | `/signup`               | Register user, send OTP email                |
| GET    | `/verification`         | Render OTP verification page                 |
| POST   | `/verification`         | Verify OTP and create user in database       |
| GET    | `/forget_password`      | Render forgot password page                  |
| POST   | `/forget_password`      | Send password reset OTP email                |
| GET    | `/verify_forgot_otp`    | Render OTP verification for password reset   |
| POST   | `/verify_forgot_otp`    | Verify OTP for password reset                |
| GET    | `/reset_password`       | Render reset password page                   |
| POST   | `/reset_password`       | Update password in database                  |
| GET    | `/logout`               | Clear session and redirect to login          |

### Vlogs

| Method | Route                  | Description                              |
| ------ | ---------------------- | ---------------------------------------- |
| GET    | `/dashboard`           | User dashboard (optional `?q=` search)   |
| GET    | `/vlog/new`            | Render create vlog form                  |
| POST   | `/vlog/new`            | Create a new vlog                        |
| GET    | `/vlog/<id>`           | View a single vlog                       |
| GET    | `/vlog/<id>/edit`      | Render edit vlog form                    |
| POST   | `/vlog/<id>/edit`      | Update vlog                              |
| POST   | `/vlog/<id>/delete`    | Delete a vlog (owner only)               |
| GET    | `/explore`             | Browse all vlogs (newest first)          |
| GET    | `/trending`            | Ranked vlog list (newest first)          |

### Contact & Messages

| Method | Route                    | Description                              |
| ------ | ------------------------ | ---------------------------------------- |
| GET    | `/contact`               | Render contact form                      |
| POST   | `/contact`               | Submit contact message (saved + emailed) |
| GET    | `/messages`              | View all contact messages (admin only)   |
| POST   | `/messages/<id>/delete`  | Delete a message (admin only)            |

### Admin

| Method | Route                       | Description                              |
| ------ | --------------------------- | ---------------------------------------- |
| GET    | `/admin`                    | Admin panel (messages, vlogs, users)     |
| POST   | `/admin/user/add`           | Manually add a user (admin only)         |
| POST   | `/admin/user/<id>/delete`   | Delete a user and their vlogs (admin only) |
| POST   | `/admin/vlog/<id>/delete`   | Delete any vlog (admin only)             |

### Static Pages

| Method | Route        | Description             |
| ------ | ------------ | ----------------------- |
| GET    | `/`          | Landing / hero page     |
| GET    | `/privacy`   | Privacy policy          |
| GET    | `/terms`     | Terms of service        |
| GET    | `/help`      | Help center (FAQ)       |

---

## 🗄️ Database Schema

### `users`

| Column          | Type     | Notes                         |
| --------------- | -------- | ----------------------------- |
| `serial_number` | Integer  | Primary key, auto-increment   |
| `First_Name`    | String   | Required, max 15 chars        |
| `Last_Name`     | String   | Optional, max 10 chars        |
| `Email`         | String   | Required, unique, max 50 chars |
| `Password`      | String   | Hashed with Werkzeug          |
| `is_admin`      | Boolean  | Default `False`               |
| `vlogs`         | Relation | One-to-many with `Vlogs`      |

### `vlogs`

| Column            | Type      | Notes                                |
| ----------------- | --------- | ------------------------------------ |
| `id`              | Integer   | Primary key, auto-increment          |
| `title`           | String    | Required, max 100 chars              |
| `description`     | Text      | Required                             |
| `content`         | Text      | Required (HTML supported)            |
| `cover_image_url` | String    | Optional, max 500 chars              |
| `created_at`      | DateTime  | Default: `utcnow`                    |
| `updated_at`      | DateTime  | Auto-updates on edit                 |
| `author_id`       | Integer   | Foreign key → `users.serial_number`  |

### `contact_message`

| Column       | Type      | Notes                               |
| ------------ | --------- | ----------------------------------- |
| `id`         | Integer   | Primary key, auto-increment         |
| `name`       | String    | Required, max 100 chars             |
| `email`      | String    | Required, max 100 chars             |
| `subject`    | String    | Required, max 200 chars             |
| `message`    | Text      | Required                            |
| `email_sent` | Boolean   | Whether the email notification sent |
| `created_at` | DateTime  | Default: `utcnow`                   |

---

## 🔄 User Workflow

```
Landing Page (/) → Explore (/explore) or Trending (/trending)
       │
       ├── Sign Up (/signup)
       │     └── Verify OTP (/verification)
       │           └── Auto-login → Dashboard (/dashboard)
       │
       ├── Log In (/login)
       │     └── Forgot Password?
       │           ├── Enter email (/forget_password)
       │           ├── Verify OTP (/verify_forgot_otp)
       │           └── Reset password (/reset_password)
       │
       ├── Dashboard (/dashboard) — search, browse, create vlogs
       │     ├── Create Vlog (/vlog/new)
       │     ├── Edit Vlog (/vlog/<id>/edit)
       │     ├── View Vlog (/vlog/<id>)
       │     └── Delete Vlog (POST /vlog/<id>/delete)
       │
       ├── Admin Panel (/admin)
       │     ├── Messages tab — read & delete contact submissions
       │     ├── Vlogs tab — view, edit, delete any vlog
       │     └── Users tab — add or delete users
       │
       └── Static Pages: Privacy, Terms, Contact, Help
```

---

## 🎨 UI / UX Highlights

- **Dark theme** with glassmorphism (`backdrop-filter: blur`, semi-transparent borders)
- **Animated background** — gradient shift, floating shapes, particle system
- **Counter animation** — stats on the hero page animate on scroll
- **Mobile-responsive** — hamburger menu, stacked layouts for small screens
- **Interactive forms** — floating labels, password visibility toggle, strength meter in signup
- **Accordion FAQ** on the Help page with live search filtering
- **Admin tabs** — client-side tab switching with badge counts
- **Ripple effect** on hero buttons
- **Scroll-reveal** feature cards with staggered delays

---

## ⚙️ Configuration

All configuration lives in `app.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = "mysecretkey"  # Override via .env or environment
```

Email config is loaded from environment variables via `python-dotenv`:

```python
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
```

Server port and debug mode (set in `if __name__ == "__main__"`):

```python
app.run(host="0.0.0.0", debug=True, port=5001)
```

---

## 📦 Dependencies

```
flask
flask-sqlalchemy
flask-mail
werkzeug
python-dotenv
```

Install with:

```bash
pip install flask flask-sqlalchemy flask-mail werkzeug python-dotenv
```

---

## 🔐 Security Notes

- Passwords are hashed with Werkzeug's `generate_password_hash` (pbkdf2:sha256).
- User sessions are signed with `app.secret_key`.
- OTPs are stored in the session (not persisted) — ephemeral per browser session.
- Admin routes check `user.is_admin` before allowing access.
- Delete operations require confirmation via `confirm()` dialog.
- SQL injection is mitigated by using SQLAlchemy's ORM parameterized queries.
- Contact form email delivery failures are logged and flagged in the database (not user-visible).

---

## 🧪 Running Locally with Gmail / Other SMTP

If you don't have Elastic Email, you can use any SMTP provider. For Gmail (App Password required):

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=your@gmail.com
```

---

## 🛠️ Future Improvements

- Profile pages for users
- Comments & likes on vlogs
- Rich text editor for vlog content (WYSIWYG)
- Image upload instead of URL-only cover images
- Pagination for large vlog collections
- Email verification link (instead of / in addition to OTP)
- API tokens for third-party integrations

---

## 📄 License

This project is for demonstration and educational purposes.

---

<p align="center">Made with ❤️ using Flask & modern CSS/JS</p>
