from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from action_db import *

product_bp = Blueprint('product', __name__, template_folder='templates')


def is_logged():
    return 'company_name' in session


@product_bp.route('/')
def index():
    if not is_logged():
        return redirect(url_for('auth.login'))

    company = get_company(session['company_name'])
    products = get_products_by_company(company.id)
    return render_template('product/index.html', products=products)


@product_bp.route('/edit/<name>', methods=['GET', 'POST'])
def edit(name):
    if not is_logged():
        return redirect(url_for('auth.login'))

    company = get_company(session['company_name'])
    product = get_product_by_name(name, company.id)
    categories = get_all_categories()

    if request.method == 'POST':
        price = request.form.get('price')
        category_id = request.form.get('category')
        update_product(name, price, category_id, company.id)
        flash('Товар обновлено', category='success')
        return redirect(url_for('product.index'))

    return render_template('product/edit.html', product=product, categories=categories)