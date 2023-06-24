import sys

command = str(sys.argv[1]).lower()

def deploy():
    from Hunt4TheMurderer import create_app,db
    from flask_migrate import upgrade,migrate,init,stamp
    from Hunt4TheMurderer.models import User

    app,_ = create_app()
    app.app_context().push()
    db.create_all()

    init()
    stamp()
    migrate()
    upgrade()

def update_db():
    from Hunt4TheMurderer import create_app,db
    from flask_migrate import upgrade,migrate,init,stamp
    from Hunt4TheMurderer.models import User

    app,_ = create_app()
    app.app_context().push()
    db.update(update_db)
    
    stamp()
    migrate()
    upgrade()

print(command)
if command == 'upgrade' :
    update_db()
else :
    deploy()