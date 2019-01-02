from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required

from flaskr.db import (
    get_posts_all, add_post, get_post_by_id, update_post, delete_post
)

from flaskr.auth import login_required

# url prefix not passed, because routing for this views set up in flaskr app
bp = Blueprint('blog', __name__)


@bp.route("/")
def index():
    return render_template("blog/index.html", posts=get_posts_all())


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]

        error = None

        if not title:
            error = "Title required"
        elif not body:
            error = "post body required"

        if error is None:
            add_post(g.user["id"], title, body)
            return redirect(url_for("blog.index"))


        flash(error)

    return render_template("blog/create.html")


@bp.route("/update/<int:id>", methods=("GET", "POST"))
@login_required
def update(id):
    post = get_post_by_id(id)

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if request.method == "POST":

        if post["author_id"] != g.user["id"]:
            abort(403, "Forbidden")

        title = request.form["title"]
        body = request.form["body"]

        error = None

        if not title:
            error = "Title required"
        elif not body:
            error = "Post body required"

        if error is not None:
            flash(error)
        else:
            update_post(id, title, body)
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/delete/<int:id>", methods=("POST",))
@login_required
def delete(id):
    post = get_post_by_id(id)

    if post is None:
        abort(404, "post not found!")

    if post["author_id"] != g.user["id"]:
        abort(403, "Forbidden")

    delete_post(id)
    return redirect(url_for("blog.index"))





