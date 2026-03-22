from flask import Blueprint, render_template, request, abort
from foodapp.extensions import db
from foodapp.models import Food, Category


core_bp = Blueprint('core', __name__, template_folder='templates')

@core_bp.route('/')
def index():
    page = request.args.get('page',type=int)
    foods = db.paginate(db.select(Food), per_page=4, page=page)
    return render_template('core/index.html', title='Home Page', page=page, foods=foods )

@core_bp.route('/<int:id>/details')
def details(id):
    food = db.session.get(Food, id)
    if not food:
        abort(404)
    return render_template('core/food_detail.html', title='Details Page', food=food)