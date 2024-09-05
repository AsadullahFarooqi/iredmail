# cli.py
import click
from models import db, Mailbox, Forwarding, Domain
from flask import Flask
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

@click.group()
def cli():
    pass

@cli.group()
def mailbox():
    pass

@mailbox.command()
@click.argument('email')
@click.argument('password')
def add(email, password):
    with app.app_context():
        mailbox = Mailbox(email=email, password=password)
        db.session.add(mailbox)
        db.session.commit()
        click.echo(f'Mailbox {email} added.')

@mailbox.command()
@click.argument('email')
def delete(email):
    try:
        with app.app_context():
            mailbox = Mailbox.query.filter_by(email=email).first()
            if mailbox:
                db.session.delete(mailbox)
                db.session.commit()
                click.echo(f'Mailbox {email} deleted.')
            else:
                click.echo(f'Mailbox {email} not found.')
    except Exception as e:
        logger.error(f'Error deleting mailbox {email}: {e}')
        click.echo(f'Error deleting mailbox {email}')

@mailbox.command()
@click.argument('email')
def info(email):
    with app.app_context():
        mailbox = Mailbox.query.filter_by(email=email).first()
        if mailbox:
            click.echo(f'Mailbox {email}: {mailbox}')
        else:
            click.echo(f'Mailbox {email} not found.')

@mailbox.command()
def list():
    with app.app_context():
        mailboxes = Mailbox.query.all()
        for mailbox in mailboxes:
            click.echo(mailbox.email)

# Similar structure for forwarding and domain management


@mailbox.command()
@click.argument('email')
@click.argument('new_password')
def update(email, new_password):
    with app.app_context():
        mailbox = Mailbox.query.filter_by(email=email).first()
        if mailbox:
            mailbox.password = new_password
            db.session.commit()
            click.echo(f'Mailbox {email} updated.')
        else:
            click.echo(f'Mailbox {email} not found.')

@domain.command()
@click.argument('alias_domain')
@click.argument('domain')
def add_alias(alias_domain, domain):
    with app.app_context():
        domain_alias = DomainAlias(alias_domain=alias_domain, domain=domain)
        db.session.add(domain_alias)
        db.session.commit()
        click.echo(f'Domain alias {alias_domain} for {domain} added.')

@domain.command()
@click.argument('alias_domain')
def delete_alias(alias_domain):
    with app.app_context():
        domain_alias = DomainAlias.query.filter_by(alias_domain=alias_domain).first()
        if domain_alias:
            db.session.delete(domain_alias)
            db.session.commit()
            click.echo(f'Domain alias {alias_domain} deleted.')
        else:
            click.echo(f'Domain alias {alias_domain} not found.')

@alias.command()
@click.argument('alias_email')
def add(alias_email):
    with app.app_context():
        alias = Alias(email=alias_email)
        db.session.add(alias)
        db.session.commit()
        click.echo(f'Alias {alias_email} added.')

@alias.command()
@click.argument('alias_email')
def delete(alias_email):
    with app.app_context():
        alias = Alias.query.filter_by(email=alias_email).first()
        if alias:
            db.session.delete(alias)
            db.session.commit()
            click.echo(f'Alias {alias_email} deleted.')
        else:
            click.echo(f'Alias {alias_email} not found.')


@cli.command()
def version():
    click.echo('iRedMail CLI version 1.0.0')


if __name__ == '__main__':
    cli()