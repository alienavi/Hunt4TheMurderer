from Hunt4TheMurderer import create_app

app, socketio = create_app()

if __name__ == "__main__":
    socketio.run(app) 