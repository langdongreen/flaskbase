import logging

from flask import render_template,Blueprint

log = logging.getLogger(__name__)

public_blueprint = Blueprint('public', __name__, template_folder='templates')
@public_blueprint.route("/",methods=["GET","POST"])
def index():
     return render_template('page.html',message="index")