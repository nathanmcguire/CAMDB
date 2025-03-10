import json
import click
from datetime import datetime
from app import db
from app.models import User, Post, Control, AssetType, Asset, ControlFramework, Safeguard

@click.command("export-data")
def export_data():
    """Export current database data to a JSON file."""
    data = {
        "users": [],
        "posts": [],
        "controls": [],
        "asset_types": [],
        "assets": [],
        "control_frameworks": [],
        "safeguards": []
    }

    # Query users and add to data
    users = User.query.all()
    for user in users:
        data["users"].append({
            "username": user.username,
            "email": user.email,
            "password": user.password_hash  # Note: This is the hashed password
        })

    # Query posts and add to data
    posts = Post.query.all()
    for post in posts:
        data["posts"].append({
            "body": post.body,
            "username": post.author.username
        })

    # Query controls and add to data
    controls = Control.query.all()
    for control in controls:
        data["controls"].append({
            "number": control.number,
            "name": control.name,
            "description": control.description,
            "framework_id": control.framework_id,
            "created": control.created.isoformat(),
            "updated": control.updated.isoformat(),
            "archived": control.archived.isoformat() if control.archived else None
        })

    # Query asset types and add to data
    asset_types = AssetType.query.all()
    for asset_type in asset_types:
        data["asset_types"].append({
            "name": asset_type.name,
            "description": asset_type.description,
            "created": asset_type.created.isoformat(),
            "updated": asset_type.updated.isoformat()
        })

    # Query assets and add to data
    assets = Asset.query.all()
    for asset in assets:
        data["assets"].append({
            "name": asset.name,
            "description": asset.description,
            "asset_type_id": asset.asset_type_id,
            "created": asset.created.isoformat(),
            "updated": asset.updated.isoformat(),
            "archived": asset.archived.isoformat() if asset.archived else None
        })

    # Query control frameworks and add to data
    control_frameworks = ControlFramework.query.all()
    for framework in control_frameworks:
        data["control_frameworks"].append({
            "name": framework.name,
            "description": framework.description,
            "created": framework.created.isoformat(),
            "updated": framework.updated.isoformat()
        })

    # Query safeguards and add to data
    safeguards = Safeguard.query.all()
    for safeguard in safeguards:
        data["safeguards"].append({
            "name": safeguard.name,
            "description": safeguard.description,
            "control_id": safeguard.control_id,
            "created": safeguard.created.isoformat(),
            "updated": safeguard.updated.isoformat(),
            "archived": safeguard.archived.isoformat() if safeguard.archived else None
        })

    # Write data to JSON file
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

    click.echo('Data exported successfully.')

@click.command("import-data")
def import_data():
    """Import sample data from a JSON file into the database."""
    with open('data.json') as f:
        data = json.load(f)

    # Create users
    users = {}
    for user_data in data['users']:
        user = User(username=user_data['username'], email=user_data['email'])
        user.password_hash = user_data['password']
        db.session.add(user)
        users[user.username] = user

    # Create posts
    for post_data in data['posts']:
        user = users.get(post_data['username'])
        if user:
            post = Post(body=post_data['body'], author=user)
            db.session.add(post)

    # Create control frameworks
    frameworks = {}
    for framework_data in data['control_frameworks']:
        framework = ControlFramework(
            name=framework_data['name'],
            description=framework_data['description'],
            created=datetime.fromisoformat(framework_data['created']),
            updated=datetime.fromisoformat(framework_data['updated'])
        )
        db.session.add(framework)
        frameworks[framework.name] = framework

    # Create controls
    for control_data in data['controls']:
        control = Control(
            number=control_data['number'],
            name=control_data['name'],
            description=control_data['description'],
            framework_id=control_data['framework_id'],
            created=datetime.fromisoformat(control_data['created']),
            updated=datetime.fromisoformat(control_data['updated']),
            archived=datetime.fromisoformat(control_data['archived']) if control_data['archived'] else None
        )
        db.session.add(control)

    # Create asset types
    asset_types = {}
    for asset_type_data in data['asset_types']:
        asset_type = AssetType(
            name=asset_type_data['name'],
            description=asset_type_data['description'],
            created=datetime.fromisoformat(asset_type_data['created']),
            updated=datetime.fromisoformat(asset_type_data['updated'])
        )
        db.session.add(asset_type)
        asset_types[asset_type.name] = asset_type

    # Create assets
    for asset_data in data['assets']:
        asset = Asset(
            name=asset_data['name'],
            description=asset_data['description'],
            asset_type_id=asset_data['asset_type_id'],
            created=datetime.fromisoformat(asset_data['created']),
            updated=datetime.fromisoformat(asset_data['updated']),
            archived=datetime.fromisoformat(asset_data['archived']) if asset_data['archived'] else None
        )
        db.session.add(asset)

    # Create safeguards
    for safeguard_data in data['safeguards']:
        safeguard = Safeguard(
            name=safeguard_data['name'],
            description=safeguard_data['description'],
            control_id=safeguard_data['control_id'],
            created=datetime.fromisoformat(safeguard_data['created']),
            updated=datetime.fromisoformat(safeguard_data['updated']),
            archived=datetime.fromisoformat(safeguard_data['archived']) if safeguard_data['archived'] else None
        )
        db.session.add(safeguard)

    db.session.commit()
    click.echo('Sample data imported successfully.')

def register_commands(app):
    app.cli.add_command(export_data)
    app.cli.add_command(import_data)