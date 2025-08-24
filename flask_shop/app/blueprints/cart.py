from flask import Blueprint, render_template, request, redirect, url_for, session

bp = Blueprint('cart', __name__)


def _get_cart():
    return session.setdefault('cart', {})


def _save_cart(cart):
    session['cart'] = cart
    session.modified = True


@bp.route('/')
def view_cart():
    cart = _get_cart()
    items = []
    total = 0
    for product_id, item in cart.items():
        subtotal = item['price'] * item['qty']
        total += subtotal
        items.append({"id": product_id, **item, "subtotal": subtotal})
    return render_template('cart/view.html', items=items, total=total)


@bp.route('/add', methods=['POST'])
def add_to_cart():
    product_id = str(request.form.get('product_id'))
    name = request.form.get('name')
    price = int(request.form.get('price', 0))
    image = request.form.get('image')
    qty = int(request.form.get('qty', 1))
    cart = _get_cart()
    if product_id in cart:
        cart[product_id]['qty'] += qty
    else:
        cart[product_id] = {"name": name, "price": price, "image": image, "qty": qty}
    _save_cart(cart)
    return redirect(url_for('cart.view_cart'))


@bp.route('/remove/<product_id>', methods=['POST'])
def remove_item(product_id):
    cart = _get_cart()
    cart.pop(str(product_id), None)
    _save_cart(cart)
    return redirect(url_for('cart.view_cart'))


@bp.route('/checkout')
def checkout():
    return render_template('cart/checkout.html')
