import os
import re
from datetime import datetime
from functools import wraps

import markdown2
from flask import (
    Flask,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "peb-union-secure-key-123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "instance", "peb_union.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


# --- HELPERS ---
def roles_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                abort(403)
            return f(*args, **kwargs)

        return decorated_view

    return wrapper


def parse_md(text):
    if not text:
        return ""
    return markdown2.markdown(
        text, extras=["fenced-code-blocks", "tables", "break-on-newline"]
    )


def clean_youtube(url):
    """Converts any YT link to embed format for storage safety"""
    if not url:
        return ""
    reg = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(reg, url)
    # FIXED: Corrected the return string logic
    return f"https://www.youtube.com/embed/{match.group(1)}" if match else url


# --- MODELS ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="researcher")
    posts = db.relationship("Post", backref="author_ref", lazy=True)


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    initial = db.Column(db.String(5), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    # Added new column for cropping
    image_position = db.Column(db.String(20), default="center")

    def to_dict(self):
        return {
            "name": self.name,
            "role": self.role,
            "dept": self.department,
            "initial": self.initial,
            "image": self.image_url or "",
            "image_position": self.image_position,
        }


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    date = db.Column(
        db.String(50), default=lambda: datetime.now().strftime("%B %d, %Y")
    )
    post_type = db.Column(db.String(20), default="news")
    category = db.Column(db.String(50), nullable=False)
    summary = db.Column(db.String(500), nullable=False)
    content_raw = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="draft")
    image_url = db.Column(db.String(250), nullable=True)
    video_url = db.Column(db.String(250), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "date": self.date,
            "category": self.category,
            "summary": self.summary,
            "type": self.post_type,
            "video_url": self.video_url,
            "image": self.image_url or "",
            "author": self.author_ref.username,
        }


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --- API ---
@app.route("/api/content")
def get_content_api():
    ptype = request.args.get("type", "news")
    posts = (
        Post.query.filter_by(post_type=ptype, status="published")
        .order_by(Post.id.desc())
        .all()
    )
    return jsonify([post.to_dict() for post in posts])


@app.route("/api/staff")
def get_staff_api():
    members = Staff.query.all()
    return jsonify([m.to_dict() for m in members])


# --- PUBLIC PAGE ROUTES (Fixed 404s) ---


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/staff")
def staff():
    return render_template("staff.html")


@app.route("/charter")
def charter():
    return render_template("charter.html")


@app.route("/news")
def news():
    return render_template("news.html")


@app.route("/articles")
def articles():
    return render_template("articles.html")


@app.route("/interviews")
def interviews():
    return render_template("interviews.html")


@app.route("/activities")
def activities():
    return render_template("activities.html")


@app.route("/mun")
def mun():
    return render_template("mun.html")


@app.route("/peer-support")
def peer_support():
    return render_template("peer-support.html")


@app.route("/market-simulation")
def market_simulation():
    return render_template("market-simulation.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/news/<int:id>")
def news_detail(id):
    post = Post.query.get_or_404(id)
    post.content_html = parse_md(post.content_raw)
    return render_template("detail_view.html", post=post)


# --- AUTH ---
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form.get("username")).first()
        if user and check_password_hash(user.password, request.form.get("password")):
            login_user(user)
            return redirect(url_for("manage_news"))
        flash("Invalid credentials")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


# --- ADMIN ---
@app.route("/admin/manage")
@login_required
def manage_news():
    if current_user.role == "researcher":
        posts = (
            Post.query.filter_by(author_id=current_user.id)
            .order_by(Post.id.desc())
            .all()
        )
    else:
        posts = Post.query.order_by(Post.id.desc()).all()
    return render_template("manage.html", posts=posts)


@app.route("/admin/add", methods=["GET", "POST"])
@login_required
def add_news():
    if request.method == "POST":
        action = request.form.get("action", "draft")
        new_post = Post(
            title=request.form.get("title", "Untitled"),
            post_type=request.form.get("post_type", "news"),
            category=request.form.get("category", "general"),
            summary=request.form.get("summary", ""),
            content_raw=request.form.get("content_raw", ""),
            video_url=clean_youtube(request.form.get("video_url", "")),
            image_url=request.form.get("image_url", ""),
            status=action,
            author_id=current_user.id,
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("manage_news"))
    return render_template("editor.html")


@app.route("/admin/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_news(id):
    post = Post.query.get_or_404(id)
    if current_user.role == "researcher" and post.author_id != current_user.id:
        abort(403)
    if request.method == "POST":
        post.title = request.form.get("title")
        post.post_type = request.form.get("post_type")
        post.category = request.form.get("category")
        post.summary = request.form.get("summary")
        post.content_raw = request.form.get("content_raw")
        post.video_url = clean_youtube(request.form.get("video_url"))
        post.image_url = request.form.get("image_url")
        post.status = request.form.get("action")
        db.session.commit()
        return redirect(url_for("manage_news"))
    return render_template("editor.html", post=post)


@app.route("/admin/delete/<int:id>")
@login_required
@roles_required("admin")
def delete_news(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("manage_news"))


@app.route("/admin/staff/add", methods=["GET", "POST"])
@login_required
@roles_required("admin")
def add_staff():
    if request.method == "POST":
        # Get data from the form
        name = request.form.get("name")
        new_member = Staff(
            name=name,
            role=request.form.get("role"),
            department=request.form.get("department"),
            initial=name[0] if name else "?",
            image_url=request.form.get("image_url"),
            # Capture the value from the <select> dropdown in your form
            image_position=request.form.get("image_position", "center"),
        )
        db.session.add(new_member)
        db.session.commit()
        flash("Staff member added successfully!")
        return redirect(url_for("manage_news"))

    return render_template("edit_staff.html")


# Template Save/Update Compatibility
@app.route("/admin/editor/save", methods=["POST"])
@login_required
def editor_save():
    return add_news()


@app.route("/admin/editor/update/<int:id>", methods=["POST"])
@login_required
def editor_update(id):
    return edit_news(id)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
