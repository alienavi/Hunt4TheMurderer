from Hunt4TheMurderer import create_app, db
from Hunt4TheMurderer.models import User
from flask_bcrypt import generate_password_hash

def create_admin():
    app, _ = create_app()
    with app.app_context():
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user:
            admin_user.password = generate_password_hash('admin123')
            db.session.commit()
            print('Admin password updated to: admin123')
        else:
            print('Admin user not found.') 

create_admin()