from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
from .data import menu

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html', menu=menu)


@main.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_id = request.form.get('item_id')
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(item_id)
    session.modified = True
    return redirect(url_for('main.index'))


@main.route('/cart')
def cart():
    cart_items = []
    total_price = 0
    if 'cart' in session:
        for item_id in session['cart']:
            item = menu.get(item_id)
            if item:
                cart_items.append(item)
                total_price += item['price']
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


@main.route('/order', methods=['POST'])
def order():
    if 'cart' not in session or not session['cart']:
        return redirect(url_for('main.index'))

    session.pop('cart', None)
    ready_time = datetime.now() + timedelta(minutes=30)
    return render_template('order.html', ready_time=ready_time.strftime('%H:%M'))
