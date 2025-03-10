import json
import click
from app import db
from app.models import User, Post, Control

@click.command("export-data")
def export_data():
    """Export current database data to a JSON file."""
    data = {
        "users": [],
        "posts": [],
        "controls": []
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
            "name": control.name,
            "created": control.created.isoformat(),
            "updated": control.updated.isoformat(),
            "archived": control.archived.isoformat() if control.archived else None
        })

    # Write data to JSON file
    with open('sample_data.json', 'w') as f:
        json.dump(data, f, indent=4)

    click.echo('Data exported successfully.')

@click.command("import-sample-data")
def import_sample_data():
    """Import sample data from a JSON file into the database."""
    with open('sample_data.json') as f:
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

    # Create controls
    for control_data in data['controls']:
        control = Control(
            name=control_data['name'],
            created=control_data['created'],
            updated=control_data['updated'],
            archived=control_data['archived']
        )
        db.session.add(control)

    db.session.commit()
    click.echo('Sample data imported successfully.')

def register_commands(app):
    app.cli.add_command(export_data)
    app.cli.add_command(import_sample_data)