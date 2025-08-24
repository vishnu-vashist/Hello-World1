from flask import Blueprint, render_template, request
from .. import db
from ..models.product import Product, ProductImage, ProductVariant

bp = Blueprint('storefront', __name__)


@bp.route('/')
def index():
	query = Product.query
	color = request.args.get('color')
	design = request.args.get('design')
	if color:
		query = query.join(ProductVariant).filter(ProductVariant.color == color)
	# 'design' could map to category or description keyword for demo
	if design:
		query = query.filter(Product.description.ilike(f"%{design}%"))
	products = query.limit(30).all()
	cards = []
	for p in products:
		img = next((i.url for i in sorted(p.images, key=lambda x: x.position)), None) or '/static/img/sample1.svg'
		cards.append({
			'id': p.id,
			'name': p.title,
			'price': int(p.price_cents/100),
			'image': img,
		})
	return render_template('index.html', products=cards)


@bp.route('/product/<int:product_id>')
def product_detail(product_id):
	p = Product.query.get_or_404(product_id)
	images = [i.url for i in sorted(p.images, key=lambda x: x.position)] or ['/static/img/sample1.svg']
	related = Product.query.filter(Product.category == p.category, Product.id != p.id).limit(4).all()
	related_cards = [{
		'id': r.id,
		'name': r.title,
		'price': int(r.price_cents/100),
		'image': (r.images[0].url if r.images else '/static/img/sample2.svg')
	} for r in related]
	product = {
		'id': p.id,
		'name': p.title,
		'price': int(p.price_cents/100),
		'images': images,
		'variants': [{
			'color': v.color,
			'size': v.size,
			'fabric': v.fabric
		} for v in p.variants]
	}
	return render_template('product_detail.html', product=product, related=related_cards)
