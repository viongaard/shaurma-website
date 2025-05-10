from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
from .data import menu

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """
    Главная страница с меню.

    Returns:
        rendered_template: HTML-страница с меню
    """
    return render_template('index.html', menu=menu)


@main.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    """
    Добавляет товар в корзину через POST-запрос.

    Получает item_id из формы и сохраняет в сессии.
    Сессия автоматически создается при первом добавлении.

    Returns:
        redirect: Перенаправление на главную страницу
    """
    item_id = request.form.get('item_id')
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(item_id)
    session.modified = True
    return redirect(url_for('main.index'))


@main.route('/cart')
def cart():
    """
    Отображает содержимое корзины с расчетом суммы.

    Формирует список товаров и их общую стоимость на основе:
        - Данных из сессии (ID товаров)
        - Актуальных цен из menu.json

    Returns:
        rendered_template: HTML-страница cart.html с параметрами:
            - cart_items (list): Список словарей с товарами
            - total_price (int): Общая сумма заказа
        """
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
    """
    Оформляет заказ и очищает корзину.

    Проверяет наличие товаров в корзине. Если корзина пуста -
    перенаправляет на главную страницу.

    Returns:
        rendered_template: HTML-страница order.html с параметром:
            - ready_time (str): Время готовности заказа (текущее время + 30 минут)

        OR

        redirect: Перенаправление на главную страницу при пустой корзине
    """
    if 'cart' not in session or not session['cart']:
        return redirect(url_for('main.index'))

    session.pop('cart', None)
    ready_time = datetime.now() + timedelta(minutes=30)
    return render_template('order.html', ready_time=ready_time.strftime('%H:%M'))
