from flask_mail import Mail


def mail_config(app):
    app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 2525
    app.config['MAIL_USERNAME'] = 'ea5399b563c1b8'
    app.config['MAIL_PASSWORD'] = '2ebfbb95e2e020'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    return Mail(app)
