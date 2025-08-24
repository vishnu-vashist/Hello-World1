import os
from app import create_app, db
from app.models.product import Product, ProductImage, ProductVariant


def main():
	app = create_app()
	with app.app_context():
		db.create_all()
		if Product.query.count() == 0:
			p1 = Product(title="Cotton Dress Material", description="Soft cotton dress material.", price_cents=129900, sku="COT-001", category="dress")
			p2 = Product(title="Silk Dress Material", description="Premium silk dress material.", price_cents=249900, sku="SLK-001", category="dress")
			p3 = Product(title="Festive Gift Hamper", description="Curated festive gift hamper.", price_cents=199900, sku="HMP-001", category="hamper")

			db.session.add_all([p1, p2, p3])
			db.session.flush()

			imgs = [
				ProductImage(product_id=p1.id, url="/static/img/sample1.svg", position=0),
				ProductImage(product_id=p1.id, url="/static/img/sample1b.svg", position=1),
				ProductImage(product_id=p2.id, url="/static/img/sample2.svg", position=0),
				ProductImage(product_id=p3.id, url="/static/img/sample3.svg", position=0),
			]
			vars = [
				ProductVariant(product_id=p1.id, color="red", size="2.5m", fabric="cotton", stock=10),
				ProductVariant(product_id=p1.id, color="blue", size="2.5m", fabric="cotton", stock=5),
				ProductVariant(product_id=p2.id, color="green", size="2.5m", fabric="silk", stock=8),
			]
			db.session.add_all(imgs + vars)
			db.session.commit()
			for product in Product.query.all():
				product.ensure_slug()
			db.session.commit()
			print("Seeded sample data.")
		else:
			print("Data already present, skipping.")


if __name__ == "__main__":
	main()