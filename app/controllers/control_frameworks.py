# app/controllers/control_frameworks.py
from flask import render_template, request, redirect, url_for, Blueprint
from app import db
from app.models.control_frameworks import ControlFramework

# Create a Blueprint for control frameworks
control_frameworks_bp = Blueprint('control_frameworks', __name__)

# Route for displaying all control frameworks
@control_frameworks_bp.route('/control_frameworks')
def list():
    all_control_frameworks = ControlFramework.query.all()
    return render_template('control_frameworks/list.html', control_frameworks=all_control_frameworks)

# Route for adding a new control framework
@control_frameworks_bp.route('/control_frameworks/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        framework_name = request.form['name']
        description = request.form.get('description')
        if not framework_name:
            return render_template('control_frameworks/create.html', error="Framework name is required.")
        new_framework = ControlFramework(name=framework_name, description=description)
        db.session.add(new_framework)
        db.session.commit()
        return redirect(url_for('control_frameworks.list'))  # Redirecting to the list of control frameworks

    return render_template('control_frameworks/create.html')

# Route for editing an existing control framework
@control_frameworks_bp.route('/control_frameworks/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    control_framework = ControlFramework.query.get_or_404(id)

    if request.method == 'POST':
        control_framework.name = request.form['name']
        control_framework.description = request.form.get('description')
        db.session.commit()
        return redirect(url_for('control_frameworks.list'))  # Redirecting to the list of control frameworks

    return render_template('control_frameworks/edit.html', control_framework=control_framework)

# Route for deleting a control framework
@control_frameworks_bp.route('/control_frameworks/delete/<int:id>', methods=['POST'])
def delete(id):
    control_framework = ControlFramework.query.get_or_404(id)
    db.session.delete(control_framework)
    db.session.commit()
    return redirect(url_for('control_frameworks.list'))  # Redirecting to the list of control frameworks