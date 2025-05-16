from Hunt4TheMurderer import create_app, db
from flask_migrate import upgrade, migrate, init, stamp
from Hunt4TheMurderer.models import User

def deploy():
    app, _ = create_app()
    app.app_context().push()
    
    # Initialize database
    db.create_all()
    
    # Initialize migrations
    try:
        init()
    except:
        pass  # Migrations might already be initialized
    
    try:
        stamp()
    except:
        pass  # Might already be stamped
    
    migrate()
    upgrade()
    
    # Create admin user after database is set up
    from create_admin import create_admin
    create_admin()

if __name__ == '__main__':
    deploy()