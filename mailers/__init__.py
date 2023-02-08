from flask_mail import Mail


def mail_config(app):
    app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 2525
    app.config['MAIL_USERNAME'] = 'c0ee358a5dc309'
    app.config['MAIL_PASSWORD'] = '64426853e71728'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    return Mail(app)
