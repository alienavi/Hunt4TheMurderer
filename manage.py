def deploy():
    from Hunt4TheMurderer import create_app,db
    from flask_migrate import upgrade,migrate,init,stamp
    from Hunt4TheMurderer.models import User
    from create_admin import create_admin

    app,_ = create_app()
    app.app_context().push()
    db.create_all()

    init()
    stamp()
    migrate()
    upgrade()
    create_admin()

deploy()