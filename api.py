# api.py
from flask import Flask, request, jsonify
from models import db, Mailbox, Forwarding, Domain
import logging
from sqlalchemy import Migrate


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/mailbox', methods=['POST'])
def add_mailbox():
    data = request.json
    mailbox = Mailbox(email=data['email'], password=data['password'])
    db.session.add(mailbox)
    db.session.commit()
    return jsonify({'message': f'Mailbox {data["email"]} added.'}), 201

@app.route('/mailbox/<email>', methods=['DELETE'])
def delete_mailbox(email):
    try:
        mailbox = Mailbox.query.filter_by(email=email).first()
        if mailbox:
            db.session.delete(mailbox)
            db.session.commit()
            return jsonify({'message': f'Mailbox {email} deleted.'}), 200
        else:
            return jsonify({'message': f'Mailbox {email} not found.'}), 404
    except Exception as e:
        logger.error(f'Error deleting mailbox {email}: {e}')
        return jsonify({'message': f'Error deleting mailbox {email}'}), 500


@app.route('/mailbox/<email>', methods=['GET'])
def get_mailbox_info(email):
    mailbox = Mailbox.query.filter_by(email=email).first()
    if mailbox:
        return jsonify({'email': mailbox.email, 'password': mailbox.password}), 200
    else:
        return jsonify({'message': f'Mailbox {email} not found.'}), 404

@app.route('/mailboxes', methods=['GET'])
def list_mailboxes():
    mailboxes = Mailbox.query.all()
    return jsonify([mailbox.email for mailbox in mailboxes]), 200

# Similar structure for forwarding and domain management

@app.route('/mailbox/<email>', methods=['PUT'])
def update_mailbox(email):
    data = request.json
    mailbox = Mailbox.query.filter_by(email=email).first()
    if mailbox:
        mailbox.password = data['new_password']
        db.session.commit()
        return jsonify({'message': f'Mailbox {email} updated.'}), 200
    else:
        return jsonify({'message': f'Mailbox {email} not found.'}), 404

@app.route('/domain/alias', methods=['POST'])
def add_domain_alias():
    data = request.json
    domain_alias = DomainAlias(alias_domain=data['alias_domain'], domain=data['domain'])
    db.session.add(domain_alias)
    db.session.commit()
    return jsonify({'message': f'Domain alias {data["alias_domain"]} for {data["domain"]} added.'}), 201

@app.route('/domain/alias/<alias_domain>', methods=['DELETE'])
def delete_domain_alias(alias_domain):
    domain_alias = DomainAlias.query.filter_by(alias_domain=alias_domain).first()
    if domain_alias:
        db.session.delete(domain_alias)
        db.session.commit()
        return jsonify({'message': f'Domain alias {alias_domain} deleted.'}), 200
    else:
        return jsonify({'message': f'Domain alias {alias_domain} not found.'}), 404

@app.route('/alias', methods=['POST'])
def add_alias():
    data = request.json
    alias = Alias(email=data['alias_email'])
    db.session.add(alias)
    db.session.commit()
    return jsonify({'message': f'Alias {data["alias_email"]} added.'}), 201

@app.route('/alias/<alias_email>', methods=['DELETE'])
def delete_alias(alias_email):
    alias = Alias.query.filter_by(email=alias_email).first()
    if alias:
        db.session.delete(alias)
        db.session.commit()
        return jsonify({'message': f'Alias {alias_email} deleted.'}), 200
    else:
        return jsonify({'message': f'Alias {alias_email} not found.'}), 404


@app.route('/version', methods=['GET'])
def get_version():
    return jsonify({'version': '1.0.0'}), 200


# api.py
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("secret")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@app.route('/secure-endpoint')
@auth.login_required
def secure_endpoint():
    return jsonify({'message': 'This is a secure endpoint.'}), 200


if __name__ == '__main__':
    app.run()