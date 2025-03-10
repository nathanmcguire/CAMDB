from app import db
from sqlalchemy import func
from app.utils import utc_to_local

class Control(db.Model):
    __tablename__ = 'controls'  # Explicitly define the table name
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    # Use func.now() for both created and updated to automatically set timestamps
    created = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)  # Default func.now()
    archived = db.Column(db.DateTime, nullable=True)  # Nullable, set when the asset is archived (for soft deletes)

    def __repr__(self):
        return f'<Asset {self.name}>'
    
    @property
    def created_local(self):
        return utc_to_local(self.created)
    
    @property
    def updated_local(self):
        return utc_to_local(self.updated)
    
    @property
    def archived_local(self):
        return utc_to_local(self.archived)