from flask import render_template, request, jsonify, Response, flash, redirect, url_for, session
from flask_login import login_user, current_user, logout_user, login_required
from . import db, socketio, bcrypt, login_manager
from .models import Parcel, TransactionLog, User
# from .auth import role_required
from flask import current_app as app
from .reports.report import generate_report
from .auth import role_required

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        # email = request.form['email']
        password = request.form['password']
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password, role="ADMIN")
        
        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout the current user."""  
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
# @role_required('admin')
def index():
    print(f"user role: {current_user.role}")
    parcels = Parcel.query.all()
    transactionLogs = TransactionLog.query.all()
    received_parcels = [parcel for parcel in parcels if parcel.status == 'received']
    inTransit_parcels = [parcel for parcel in parcels if parcel.status == 'in_transit']
    delivered_parcels = [parcel for parcel in parcels if parcel.status == 'delivered']
    return render_template('index.html', parcels=parcels, transactionLogs=transactionLogs, username=current_user.username, delivered_parcels=delivered_parcels, received_parcels=received_parcels, inTransit_parcels=inTransit_parcels)

@app.route('/admin-dashboard')
def show_all_parcels():
    parcels = Parcel.query.all()
    return render_template('list-parcels.html', parcels=parcels)

# get all parcesl 
@app.route('/parcels', methods=['GET'])
@login_required
# @role_required('admin')
def get_parcels():
    parcels = Parcel.query.all()
    parcels_data = []
    for parcel in parcels:
        parcel_dict = {
            'id': parcel.id,
            'status': parcel.status,
            'sender': parcel.sender,
            'receiver': parcel.receiver,
            # 'location': parcel.location,
            'timestamp': parcel.created_at
        }
        parcels_data.append(parcel_dict), 200
    return jsonify(parcels_data)

@app.route('/parcels', methods=['GET', 'POST'])
def create_parcel():
    # data = request.get_json()
    if request.method == 'POST':
        sender = request.form['sender']
        receiver = request.form['receiver']
    
    if not sender or not receiver:
        return jsonify({'error': 'Missing data'}), 400
    
    # save new parcel to db
    new_parcel = Parcel(sender=sender, receiver=receiver)
    db.session.add(new_parcel)
    db.session.commit()
    
    # create new transaction_log
    new_log = TransactionLog(parcel_id=new_parcel.id, status='received')
    db.session.add(new_log)
    db.session.commit()
    socketio.emit('create_parcel', {'parcel_id': new_parcel.id, 'sender': new_parcel.sender, 'receiver': new_parcel.receiver, 'status': new_parcel.status})
    
    return redirect(url_for('show_all_parcels'))

@app.route('/parcels/<int:id>', methods=['PUT'])
def update_parcel(id):
    parcel = Parcel.query.get(id)
    if not parcel:
        return jsonify({'error': 'No Parcel Found.'}), 404
    data = request.get_json()
    parcel.status = data['status']
    db.session.commit() 
    new_log = TransactionLog(parcel_id=parcel.id, status=data['status'])
    db.session.add(new_log)
    db.session.commit()
    socketio.emit('parcel_status_updated', {'parcel_id': parcel.id, 'status': parcel.status})
    return jsonify({'message': 'Parcel updated'}), 200

@app.route('/parcels/bulk_process', methods=['POST'])
def bulk_process_parcels():
    parcels = Parcel.query.all()
    for parcel in parcels:
        parcel.status = 'in_transit'  # Simulating processing
        db.session.commit()
        socketio.emit('progress_update', {'parcel_id': parcel.id, 'status': 'processing'})
    return jsonify({'message': 'Bulk processing started'}), 202

@app.route('/report', methods=['GET'])
# @login_required
# @role_required('admin')
def generate_report():
    report_data = generate_report()  # Call the imported function
    return Response(
        report_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=parcel_report.csv"}
    )
