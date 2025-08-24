from flask import Blueprint, render_template

bp = Blueprint('admin', __name__)


@bp.route('/')
def dashboard():
    metrics = {"sales_today": 0, "orders_pending": 0, "inventory_low": 0}
    return render_template('admin/dashboard.html', metrics=metrics)
