# -*- coding: utf-8 -*-
__author__ = "María Andrea Vignau (mavignau@gmail.com)"
__copyright__ = "(C) 2016 María Andrea Vignau. GNU GPL 3."


linked_tables = ['movimiento', 'agenda', 'parte']


@auth.requires_login()
def index():
    'muestra la grilla y permite la edición de los datos de los expedientes'

    # para que no aparezca visible el expediente al editarse datos relacionados
    db.movimiento.expediente_id.readable = db.movimiento.expediente_id.writable = False
    db.parte.expediente_id.readable = db.parte.expediente_id.writable = False
    db.agenda.expediente_id.readable = db.agenda.expediente_id.writable = False

    maxtextlengths = {'db.expediente.numero': 15,
                      'db.expediente.caratula': 60,
                      'db.expediente.juzgado_id': 45,
                      'db.movimiento.titulo': 40,
                      'db.movimiento.texto': 40,
                      'db.movimiento.estado': 5,
                      'db.agenda.vencimiento': 15,
                      'db.agenda.titulo': 60,
                      'db.parte.persona_id': 40,
                      'db.parte.caracter': 30}
    grid = SQLFORM.smartgrid(
        db.expediente,
        fields=[
            db.expediente.numero,
            db.expediente.caratula,
            db.expediente.juzgado_id,
            db.movimiento.estado,
            db.movimiento.titulo,
            db.movimiento.texto,
            db.agenda.estado,
            db.agenda.prioridad,
            db.agenda.vencimiento,
            db.agenda.titulo,
            db.parte.persona_id,
            db.parte.caracter,
            db.movimiento.expediente_id,
            db.parte.expediente_id,
            db.agenda.expediente_id,
            db.movimiento.id,
            db.parte.id,
            db.agenda.id,
        ],
        constraints={
            'expediente': (
                db.expediente.created_by == auth.user.id)},
        linked_tables=linked_tables,
        buttons_placement='right',
        exportclasses=myexport,
        advanced_search=False,
        maxtextlength=100,
        orderby={
            'expediente': db.expediente.numero,
            'movimiento': db.movimiento.id,
            'parte': db.parte.persona_id,
            'agenda': ~db.agenda.vencimiento},
        maxtextlengths=maxtextlengths)
    return locals()


def vista_expediente():
    'muestra un panel a la izquierda que tiene los datos del expediente y permite navegar en él'
    expte = SQLFORM(db.expediente,
                    int(request.args[0]),
                    formstyle='bootstrap',
                    readonly=True)

    url = URL(
        'index',
        args=[
            'expediente',
            'edit',
            'expediente',
            request.args[0]],
        user_signature=True)
    links = [A('Expediente', _href=url, _type='button',
               _class='btn btn-default')]
    for k in linked_tables:
        args = ['expediente', '%s.expediente_id' % k, request.args[0]]
        url = URL('index', args=args, user_signature=True)
        text = SPAN(k.capitalize() + 's', _class='buttontext button')
        links.append(A(text, _href=url, _type='button',
                       _class='btn btn-default'))

    return dict(links=links, expte=expte)
