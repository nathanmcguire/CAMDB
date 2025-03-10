from flask import render_template, request, redirect, url_for, Blueprint
from app import db
from app.models.asset_types import AssetType

# Create a Blueprint for asset types
asset_types_bp = Blueprint('asset_types', __name__)

# Route for displaying all asset types
@asset_types_bp.route('/asset_types')
def list():
    all_asset_types = AssetType.query.all()
    return render_template('asset_types/list.html', asset_types=all_asset_types)

# Route for adding a new asset type
@asset_types_bp.route('/asset_types/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description')
        if not name:
            return render_template('asset_types/create.html', error="Asset type name is required.")
        new_asset_type = AssetType(name=name, description=description)
        db.session.add(new_asset_type)
        db.session.commit()
        return redirect(url_for('asset_types.list'))  # Redirecting to the list of asset types

    return render_template('asset_types/create.html')

# Route for editing an existing asset type
@asset_types_bp.route('/asset_types/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    asset_type = AssetType.query.get_or_404(id)

    if request.method == 'POST':
        asset_type.name = request.form['name']
        asset_type.description = request.form.get('description')
        db.session.commit()
        return redirect(url_for('asset_types.list'))  # Redirecting to the list of asset types

    return render_template('asset_types/edit.html', asset_type=asset_type)

# Route for deleting an asset type
@asset_types_bp.route('/asset_types/delete/<int:id>', methods=['POST'])
def delete(id):
    asset_type = AssetType.query.get_or_404(id)
    db.session.delete(asset_type)
    db.session.commit()
    return redirect(url_for('asset_types.list'))  # Redirecting to the list of asset types