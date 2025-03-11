from flask import render_template, request, redirect, url_for, Blueprint
from app import db
from app.models.controls import Control
from app.models.control_frameworks import ControlFramework

# Create a Blueprint for controls
controls_bp = Blueprint('controls', __name__)

# Route for displaying all controls
@controls_bp.route('/controls')
def list():
    all_controls = Control.query.all()
    return render_template('controls/list.html', controls=all_controls)

# Route for adding a new control
@controls_bp.route('/controls/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        number = request.form['number']
        control_name = request.form['name']
        description = request.form.get('description')
        framework_id = request.form['framework_id']
        if not control_name:
            frameworks = ControlFramework.query.all()
            return render_template('controls/create.html', frameworks=frameworks, error="Control name is required.")
        new_control = Control(number=number, name=control_name, description=description, framework_id=framework_id)
        db.session.add(new_control)
        db.session.commit()
        return redirect(url_for('controls.list'))  # Redirecting to the list of controls

    frameworks = ControlFramework.query.all()
    return render_template('controls/create.html', frameworks=frameworks)

# Route for editing an existing control
@controls_bp.route('/controls/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    control = Control.query.get_or_404(id)

    if request.method == 'POST':
        control.number = request.form['number']
        control.name = request.form['name']
        control.description = request.form.get('description')
        control.framework_id = request.form['framework_id']
        db.session.commit()
        return redirect(url_for('controls.list'))  # Redirecting to the list of controls

    frameworks = ControlFramework.query.all()
    return render_template('controls/edit.html', control=control, frameworks=frameworks)

# Route for deleting a control
@controls_bp.route('/controls/delete/<int:id>', methods=['POST'])
def delete(id):
    control = Control.query.get_or_404(id)
    db.session.delete(control)
    db.session.commit()
    return redirect(url_for('controls.list'))  # Redirecting to the list of controls
