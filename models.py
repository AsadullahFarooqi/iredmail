from sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Mailbox(db.Model):
    __tablename__ = 'mailbox'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Mailbox {self.email}>'

class Forwarding(db.Model):
    __tablename__ = 'forwarding'
    id = db.Column(db.Integer, primary_key=True)
    source_email = db.Column(db.String(120), nullable=False)
    destination_email = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Forwarding {self.source_email} -> {self.destination_email}>'

class Domain(db.Model):
    __tablename__ = 'domain'
    id = db.Column(db.Integer, primary_key=True)
    domain_name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Domain {self.domain_name}>'