from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from config import create_app, db

app = create_app()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/panel')
@login_required
def panel():
    return render_template('panel/index.html', current_user=current_user)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True,ssl_context=('localhost.crt', 'localhost.key'), port=443)