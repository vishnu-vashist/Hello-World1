from flask import Blueprint, render_template

bp = Blueprint('account', __name__)


@bp.route('/')
def dashboard():
    return render_template('account/dashboard.html')
