from datetime import datetime
from sqlalchemy.orm import relationship
from slugify import slugify
from .. import db


class Product(db.Model):
	__tablename__ = 'products'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	description = db.Column(db.Text)
	price_cents = db.Column(db.Integer, nullable=False, default=0)
	sku = db.Column(db.String(64), unique=True)
	slug = db.Column(db.String(255), unique=True, index=True)
	category = db.Column(db.String(64))
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

	images = relationship('ProductImage', back_populates='product', cascade='all, delete-orphan')
	variants = relationship('ProductVariant', back_populates='product', cascade='all, delete-orphan')

	def ensure_slug(self):
		if not self.slug:
			base = slugify(self.title)
			self.slug = f"{base}-{self.id}" if self.id else base

	@property
	def price(self) -> float:
		return (self.price_cents or 0) / 100.0


class ProductImage(db.Model):
	__tablename__ = 'product_images'
	id = db.Column(db.Integer, primary_key=True)
	product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
	url = db.Column(db.String(512), nullable=False)
	position = db.Column(db.Integer, default=0)

	product = relationship('Product', back_populates='images')


class ProductVariant(db.Model):
	__tablename__ = 'product_variants'
	id = db.Column(db.Integer, primary_key=True)
	product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
	color = db.Column(db.String(32))
	size = db.Column(db.String(32))
	fabric = db.Column(db.String(32))
	stock = db.Column(db.Integer, default=0)

	product = relationship('Product', back_populates='variants')