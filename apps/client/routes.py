# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import math

from flask import render_template, redirect, request, url_for
from flask_login import current_user, login_required

from apps import login_manager, db
from apps.client import blueprint
from apps.client.forms import CltInfoForm

from apps.client.models import ClientInfo

@blueprint.route('/cltinfo', methods=['GET'])
@login_required
def cltinfo():
    cltInfos = ClientInfo.query.all()
    dict = {'content': cltInfos}
    return render_template('client/cltinfo.html', form=dict)

@blueprint.route('/cltinfoedit', methods=['GET', 'POST'])
@login_required
def cltinfoedit():
    cltinfo_form = CltInfoForm(request.form)
    if 'add_cltinfo' in request.form:
        company = request.form['company']
        # Check ClientInfo exists
        cltInfo = ClientInfo.query.filter_by(company=company).first()
        if cltInfo:
            return render_template('client/cltinfoedit.html',
                                   msg='客户信息重复',
                                   success=False,
                                   form=cltinfo_form)
        cltInfo = ClientInfo(**request.form)
        cltInfo.charge = current_user.username
        db.session.add(cltInfo)
        db.session.commit()
        return render_template('client/cltinfoedit.html', msg='插入成功', form=CltInfoForm(), current_user=current_user)


    return render_template('client/cltinfoedit.html', form=CltInfoForm(), current_user=current_user)



# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500