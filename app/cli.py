import json
import click
from datetime import datetime
from sqlalchemy.inspection import inspect
from werkzeug.security import generate_password_hash
from app import db
from app.models import User, Post, Control, AssetType, Asset, ControlFramework, Safeguard

def serialize_model(model):
    """Serialize a SQLAlchemy model instance into a dictionary."""
    data = {c.key: getattr(model, c.key) for c in inspect(model).mapper.column_attrs}
    if isinstance(model, User):
        data.pop('password_hash', None)  # Exclude password hash
    return data

def deserialize_model(model_class, data):
    """Deserialize a dictionary into a SQLAlchemy model instance."""
    instance = model_class()
    for key, value in data.items():
        if hasattr(instance, key):
            if isinstance(getattr(model_class, key).type, db.DateTime):
                value = datetime.fromisoformat(value) if value else None
            setattr(instance, key, value)
    return instance

@click.command("export-samples")
def export_samples():
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

    # Query and serialize data for each model
    for model_name, model_class in [("users", User), ("posts", Post), ("controls", Control),
                                    ("asset_types", AssetType), ("assets", Asset), 
                                    ("control_frameworks", ControlFramework), ("safeguards", Safeguard)]:
        instances = model_class.query.all()
        data[model_name] = [serialize_model(instance) for instance in instances]

    # Write data to JSON file
    with open('samples.json', 'w') as f:
        json.dump(data, f, indent=4, default=str)

    click.echo('Data exported successfully.')
    click.echo('\033[91mWARNING: Remove sensitive data from samples.json before committing!!!\033[0m')

@click.command("import-samples")
def import_samples():
    """Import sample data from a JSON file into the database."""
    with open('samples.json') as f:
        data = json.load(f)

    # Create or update data for each model
    for model_name, model_class in [("users", User), ("posts", Post), ("controls", Control),
                                    ("asset_types", AssetType), ("assets", Asset), 
                                    ("control_frameworks", ControlFramework), ("safeguards", Safeguard)]:
        for item_data in data[model_name]:
            # Check for existing instance by primary key (id) if available
            instance = model_class.query.filter_by(id=item_data.get('id')).first()
            
            if not instance:
                # If no instance found by id, check by unique constraints
                if model_name == "users":
                    instance = model_class.query.filter_by(username=item_data['username']).first()
                elif model_name == "posts":
                    instance = model_class.query.filter_by(body=item_data['body'], author_id=item_data['author_id']).first()
                elif model_name == "controls":
                    instance = model_class.query.filter_by(name=item_data['name']).first()
                elif model_name == "asset_types":
                    instance = model_class.query.filter_by(name=item_data['name']).first()
                elif model_name == "assets":
                    instance = model_class.query.filter_by(name=item_data['name']).first()
                elif model_name == "control_frameworks":
                    instance = model_class.query.filter_by(name=item_data['name']).first()
                elif model_name == "safeguards":
                    instance = model_class.query.filter_by(name=item_data['name'], control_id=item_data['control_id']).first()

            if instance:
                for key, value in item_data.items():
                    if isinstance(getattr(model_class, key).type, db.DateTime):
                        value = datetime.fromisoformat(value) if value else None
                    setattr(instance, key, value)
            else:
                instance = deserialize_model(model_class, item_data)
                db.session.add(instance)

            # Set every user's password to "password"
            if model_name == "users":
                instance.set_password("password")

    db.session.commit()
    click.echo('Sample data imported successfully.')

def register_commands(app):
    app.cli.add_command(export_samples)
    app.cli.add_command(import_samples)