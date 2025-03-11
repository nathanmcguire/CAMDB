# app/controllers/safeguards.py
from flask import render_template, request, redirect, url_for, Blueprint
from app import db
from app.models.safeguards import Safeguard
from app.models.security_functions import SecurityFunction
from app.models.controls import Control
from app.models.asset_types import AssetType
from app.models.implementation_groups import ImplementationGroup
from app.models.control_frameworks import ControlFramework

# Create a Blueprint for safeguards
safeguards_bp = Blueprint('safeguards', __name__)

# Route for displaying all safeguards
@safeguards_bp.route('/safeguards')
def list():
    all_safeguards = Safeguard.query.all()
    return render_template('safeguards/list.html', safeguards=all_safeguards)

# Route for adding a new safeguard
@safeguards_bp.route('/safeguards/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        number = request.form['number']
        safeguard_name = request.form['name']
        control_id = request.form['control_id']
        security_function_id = request.form['security_function_id']
        asset_type_id = request.form['asset_type_id']
        implementation_group_id = request.form['implementation_group_id']
        description = request.form.get('description')
        if not safeguard_name or not control_id:
            controls = Control.query.all()
            security_functions = SecurityFunction.query.all()
            asset_types = AssetType.query.all()
            implementation_groups = ImplementationGroup.query.all()
            return render_template('safeguards/create.html', controls=controls, security_functions=security_functions, asset_types=asset_types, implementation_groups=implementation_groups, error="Safeguard name and control ID are required.")
        new_safeguard = Safeguard(number=number, name=safeguard_name, control_id=control_id, security_function_id=security_function_id, asset_type_id=asset_type_id, implementation_group_id=implementation_group_id, description=description)
        db.session.add(new_safeguard)
        db.session.commit()
        return redirect(url_for('safeguards.list'))  # Redirecting to the list of safeguards

    controls = Control.query.all()
    security_functions = SecurityFunction.query.all()
    asset_types = AssetType.query.all()
    implementation_groups = ImplementationGroup.query.all()
    return render_template('safeguards/create.html', controls=controls, security_functions=security_functions, asset_types=asset_types, implementation_groups=implementation_groups)

# Route for editing an existing safeguard
@safeguards_bp.route('/safeguards/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    safeguard = Safeguard.query.get_or_404(id)

    if request.method == 'POST':
        safeguard.number = request.form['number']
        safeguard.name = request.form['name']
        safeguard.control_id = request.form['control_id']
        safeguard.security_function_id = request.form['security_function_id']
        safeguard.asset_type_id = request.form['asset_type_id']
        safeguard.implementation_group_id = request.form['implementation_group_id']
        safeguard.description = request.form.get('description')
        db.session.commit()
        return redirect(url_for('safeguards.list'))  # Redirecting to the list of safeguards

    controls = Control.query.all()
    security_functions = SecurityFunction.query.all()
    asset_types = AssetType.query.all()
    implementation_groups = ImplementationGroup.query.all()
    return render_template('safeguards/edit.html', safeguard=safeguard, controls=controls, security_functions=security_functions, asset_types=asset_types, implementation_groups=implementation_groups)

# Route for deleting a safeguard
@safeguards_bp.route('/safeguards/delete/<int:id>', methods=['POST'])
def delete(id):
    safeguard = Safeguard.query.get_or_404(id)
    db.session.delete(safeguard)
    db.session.commit()
    return redirect(url_for('safeguards.list'))  # Redirecting to the list of safeguards