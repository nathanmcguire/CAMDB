from app import db
from sqlalchemy import func

class ImplementationGroup(db.Model):
    __tablename__ = 'implementation_groups'  # Explicitly define the table name
    
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), nullable=True)  # Implementation group number as a string
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    framework_id = db.Column(db.Integer, db.ForeignKey('control_frameworks.id'), nullable=False)    
    
    # Use func.now() for both created and updated to automatically set timestamps
    created = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)  # Default func.now()

    # Relationship with control framework
    framework = db.relationship('ControlFramework', backref=db.backref('implementation_groups', lazy=True))
    def __repr__(self):
        return f'<ImplementationGroup {self.name}>'