# app/auth/routes.py

from . import auth_bp
from app import login_manager
from flask import render_template, redirect, url_for, flash, request, session, current_app
#from flask_principal import Principal, Permission, Identity, AnonymousIdentity, RoleNeed, UserNeed, identity_loaded, identity_changed
from .models import User
from .forms.login import LoginForm
from .forms.register import RegisterForm
from .utils import generate_confirmation_token, confirm_token, send_email
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
import datetime

#le decimos a Flask-Login como obtener un usuario
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@auth_bp.route('/trivia/login', methods=['GET', 'POST'])
def login():
    #if current_user.is_authenticated:
    #    return redirect(url_for('public.index_trivia'))
    form = LoginForm()
    if form.validate_on_submit():
        #get by email valida
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            # funcion provista por Flask-Login, el segundo parametro gestion el "recordar"
            login_user(user, remember=form.remember_me.data)

            next_page = request.args.get('next', None)
            if not next_page:
                next_page = url_for('public.index_trivia')

            app_actual = current_app._get_current_object()
            #identity_changed.send(app_actual, identity=Identity(user.id))
            return redirect(url_for('public.index_trivia'))
        else:
            flash('Usuario o contraseña inválido')
            return redirect(url_for('auth.login'))
    # no loggeado, dibujamos el login con el form vacio
    return render_template('login.html', form=form)

@auth_bp.route("/trivia/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('public.index_trivia'))
    form = RegisterForm()
    error = None
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # Comprobamos que no hay ya un usuario con ese email
        user = User.get_by_email(email)
        if user is not None:
            flash('El email {} ya está siendo utilizado por otro usuario'.format(email))
        else:
            # Creamos el usuario y lo guardamos
            user = User(name=username, email=email)
            user.set_password(password)
            user.save()
            # Agrego codigo del token
            token = generate_confirmation_token(user.email)
            confirm_url = url_for('auth.confirm_email', token=token, _external=True)
            html = render_template('activate_register.html', confirm_url=confirm_url)
            send_email(user.email, current_app.config['MAIL_SUBJECT'], html)
            # Dejamos al usuario logueado
            #login_user(user, remember=True)
            #app_actual = current_app._get_current_object()
            #identity_changed.send(app_actual, identity=Identity(user.id))
            return redirect(url_for('public.index_trivia'))
    return render_template("register.html", form=form)

# Confirmo el token
@auth_bp.route('/trivia/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.is_confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.is_confirmed = True
        user.email_confirmed_at = datetime.datetime.now()
        user.save()

        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('public.index_trivia'))



@auth_bp.route('/trivia/logout')
def logout():
    logout_user()
    # Flask-Principal: Remove session keys
    """
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Flask-Principal: the user is now anonymous
    app_actual = current_app._get_current_object()
    identity_changed.send(app_actual, identity=AnonymousIdentity())
    """
    return redirect(url_for('public.index_trivia'))






