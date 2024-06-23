from app import create_app, socketio

# create flask app
app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)
