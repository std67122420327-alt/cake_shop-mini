from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from foodapp.extensions import db
from foodapp.models import Food, User, Category
from flask_login import current_user, login_required


food_bp = Blueprint('food', __name__, template_folder='templates')

@food_bp.route('/')
@login_required
def index():
    query = db.select(Food).where(Food.user == current_user)
    foods = db.session.scalars(query).all()
    return render_template('foods/index.html', title='My Foods', foods=foods)

@food_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_food():
    food_categories = db.session.scalars(db.select(Category)).all()
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        img_url = request.form.get('img_url')
        category_ids = request.form.getlist('food_categories')
        user_id = current_user.id

        cats = []
        for cid in category_ids:
            cats.append(db.session.get(Category, int(cid)))

        food = Food(
            name=name,
            price=price,
            description=description,
            img_url=img_url,
            user_id=user_id,
            categories=cats
        )
        db.session.add(food)
        db.session.commit()
        flash(f'เพิ่มเมนูอาหาร {name} เรียบร้อยแล้ว', 'success')
        return redirect(url_for('food.index'))
    
    return render_template('foods/new_food.html', title='เพิ่มเมนูอาหาร', food_categories=food_categories)

@food_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_food(id):
    food = db.session.get(Food, id)
    if not food:
        abort(404)
    if food.user_id != current_user.id:
        abort(403)
    
    food_categories = db.session.scalars(db.select(Category)).all()
    if request.method == 'POST':
        food.name = request.form.get('name')
        food.price = request.form.get('price')
        food.description = request.form.get('description')
        food.img_url = request.form.get('img_url')
        category_ids = request.form.getlist('food_categories')

        cats = []
        for cid in category_ids:
            cats.append(db.session.get(Category, int(cid)))
        food.categories = cats

        db.session.commit()
        flash(f'แก้ไขเมนูอาหาร {food.name} เรียบร้อยแล้ว', 'success')
        return redirect(url_for('food.index'))
    
    return render_template('foods/edit_food.html', title='แก้ไขเมนูอาหาร', food=food, food_categories=food_categories)

@food_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_food(id):
    food = db.session.get(Food, id)
    if not food:
        abort(404)
    if food.user_id != current_user.id:
        abort(403)
    
    food_name = food.name
    db.session.delete(food)
    db.session.commit()
    flash(f'ลบเมนูอาหาร {food_name} เรียบร้อยแล้ว', 'success')
    return redirect(url_for('food.index'))

@food_bp.route('/search')
def search():
    q = request.args.get('q', '')
    foods = []
    if q:
        query = db.select(Food).where(Food.name.ilike(f'%{q}%'))
        foods = db.session.scalars(query).all()
    return render_template('foods/search_results.html', title='ผลการค้นหา', foods=foods, q=q)

@food_bp.route('/search-live')
def search_live():
    q = request.args.get('q', '')
    foods = []
    if q and len(q) >= 1:
        query = db.select(Food).where(Food.name.ilike(f'%{q}%')).limit(5)
        foods = db.session.scalars(query).all()
    return render_template('foods/search_dropdown.html', foods=foods, q=q)