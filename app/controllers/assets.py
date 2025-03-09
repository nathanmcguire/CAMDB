# controllers/assets.py
from flask import render_template, request, redirect, url_for, Blueprint, flash
from flask_login import login_required, current_user

from app import db
from app.models.assets import Asset

# Create the Blueprint for assets
assets_bp = Blueprint('assets', __name__)

# Route for displaying all assets in a table
@assets_bp.route('/assets')
#@login_required
def list():
    all_assets = Asset.query.all()
    return render_template('assets/list.html', assets=all_assets)

@assets_bp.route('/assets/<int:id>', methods=['GET'])
def read(id):
    asset = Asset.query.get_or_404(id)
    return render_template('assets/read.html', asset=asset)

# Route for adding a new asset (Create)
@assets_bp.route('/assets/create', methods=['GET', 'POST'])
#@login_required
def create():
    if request.method == 'POST':
        asset_name = request.form['name']
        
        if not asset_name:
            # Handle form validation: asset name is required
            return render_template('assets/create.html', error="Asset name is required.")
        
        new_asset = Asset(name=asset_name)
        db.session.add(new_asset)
        db.session.commit()
        return redirect(url_for('assets.read', id=new_asset.id))

    return render_template('assets/create.html')




# Route for editing an existing asset (Update)
@assets_bp.route('/assets/edit/<int:id>', methods=['GET', 'POST'])
#@login_required
def edit(id):
    asset = Asset.query.get_or_404(id)

    if request.method == 'POST':
        asset.name = request.form['name']
        db.session.commit()
        return redirect(url_for('assets.list'))  # Referencing Blueprint

    return render_template('assets/edit.html', asset=asset)


@assets_bp.route('/assets/archive/<int:id>', methods=['GET'])
def archive(id):
    asset = Asset.query.get_or_404(id)
    asset.status = 'Archived'  # Assuming you have a 'status' field for the asset
    db.session.commit()
    flash('Asset has been archived successfully.', 'success')
    return redirect(url_for('assets.list'))  # Redirect back to the asset list

# Route for deleting an asset (Delete)
@assets_bp.route('/assets/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    asset = Asset.query.get_or_404(id)
    db.session.delete(asset)
    db.session.commit()
    return redirect(url_for('assets.list'))  # Referencing Blueprint

