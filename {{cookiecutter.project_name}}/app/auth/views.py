from datetime import datetime as dt
import logging
from secrets import token_urlsafe
from flask import (
    request,
    render_template,
    flash,
    redirect,
    Blueprint,
    url_for,
    current_app
)
from flask_babel import lazy_gettext as _l
from flask_login import current_user, logout_user, login_user

from app.extensions import db
from app.forms import LoginForm, RegisterForm, ResetPasswordReq, ResetPassword
from app.models import User
from app.email import send_email

logger = logging.getLogger(__name__)

bp = Blueprint('auth', __name__, url_prefix="/auth", static_folder="../static")


def create_user(form):
    username = form.username.data
    email = form.email.data
    existing_user = User.query.filter(
        User.username == username or User.email == email
    ).first()
    if existing_user:
        flash(_l(f'{username} ({email}) already created!'), 'success')
        return redirect(url_for('auth.login'))
    else:
        now = dt.now().replace(second=0, microsecond=0)
        new_user = User(
            username=username,
            email=email,
            created=now,
            token=token_urlsafe(),
            token_expiration=dt.now()
        )
        new_user.set_password(form.password.data)
        flash(_l(f'{username} you are now a registered'), 'success')
        db.session.add(new_user)
        db.session.commit()
    logger.info('Form action')
    return True


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_l('Invalid username or password'), 'info')
            return redirect(url_for('auth.login'))
        login_user(user)
        next_page = request.args.get('next')
        return redirect(next_page or url_for('main.index'))
    return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        create_user(form)
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@bp.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordReq()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            token = user.verify_expiration_token()
            db.session.commit()
            send_email(
                _l('Request change password'),
                sender=current_app.config['ADMINS'][0],
                recipients=[user.email],
                text_body=render_template(
                    'email/reset_password.txt',
                    token=token),
                html_body=render_template(
                    'email/reset_password.html',
                    token=token)
            )
            flash("Email sent, check your mail now!", "info")
            return redirect(url_for('auth.login'))
        flash("This email not registered", "info")
    return render_template('auth/reset_password_req.html', form=form)


@bp.route("/reset_password_token/<token>", methods=['GET', 'POST'])
def reset_password_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPassword()
    if form.validate_on_submit():
        user = User.query.filter_by(token=token).first()
        if user:
            user.set_password(form.password.data)
            db.session.commit()
            flash("Password changed!", "info")
            return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
