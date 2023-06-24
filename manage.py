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

deploy()