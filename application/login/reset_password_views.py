from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash
from application.setup import db, mail, s, User
from flask_mail import Message
from flask_login import current_user

reset_blueprint = Blueprint('reset_blueprint', __name__)


@reset_blueprint.route('/reset_password', methods=['GET', 'POST'])
def reset_password_page():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            try:
                token = s.dumps(email, salt='email-reset')
                msg = Message('Reset Your Password',
                              recipients=[email])

                link = url_for('reset_blueprint.reset_with_token', token=token, _external=True)
                msg.body = f'Your link to reset your password is {link}'
                mail.send(msg)
                flash('На почту выслана ссылка для сброса пароля')
                return redirect(url_for('login_blueprint.login_page'))
            except:
                # TODO: Добавить логирование ошибки и отправку ссылки на почту
                flash('Что то пошло не так, оставьте свою почту в форме обратной связи')
                return redirect(url_for("feedback_blueprint.feedback_page"))
    return render_template('reset_password.html', user=current_user)


@reset_blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    try:
        email = s.loads(token, salt='email-reset', max_age=3600)
    except:
        return redirect(url_for('reset_request'))
    if request.method == 'POST':
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        user.password = generate_password_hash(password)
        db.session.commit()
        return redirect(url_for('login_blueprint.login_page'))
    return render_template('reset_password_with_token.html', token=token, user=current_user)
