import jinja2
import flask
import random

filters = flask.Blueprint('filters',__name__)

@jinja2.pass_context
@filters.app_template_filter()
def filter_shuffle(context, seq):
    try:
        result = list(seq)
        random.shuffle(result)
        #print(result)
        return result
    except:
        return seq
