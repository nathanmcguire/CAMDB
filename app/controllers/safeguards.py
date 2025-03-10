# app/controllers/safeguards.py
from flask import render_template, request, redirect, url_for, Blueprint
from app import db
from app.models.safeguards import Safeguard

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
        safeguard_name = request.form['name']
        control_id = request.form['control_id']
        description = request.form.get('description')
        if not safeguard_name or not control_id:
            return render_template('safeguards/create.html', error="Safeguard name and control ID are required.")
        new_safeguard = Safeguard(name=safeguard_name, control_id=control_id, description=description)
        db.session.add(new_safeguard)
        db.session.commit()
        return redirect(url_for('safeguards.list'))  # Redirecting to the list of safeguards

    return render_template('safeguards/create.html')

# Route for editing an existing safeguard
@safeguards_bp.route('/safeguards/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    safeguard = Safeguard.query.get_or_404(id)

    if request.method == 'POST':
        safeguard.name = request.form['name']
        safeguard.control_id = request.form['control_id']
        safeguard.description = request.form.get('description')
        db.session.commit()
        return redirect(url_for('safeguards.list'))  # Redirecting to the list of safeguards

    return render_template('safeguards/edit.html', safeguard=safeguard)

# Route for deleting a safeguard
@safeguards_bp.route('/safeguards/delete/<int:id>', methods=['POST'])
def delete(id):
    safeguard = Safeguard.query.get_or_404(id)
    db.session.delete(safeguard)
    db.session.commit()
    return redirect(url_for('safeguards.list'))  # Redirecting to the list of safeguards