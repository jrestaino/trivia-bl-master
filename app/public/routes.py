# app/public/routes.py

from app import login_required
from flask import render_template, session
from . import public_bp
from .models import Categoria, Pregunta, Respuesta
import random
import datetime

@public_bp.route('/trivia')
def index_trivia():
    return render_template('trivia.html')



@public_bp.route('/trivia/categorias', methods=['GET'])
@login_required
def mostrar_categorias():
    categorias = Categoria.query.all()
    # se agrega codigo para registrar las sesiones utilizando sesiones
    if "tiempo_inicio" not in session.keys():
        session['tiempo_inicio'] = datetime.datetime.now()
        #session['categorias_faltantes'] = categorias
        for c in categorias:
            session[str(c.id)] = False

    '''
    mostrarCategorias = []
    for c in categorias:
        if not session[str(c.id)]:
            mostrarCategorias.append(c)
    '''
    #return render_template('categorias.html', categorias=categorias)
    return render_template('categorias.html', categorias=categorias)


@public_bp.route('/trivia/<id_categoria>/pregunta', methods=['GET'])
@login_required
def mostrar_pregunta(id_categoria):
    if session[str(id_categoria)]:
        categ = Categoria.query.get(id_categoria)
        return render_template('categoria_respondida.html', categoria=categ)
    else:
        preguntas = Pregunta.query.filter_by(categoria_id=id_categoria).all()
        # elegir pregunta aleatoria pero de la categoria adecuada
        pregunta = random.choice(preguntas)
        categ = Categoria.query.get(id_categoria)
        respuestas_posibles = pregunta.respuestas
        return render_template('preguntas.html', categoria=categ, pregunta=pregunta, respuestas_posibles=respuestas_posibles)


@public_bp.route('/trivia/<int:id_categoria>/<int:pregunta_id>/respuesta/<int:id_respuesta>', methods=['GET'])
@login_required
def evaluar_respuesta(id_categoria, pregunta_id, id_respuesta):
    r = Respuesta.query.get(id_respuesta)
    msg = "Respuesta erronea"
    if r.pregunta_id == pregunta_id and r.correcta:
        msg = "Respuesta existosa"
        session[str(id_categoria)] = True

        termina_juego = True
        categs = Categoria.query.all()
        for c in categs:
            if session[str(c.id)] == False:
                # me voy del ciclo porque ya se que falta satisfacer alguna categoria.
                termina_juego = False
                break

        if termina_juego:
            tiempoSegundos = datetime.datetime.now() - session['tiempo_inicio']
            #tiempoSegundos.total_seconds()
            #tiempo_total = str(datetime.datetime.now() - session['tiempo_inicio'])
            tiempo_total = str(tiempoSegundos.seconds)

            session.clear()
            return render_template('ganador.html', tiempo_total = tiempo_total)


    return render_template('respuestas.html', message=msg)







