from . import socketio

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


# @socketio.on('connect')
# def handle_connect():
#     emit('response', {'data': 'Connected'})

# @socketio.on('process_parcel')
# def handle_process_parcel(data):
#     # Logic to process parcel
#     emit('response', {'data': 'Processing completed'})