from flask import Blueprint, request, render_template, url_for, session, redirect, flash
from action_db import *

# Створення логічного модулю
product_bp = Blueprint('product', __name__, template_folder='templates')


def is_logged():
    return 'company_name' in session


def current_company():
    name_company = session.get('company_name')
    if not name_company:
        return None
    return get_company_by_name(name_company)


@product_bp.route('/', methods=['GET', 'POST'])
def index():
    if not is_logged():
        return redirect(url_for('auth.login'))

    # отримання компанії, під якою людина залогінилась
    company = current_company()

    if request.method == 'POST':
        name = request.form.get('name').lower()
        price = float(request.form.get('price'))
        category = request.form.get('category').lower()

        if product_exist(name, company.id):
            flash('Такий товар вже є!', category='danger')
        else:
            add_product(name, price, category, company.id)
            flash('Товар додано!', category='success')

        return redirect(url_for('product.index'))

    all_categories = get_all_categories(company.id)

    # фіксуємо обрану категорії
    choice_category = request.args.get('category', 'all')

    if choice_category == 'all':
        filter_products = get_all_products(company.id)
    else:
        filter_products = get_product_by_category(choice_category, company.id)

    # СОРТУВАННЯ
    choice_sort = request.args.get('sort', 'all')

    if choice_sort == 'name_asc':
        filter_products = sorted(filter_products, key=lambda product: product.name)
    elif choice_sort == 'name_desc':
        filter_products = sorted(filter_products, key=lambda product: product.name, reverse=True)
    elif choice_sort == 'price_asc':
        filter_products = sorted(filter_products, key=lambda product: product.price)
    elif choice_sort == 'price_desc':
        filter_products = sorted(filter_products, key=lambda product: product.price, reverse=True)

    return render_template('product/index.html',
                           products=filter_products,
                           categories=all_categories,
                           choice_category=choice_category,
                           choice_sort=choice_sort)


@product_bp.route('/delete/<name>')
def delete(name):
    if not is_logged():
        return redirect(url_for('auth.login'))

    company = current_company()
    delete_product(name, company.id)

    flash(f'Товар {name} - видалено!', category='success')
    return redirect(url_for('product.index'))


@product_bp.route('/edit')
def edit():
    return render_template('product/edit.html')
