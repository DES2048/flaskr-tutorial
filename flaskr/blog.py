from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_posts_all

# url prefix not passed, because routing for this views set up in flaskr app
bp = Blueprint('blog', __name__)


@bp.route("/")
def index():
    return render_template("blog/index.html", posts=get_posts_all())

