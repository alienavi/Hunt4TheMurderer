from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import login_required, current_user
from . import login_manager
import json
from random import shuffle

rooms = Blueprint('rooms',__name__)

@rooms.route('/kitchen', methods=['GET', 'POST'])
def kitchen():
    print(request.form)
    if 'countries' in request.form:
        name = request.form.get('countries')
        print(name)
        if(name == 'INDIA'):
            result = 1
        else:
            result = 0
        return jsonify(message=result)
    else:
        return '',400