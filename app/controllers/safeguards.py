# app/controllers/safeguards.py
from flask import render_template, request, redirect, url_for, Blueprint, flash
import csv
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
        framework_id = request.form['framework_id']
        number = request.form['number']
        safeguard_name = request.form['name']
        control_id = request.form['control_id']
        security_function_id = request.form['security_function_id']
        asset_type_id = request.form['asset_type_id']
        implementation_group_id = request.form['implementation_group_id']
        description = request.form.get('description')
        if not safeguard_name or not control_id:
            frameworks = ControlFramework.query.all()
            controls = Control.query.all()
            security_functions = SecurityFunction.query.all()
            asset_types = AssetType.query.all()
            implementation_groups = ImplementationGroup.query.all()
            return render_template('safeguards/create.html', frameworks=frameworks, controls=controls, security_functions=security_functions, asset_types=asset_types, implementation_groups=implementation_groups, error="Safeguard name and control ID are required.")
        new_safeguard = Safeguard(framework_id=framework_id, number=number, name=safeguard_name, control_id=control_id, security_function_id=security_function_id, asset_type_id=asset_type_id, implementation_group_id=implementation_group_id, description=description)
        db.session.add(new_safeguard)
        db.session.commit()
        return redirect(url_for('safeguards.list'))  # Redirecting to the list of safeguards

    frameworks = ControlFramework.query.all()
    controls = Control.query.all()
    security_functions = SecurityFunction.query.all()
    asset_types = AssetType.query.all()
    implementation_groups = ImplementationGroup.query.all()
    return render_template('safeguards/create.html', frameworks=frameworks, controls=controls, security_functions=security_functions, asset_types=asset_types, implementation_groups=implementation_groups)

# Route for editing an existing safeguard
@safeguards_bp.route('/safeguards/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    safeguard = Safeguard.query.get_or_404(id)

    if request.method == 'POST':
        safeguard.framework_id = request.form['framework_id']
        safeguard.number = request.form['number']
        safeguard.name = request.form['name']
        safeguard.control_id = request.form['control_id']
        safeguard.security_function_id = request.form['security_function_id']
        safeguard.asset_type_id = request.form['asset_type_id']
        safeguard.implementation_group_id = request.form['implementation_group_id']
        safeguard.description = request.form.get('description')
        db.session.commit()
        return redirect(url_for('safeguards.list'))  # Redirecting to the list of safeguards

    frameworks = ControlFramework.query.all()
    controls = Control.query.all()
    security_functions = SecurityFunction.query.all()
    asset_types = AssetType.query.all()
    implementation_groups = ImplementationGroup.query.all()
    return render_template('safeguards/edit.html', safeguard=safeguard, frameworks=frameworks, controls=controls, security_functions=security_functions, asset_types=asset_types, implementation_groups=implementation_groups)

# Route for deleting a safeguard
@safeguards_bp.route('/safeguards/delete/<int:id>', methods=['POST'])
def delete(id):
    safeguard = Safeguard.query.get_or_404(id)
    db.session.delete(safeguard)
    db.session.commit()
    return redirect(url_for('safeguards.list'))  # Redirecting to the list of safeguards

# Route for importing safeguards from a CSV file
@safeguards_bp.route('/safeguards/import', methods=['GET', 'POST'])
def import_safeguards():
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            flash('No file selected', 'danger')
            return redirect(request.url)

        csv_file = csv.DictReader(file.stream.read().decode('utf-8').splitlines())
        for row in csv_file:
            framework_number = row['Framework Number']
            control_number = row['Control Number']
            safeguard_number = row['Safeguard Number']
            asset_type_name = row['Asset Type Name']
            security_function_name = row['Security Function Name']
            name = row['Safeguard Name']
            description = row['Description']
            implementation_group_number = row['Implementation Group Number']

            framework = ControlFramework.query.filter_by(number=framework_number).first()
            if not framework:
                flash(f'Framework {framework_number} not found', 'danger')
                continue

            control = Control.query.filter_by(number=control_number, framework_id=framework.id).first()
            if not control:
                flash(f'Control {control_number} not found for framework {framework_number}', 'danger')
                continue

            asset_type = AssetType.query.filter_by(name=asset_type_name).first()
            security_function = SecurityFunction.query.filter_by(name=security_function_name).first()
            implementation_group = ImplementationGroup.query.filter_by(number=implementation_group_number, framework_id=framework.id).first()

            new_safeguard = Safeguard(
                framework_id=framework.id,
                control_id=control.id,
                number=safeguard_number,
                asset_type_id=asset_type.id if asset_type else None,
                security_function_id=security_function.id if security_function else None,
                name=name,
                description=description,
                implementation_group_id=implementation_group.id if implementation_group else None
            )
            db.session.add(new_safeguard)

        db.session.commit()
        flash('Safeguards imported successfully', 'success')
        return redirect(url_for('safeguards.list'))

    return render_template('safeguards/import.html')
