from flask import render_template, request, redirect, url_for, Blueprint

from app import db
from app.models.controls import Control

# Create a Blueprint for controls
controls_bp = Blueprint('controls', __name__)

# Route for displaying all controls
@controls_bp.route('/controls')
#@login_required
def list():
    all_controls = Control.query.all()
    return render_template('controls/list.html', controls=all_controls)

# Route for adding a new control
@controls_bp.route('/controls/create', methods=['GET', 'POST'])
#@login_required
def create():
    if request.method == 'POST':
        control_name = request.form['name']
        if not control_name:
            return render_template('controls_create.html', error="Control name is required.")
        new_control = Control(name=control_name)
        db.session.add(new_control)
        db.session.commit()
        return redirect(url_for('controls.list'))  # Redirecting to the list of controls

    return render_template('controls/create.html')

# Route for editing an existing control
@controls_bp.route('/controls/edit/<int:id>', methods=['GET', 'POST'])
#@login_required
def edit(id):
    control = Control.query.get_or_404(id)

    if request.method == 'POST':
        control.name = request.form['name']
        db.session.commit()
        return redirect(url_for('controls.list'))  # Redirecting to the list of controls

    return render_template('controls/edit.html', control=control)

# Route for deleting a control
@controls_bp.route('/controls/delete/<int:id>', methods=['GET', 'POST'])
#@login_required
def delete(id):
    control = Control.query.get_or_404(id)
    db.session.delete(control)
    db.session.commit()
    return redirect(url_for('controls.list'))  # Redirecting to the list of controls
