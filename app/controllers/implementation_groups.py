from flask import render_template, request, redirect, url_for, Blueprint
from app import db
from app.models.implementation_groups import ImplementationGroup
from app.models.control_frameworks import ControlFramework

# Create a Blueprint for implementation groups
implementation_groups_bp = Blueprint('implementation_groups', __name__)

# Route for displaying all implementation groups
@implementation_groups_bp.route('/implementation_groups')
def list():
    all_implementation_groups = ImplementationGroup.query.all()
    return render_template('implementation_groups/list.html', implementation_groups=all_implementation_groups)

# Route for adding a new implementation group
@implementation_groups_bp.route('/implementation_groups/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        description = request.form['description']
        framework_id = request.form['framework_id']
        new_implementation_group = ImplementationGroup(name=name, number=number, description=description, framework_id=framework_id)
        db.session.add(new_implementation_group)
        db.session.commit()
        return redirect(url_for('implementation_groups.list'))  # Redirecting to the list of implementation groups

    frameworks = ControlFramework.query.all()
    return render_template('implementation_groups/create.html', frameworks=frameworks)

# Route for editing an existing implementation group
@implementation_groups_bp.route('/implementation_groups/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    implementation_group = ImplementationGroup.query.get_or_404(id)

    if request.method == 'POST':
        implementation_group.name = request.form['name']
        implementation_group.number = request.form['number']
        implementation_group.description = request.form['description']
        implementation_group.framework_id = request.form['framework_id']
        db.session.commit()
        return redirect(url_for('implementation_groups.list'))  # Redirecting to the list of implementation groups

    frameworks = ControlFramework.query.all()
    return render_template('implementation_groups/edit.html', implementation_group=implementation_group, frameworks=frameworks)

# Route for deleting an implementation group
@implementation_groups_bp.route('/implementation_groups/delete/<int:id>', methods=['POST'])
def delete(id):
    implementation_group = ImplementationGroup.query.get_or_404(id)
    db.session.delete(implementation_group)
    db.session.commit()
    return redirect(url_for('implementation_groups.list'))  # Redirecting to the list of implementation groups