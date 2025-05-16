from Hunt4TheMurderer import create_app, db
from Hunt4TheMurderer.models import User
from flask_bcrypt import generate_password_hash

def create_admin():
    app, _ = create_app()
    with app.app_context():
        # Ensure database tables exist
        db.create_all()
        
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            # Create new admin user
            admin_user = User(
                username='admin',
                password=generate_password_hash('admin123'),
                admin=True,
                is_active=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print('Admin user created with password: admin123')
        else:
            # Update existing admin password
            admin_user.password = generate_password_hash('admin123')
            db.session.commit()
            print('Admin password updated to: admin123')

if __name__ == '__main__':
    create_admin()