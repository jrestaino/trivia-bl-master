#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.public.models import Categoria, Pregunta, Respuesta
from app.auth.models import User, Role

from app import create_app, db
app = create_app()
with app.app_context():


    db.drop_all()
    db.create_all()

    # categorias
    c_geogra = Categoria(descripcion="Geografía")
    c_deporte = Categoria(descripcion="Deportes")
    c_arte = Categoria(descripcion="Arte")

    # preguntas
    q_Laos = Pregunta(text="¿Cuál es la capital de Laos?", categoria = c_geogra)
    r1_Laos = Respuesta(text="Bangkok", correcta=False, pregunta=q_Laos)
    r2_Laos = Respuesta(text="Phom Penh", correcta=False, pregunta=q_Laos)
    r3_Laos  = Respuesta(text="Vientiane", correcta=True, pregunta=q_Laos)

    q_Armenia = Pregunta(text="¿Cuál es la población aproximada de Armenia?", categoria = c_geogra)
    r1_Armenia = Respuesta(text="1.500.000", correcta=False, pregunta=q_Armenia)
    r2_Armenia = Respuesta(text="3.500.000", correcta=False, pregunta=q_Armenia)
    r3_Armenia = Respuesta(text="3.000.000", correcta=True, pregunta=q_Armenia)


    q_mundial = Pregunta(text="¿En qué país se jugó la Copa del Mundo de 1962?", categoria = c_deporte)
    r1_Armenia = Respuesta(text="Brasil", correcta=False, pregunta=q_mundial)
    r2_Armenia = Respuesta(text="Chile", correcta=True, pregunta=q_mundial)
    r3_Armenia = Respuesta(text="Italia", correcta=False, pregunta=q_mundial)

    q_f1_1 = Pregunta(text="¿Quien salio campeon del mundo en 1991", categoria = c_deporte)
    r1_f1_1 = Respuesta(text="Senna", correcta=True, pregunta=q_mundial)
    r1_f1_1 = Respuesta(text="Prost", correcta=False, pregunta=q_mundial)
    r1_f1_1 = Respuesta(text="Mansell", correcta=False, pregunta=q_mundial)

    # Arte
    c_arte = Categoria(descripcion="Arte")
    q_Gioconda = Pregunta(text="¿Quién pintó La Gioconda (Mona Lisa)?", categoria=c_arte)
    r1_Gioconda = Respuesta(text="Da Vinci", correcta=True, pregunta=q_Gioconda)
    r2_Gioconda = Respuesta(text="Dalí", correcta=False, pregunta=q_Gioconda)
    r3_Gioconda = Respuesta(text="Miguel Ángel", correcta=False, pregunta=q_Gioconda)

    q_Gogh = Pregunta(text="¿En qué siglo nació Van Gogh?", categoria=c_arte)
    r1_Gogh = Respuesta(text="XVIII", correcta=False, pregunta=q_Gogh)
    r2_Gogh = Respuesta(text="XIX", correcta=True, pregunta=q_Gogh)
    r3_Gogh = Respuesta(text="XVII", correcta=False, pregunta=q_Gogh)

    '''
    #Usuarios
    u_u1 = User(name = "Jose", email = "jrestaino@antel.com.uy")
    # el pass lo seteamos con el método set_password para que se guarde con hash
    u_u1.set_password("jose10")


    # lo hago agent
    u_u2 = User(name = "Maria", email = "maria@antel.com.uy")
    u_u2.set_password("maria10")

    u_u3 = User(name = "Natalia", email = "natalia@antel.com.uy")
    u_u3.set_password("natalia10")
    '''

    db.session.add(c_arte)
    db.session.add(q_Gioconda)
    db.session.add(r1_Gioconda)
    db.session.add(r2_Gioconda)
    db.session.add(r3_Gioconda)
    db.session.add(q_Gogh)
    db.session.add(r1_Gogh)
    db.session.add(r2_Gogh)
    db.session.add(r3_Gogh)

    db.session.add(c_geogra)
    db.session.add(c_deporte)
    db.session.add(q_Laos)
    db.session.add(q_Armenia)
    db.session.add(q_mundial)

    '''
    db.session.add(u_u1)
    db.session.add(u_u2)
    db.session.add(u_u3)
    db.session.commit()
    
    # le agrego los roles Agent y Admin
    u_u1.roles.append(Role(name='Admin'))
    u_u1.roles.append(Role(name='Agent'))
    u_u2.roles.append(Role(name='Agent'))
    u_u3.roles.append(Role(name='Agent'))
    db.session.add(u_u1)
    db.session.add(u_u2)
    db.session.add(u_u3)
    '''
    db.session.commit()


    # creamos otros usuarios (…) y los recorremos
    categorias = Categoria.query.all()
    for c in categorias:
        print(c.id, c.descripcion)
        # para cada categoria, obtenemos sus preguntas y las recorremos
        for p in c.preguntas:
            print(p.id, p.text)


    cat = Categoria.query.get(1)
    print(cat)


    if not User.query.filter(User.email == 'gsignorele@antel.com.uy').first():
        user = User(name="Gustavo",  email="gsignorele@antel.com.uy")
        user.set_password("blabla")
        db.session.add(user)
        db.session.commit()

    # Create 'admin@example.com' user with 'Admin' and 'Agent' roles
    if not User.query.filter(User.email == 'signorele@gmail.com').first():
        user = User(name="Admin",  email="signorele@gmail.com", is_admin=True)
        user.set_password("blabla")
        user.roles.append(Role(name='Admin'))
        user.roles.append(Role(name='Agent'))
        db.session.add(user)
        db.session.commit()
