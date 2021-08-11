from stepik_delivery import app
from flask import render_template


@app.route('/')
def render_main():
    print(app.config)
    return render_template('market/templates/main.html')


@app.route('/admin/')
def render_admin():
    pass
