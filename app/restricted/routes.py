# app/restricted/routes.py

from . import restricted_bp

from app import db, admin
from flask_login import current_user, login_required
#from flask_principal import Permission, RoleNeed, UserNeed, identity_loaded
from flask import render_template,request, url_for, redirect
from flask_admin.contrib.sqla import ModelView

from app.auth.models import User
from app.public.models import Categoria, Pregunta, Respuesta
from flask_admin import AdminIndexView


# Agregamos las necesidades a una identidad, una vez que se loguee el usuario.
#admin_permission = Permission(RoleNeed('admin'))

"""
@identity_loaded.connect
def on_identity_loaded(sender, identity):
    # Seteamos la identidad al usuario
    identity.user = current_user
    # Agregamos una UserNeed a la identidad, con el usuario actual.
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))
    # Agregamos a la identidad la lista de roles que posee el usuario actual.
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.rolename))
"""

class MyModelView(ModelView):
    def is_accessible(self):
        has_auth = current_user.is_authenticated
        role_admin = False
        if has_auth:
            role_admin = current_user.is_admin
        return has_auth and role_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        has_auth = current_user.is_authenticated
        return has_auth
        #has_perm = admin_permission.allows(g.identity)
        #sreturn has_auth and has_perm


admin._set_admin_index_view(MyAdminIndexView())
# agregadmos al admin de todos los modelos
admin.add_view(MyModelView(Categoria, db.session))
admin.add_view(MyModelView(Pregunta, db.session))
admin.add_view(MyModelView(Respuesta, db.session))
admin.add_view(MyModelView(User, db.session))
#admin.add_view(MyModelView(Role, db.session))



@restricted_bp.route('/test')
@login_required
#@admin_permission.require(http_exception=403)
def test_principal():
    return render_template('test.html')
