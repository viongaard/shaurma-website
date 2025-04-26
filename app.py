from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Секретный ключ для работы с сессиями

# Меню шаурмы
menu = {
    "shaurma1": {"name": "Шаурма с курицей", "price": 200,
                 "image": "shawarma1.jpg"},
    "shaurma2": {"name": "Шаурма с говядиной", "price": 250,
                 "image": "shawarma2.jpg"},
    "shaurma3": {"name": "Шаурма с овощами", "price": 180,
                 "image": "shawarma3.jpg"},
}


@app.route('/')
def index():
    return render_template('index.html', menu=menu)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_id = request.form.get('item_id')
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(item_id)
    session.modified = True
    return redirect(url_for('index'))


@app.route('/cart')
def cart():
    cart_items = []
    total_price = 0
    if 'cart' in session:
        for item_id in session['cart']:
            item = menu.get(item_id)
            if item:
                cart_items.append(item)
                total_price += item['price']
    return render_template('cart.html', cart_items=cart_items,
                           total_price=total_price)


@app.route('/order', methods=['POST'])
def order():
    if 'cart' not in session or not session['cart']:
        return redirect(url_for('index'))

    # Очищаем корзину после оформления заказа
    session.pop('cart', None)

    # Устанавливаем время готовности заказа (30 минут с текущего момента)
    ready_time = datetime.now() + timedelta(minutes=30)
    return render_template('order.html',
                           ready_time=ready_time.strftime('%H:%M'))


if __name__ == '__main__':
    app.run(debug=True)