from flask import render_template, request, redirect, url_for, Blueprint
from app import db
from app.models.security_functions import SecurityFunction

# Create a Blueprint for security functions
security_functions_bp = Blueprint('security_functions', __name__)

# Route for displaying all security functions
@security_functions_bp.route('/security_functions')
def list():
    all_security_functions = SecurityFunction.query.all()
    return render_template('security_functions/list.html', security_functions=all_security_functions)

# Route for adding a new security function
@security_functions_bp.route('/security_functions/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description')
        if not name:
            return render_template('security_functions/create.html', error="Security function name is required.")
        new_security_function = SecurityFunction(name=name, description=description)
        db.session.add(new_security_function)
        db.session.commit()
        return redirect(url_for('security_functions.list'))  # Redirecting to the list of security functions

    return render_template('security_functions/create.html')

# Route for editing an existing security function
@security_functions_bp.route('/security_functions/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    security_function = SecurityFunction.query.get_or_404(id)

    if request.method == 'POST':
        security_function.name = request.form['name']
        security_function.description = request.form.get('description')
        db.session.commit()
        return redirect(url_for('security_functions.list'))  # Redirecting to the list of security functions

    return render_template('security_functions/edit.html', security_function=security_function)

# Route for deleting a security function
@security_functions_bp.route('/security_functions/delete/<int:id>', methods=['POST'])
def delete(id):
    security_function = SecurityFunction.query.get_or_404(id)
    db.session.delete(security_function)
    db.session.commit()
    return redirect(url_for('security_functions.list'))  # Redirecting to the list of security functions