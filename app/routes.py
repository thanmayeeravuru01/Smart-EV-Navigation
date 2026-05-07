print("ROUTES.PY LOADED — available_start_times SHOULD EXIST")
from flask import get_flashed_messages
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, User, EVVehicle, ContactUs, Feedback, ChargingStation, Booking, Slot
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from flask import jsonify, request
import math
import matplotlib.pyplot as plt
import io
import base64
from app.utils.email import send_email

from datetime import datetime, timedelta
bp = Blueprint('main', __name__)
API_KEY = 'pk.218199c167e2d299d7a2ac441eac33b2'
import requests

def get_coordinates_from_location(location):
    api_key = 'pk.218199c167e2d299d7a2ac441eac33b2'  # Replace with your actual LocationIQ API key
    url = f'https://us1.locationiq.com/v1/search.php?key={api_key}&q={location}&format=json'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data:
            latitude = float(data[0]['lat'])
            longitude = float(data[0]['lon'])
            print(f"User location: {latitude}, {longitude}")  # Debugging the user's coordinates
            return latitude, longitude
    # Debugging: If the coordinates aren't fetched properly, log it.
    print(f"Failed to fetch coordinates for location: {location}")
    return None, None  # Return None if location is not found

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/home')
def home():
    return render_template('home.html')

# Profile Page (Requires User to Be Logged In)
@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('Please log in to view your profile.', 'danger')
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        # Update profile details
        user.name = request.form['name']
        user.email = request.form['email']
        user.phone = request.form['phone']
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('profile.html', user=user)

# Change Password (Requires User to Be Logged In)
@bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        
        # Check if the current password is correct
        if not check_password_hash(user.password, current_password):
            return "Incorrect password", 400
        
        user.password = generate_password_hash(new_password)
        
        db.session.commit()
        flash('Password changed successfully!', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('change_password.html')

# User Dashboard (Requires User to Be Logged In)
@bp.route('/user_dashboard')
def user_dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'danger')
        return redirect(url_for('main.login'))

    user = User.query.get(session['user_id'])
    return render_template('user_dashboard.html', user=user)

# Login Route
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Find user by email
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # Login success
            session['user_id'] = user.user_id
            session['user_name'] = user.name
            flash('Login successful!', 'auth')
            return redirect(url_for('main.user_dashboard'))
        else:
            flash('Invalid email or password!', 'auth')
            return redirect(url_for('main.login'))
    
    return render_template('login.html')

# Logout Route
@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.home'))

# Registration Route
@bp.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        name = request.form['fullname']
        email = request.form['email']
        phone = request.form['Phone Number']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate passwords
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('main.register_user'))

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already registered!', 'danger')
            return redirect(url_for('main.register_user'))

        # Save user to database
        hashed_password = generate_password_hash(password)
        user = User(name=name, email=email, password=hashed_password, phone=phone)
        db.session.add(user)
        db.session.commit()

        flash('Signup successful! Please login.', 'success')
        return redirect(url_for('main.login'))

    
    return render_template('home.html')

# Forgot Password Route
@bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if user:
            from app.utils.security import generate_reset_token
            token = generate_reset_token(user.email)

            reset_link = url_for(
                'main.reset_password',
                token=token,
                _external=True
            )

            send_email(
                to=user.email,
                subject="🔐 Reset Your ChargeMate Password",
                body=render_template(
                    'emails/reset_password.html',
                    user=user,
                    reset_link=reset_link
                )
            )

        flash(
            "If the email exists, a password reset link has been sent.",
            "auth"
        )
        return redirect(url_for('main.login'))

    return render_template('forgot_password.html')


# Contact For
    
@bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    from app.utils.security import verify_reset_token

    email = verify_reset_token(token)
    if not email:
        flash("Reset link expired or invalid.", "danger")
        return redirect(url_for('main.login'))

    user = User.query.filter_by(email=email).first_or_404()

    if request.method == 'POST':
        password = request.form['password']
        confirm = request.form['confirm_password']

        if password != confirm:
            flash("Passwords do not match.", "danger")
            return redirect(request.url)

        user.password = generate_password_hash(password)
        db.session.commit()

        flash("Password reset successful. Please login.", "auth")
        return redirect(url_for('main.login'))

    return render_template('reset_password.html')

# Vehicle Management Routes
@bp.route('/manage_vehicles')
def manage_vehicles():
    if 'user_id' not in session:
        flash('Please log in to manage vehicles.', 'danger')
        return redirect(url_for('main.login'))
    
    return render_template('manage_vehicles.html')

# View All Vehicles
@bp.route('/vehicles')
def view_vehicles():
    if 'user_id' not in session:
        flash('Please log in to view your vehicles.', 'danger')
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    vehicles = EVVehicle.query.filter_by(user_id=user_id).all()  # Filter by logged-in user's ID
    return render_template('view_vehicles.html', vehicles=vehicles)


# Add a New Vehicle (Requires User to Be Logged In)
@bp.route('/add_vehicle', methods=['GET', 'POST'])
def add_vehicle():
    if 'user_id' not in session:
        flash('Please log in to add a vehicle.', 'vehicle')
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        vehicle_name = request.form['vehicle_name']
        vehicle_type = request.form['vehicle_type']
        license_plate = request.form['license_plate']
        battery_capacity = request.form['battery_capacity']
        range_per_charge = request.form['range_per_charge']
        max_charging_rate = request.form['max_charging_rate']
        print(EVVehicle.__table__.columns.keys())

        new_vehicle = EVVehicle(
            user_id=session['user_id'],  # Use the user_id from the session
            vehicle_name=vehicle_name,
            vehicle_type=vehicle_type,
            license_plate=license_plate,
            battery_capacity=battery_capacity,
            range_per_charge=range_per_charge,
            max_charging_rate=max_charging_rate
        )
        
        db.session.add(new_vehicle)
        db.session.commit()
        flash('Vehicle added successfully', 'vehicle')
        return redirect(url_for('main.view_vehicles'))  # Update the URL endpoint
        
    return render_template('add_vehicle.html')

# Update an Existing Vehicle (Requires User to Be Logged In)
@bp.route('/update_vehicle/<int:vehicle_id>', methods=['GET', 'POST'])
def update_vehicle(vehicle_id):
    if 'user_id' not in session:
        flash('Please log in to update a vehicle.', 'vehicle')
        return redirect(url_for('main.login'))
    
    vehicle = EVVehicle.query.get_or_404(vehicle_id)  # Get vehicle by ID
    
    if request.method == 'POST':
        vehicle.vehicle_name = request.form['vehicle_name']
        vehicle.vehicle_type = request.form['vehicle_type']
        vehicle.license_plate = request.form['license_plate']
        vehicle.battery_capacity = request.form['battery_capacity']
        vehicle.range_per_charge = request.form['range_per_charge']
        vehicle.max_charging_rate = request.form['max_charging_rate']
        db.session.commit()
        flash('Vehicle updated successfully', 'vehicle')
        return redirect(url_for('main.view_vehicles'))  # Update the URL endpoint
    
    return render_template('update_vehicle.html', vehicle=vehicle)

# Delete a Vehicle (Requires User to Be Logged In)
@bp.route('/delete_vehicle/<int:vehicle_id>', methods=['GET'])
def delete_vehicle(vehicle_id):
    if 'user_id' not in session:
        flash('Please log in to delete a vehicle.', 'vehicle')
        return redirect(url_for('main.login'))
    
    vehicle = EVVehicle.query.get_or_404(vehicle_id)  # Get vehicle by ID
    db.session.delete(vehicle)
    db.session.commit()
    flash('Vehicle deleted successfully', 'vehicle')
    return redirect(url_for('main.view_vehicles'))  # Update the URL endpoint

# Bookings (Requires User to Be Logged In)
from datetime import datetime

@bp.route('/my_bookings')
def my_bookings():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    bookings = (
        db.session.query(Booking, ChargingStation, Slot)
        .join(ChargingStation, Booking.station_id == ChargingStation.id)
        .join(Slot, Booking.slot_id == Slot.id)
        .filter(Booking.user_id == session['user_id'])
        .order_by(Booking.created_at.desc())
        .all()
    )

    return render_template(
        'my_bookings.html',
        bookings=bookings,
        flash_message=get_flashed_messages(with_categories=True)
    )



@bp.route('/features')
def features():
    return render_template('features.html')

@bp.route('/charging_stations')
def charging_stations():
    return render_template('chargingstations.html')

# Find Stations
def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in km
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Difference in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in km
    distance = R * c
    return distance
def estimate_charging_time(kwh, vehicle_rate, station_rate):
    effective_rate = min(vehicle_rate, station_rate)
    hours = kwh / effective_rate
    return int(hours * 60)

@bp.route("/payment/<int:booking_id>")
def payment_page(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    if booking.user_id != session.get("user_id"):
        return "Unauthorized", 403

    if booking.status != "Accepted":
        return "Payment not available", 400

    return render_template("payment.html", booking=booking)
@bp.route("/process_payment/<int:booking_id>", methods=["POST"])
def process_payment(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    if booking.payment_status == "Paid":
        flash("Payment already completed.", "payment")
        return redirect(url_for("main.my_bookings"))

    # 1️⃣ Mark payment as paid
    booking.payment_status = "Paid"

    # 2️⃣ Increment vehicle charge cycle
    vehicle = EVVehicle.query.get(booking.vehicle_id)
    if vehicle:
        vehicle.charge_cycles = (vehicle.charge_cycles or 0) + 1

        # OPTIONAL: degrade battery health
        # Simple model: lose 0.05% per charge
        vehicle.battery_health = max(
            70,
            (vehicle.battery_health or 100) - 0.05
        )

    db.session.commit()

    flash("Payment successful! Charging completed.", "payment")
    return redirect(url_for("main.my_bookings"))


@bp.route('/find_stations', methods=['GET'])
def find_stations():
    
    location = request.args.get('location')

    # Validate user input
    if not location:
        return jsonify({"error": "Location is required."}), 400

    # Get coordinates from the user's location
    latitude, longitude = get_coordinates_from_location(location)

    if latitude is None or longitude is None:
        return jsonify({"error": "Location not found or invalid."}), 400

    # Query the database for stations
    stations = ChargingStation.query.all()
    nearby_stations = []

    for station in stations:
        print(f"Station {station.name} - Latitude: {station.latitude}, Longitude: {station.longitude}")
        
        # Check if coordinates are missing and fetch them using LocationIQ
        if station.latitude is None or station.longitude is None:
            print(f"Station {station.name} is missijhfbehfng coordinates. Trying to fetch...")
            # Fetch coordinates using station's address
            station_lat, station_lon = get_coordinates_from_location(station.location)
            if station_lat is None or station_lon is None:
                print(f"Failed to fetch coordinates for {station.name}. Skipping...")
                continue  # Skip station if coordinates can't be fetched
            station.latitude = station_lat
            station.longitude = station_lon
            print(f"ni yabba {station_lat} nen unna")
        # Calculate the distance between the user's location and the station
        distance = haversine(latitude, longitude, station.latitude, station.longitude)
        print(f"Distance from user to {station.name}: {distance} km")  # Debug log

        # Filter stations within a 10 km radius
        if distance <= 10:
            nearby_stations.append({
            'name': station.name,
            'address': station.location,
            'latitude': station.latitude,   # Add latitude to the response
            'longitude': station.longitude,
             'stationid': station.id,
             # Add longitude to the response
            'distance': round(distance, 2)
        })

    # Handle case when no stations are nearby
    if not nearby_stations:
        return jsonify({"message": "No nearby stations found."}), 200

    return jsonify({'stations': nearby_stations})


@bp.route('/get_user_vehicles', methods=['GET'])
def get_user_vehicles():
    if 'user_id' not in session:
        return jsonify({"vehicles": []}), 401

    user_id = session['user_id']
    vehicles = EVVehicle.query.filter_by(user_id=user_id).all()

    vehicle_list = [
        {
            "id": v.id,
            "vehicle_name": v.vehicle_name,
            "license_plate": v.license_plate
        }
        for v in vehicles
    ]
    return jsonify({"vehicles": vehicle_list})




locationiq_api_key = 'pk.218199c167e2d299d7a2ac441eac33b2'  # Replace with your LocationIQ API key

@bp.route('/route-to-station', methods=['GET'])
def route_to_station():
    return render_template(
        'route_to_station.html',
        userLat=request.args.get('userLat'),
        userLon=request.args.get('userLon'),
        stationLat=request.args.get('stationLat'),
        stationLon=request.args.get('stationLon'),
        stationName=request.args.get('stationName'),
        stationAddress=request.args.get('stationAddress'),
        stationId=request.args.get('stationId')
    )




@bp.route('/book_slot', methods=['POST'])
def book_slot():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Login required'}), 401

    data = request.json
    station_id = data['station_id']
    slot_number = int(data['slot_name'])
    date_str = data['date']
    vehicle_id = data['vehicle_id']
    kwh = float(data['kwh'])

    station = ChargingStation.query.get_or_404(station_id)
    slot = Slot.query.filter_by(
        station_id=station_id,
        slot_number=slot_number
    ).first_or_404()

    vehicle = EVVehicle.query.get_or_404(vehicle_id)
    
    # SLOT WINDOW
    base_date = datetime.strptime(date_str, "%Y-%m-%d")
    slot_start = base_date.replace(hour=slot.start_hour, minute=0)
    slot_end = base_date.replace(hour=slot.end_hour, minute=0)

    # REQUIRED TIME
    effective_rate = min(vehicle.max_charging_rate, station.charger_power)
    required_minutes = int((kwh / effective_rate) * 60)
    # 🔒 AUTO LIMIT kWh BASED ON SLOT CAPACITY
    slot_duration_hours = slot.end_hour - slot.start_hour
    max_allowed_kwh = effective_rate * slot_duration_hours

    if kwh > max_allowed_kwh:
        return jsonify({
        'status': 'error',
        'message': f'Max kWh for this slot is {max_allowed_kwh:.1f} kWh'
    }), 400

    cursor = slot_start
    step = timedelta(minutes=15)
    BASE_RATE = 22  # ₹ per kWh
    system_price = round(kwh * BASE_RATE, 2)

    while cursor + timedelta(minutes=required_minutes) <= slot_end:
        conflict = Booking.query.filter(
            Booking.slot_id == slot.id,
            Booking.status.in_(['Pending', 'Accepted']),
            Booking.start_time < cursor + timedelta(minutes=required_minutes),
            Booking.end_time > cursor
        ).first()

        if not conflict:
            booking = Booking(
                    user_id=session['user_id'],
                    station_id=station.id,
                    slot_id=slot.id,
                    vehicle_id=vehicle.id,
                    start_time=cursor,
                    end_time=cursor + timedelta(minutes=required_minutes),
                    estimated_minutes=required_minutes,
                    kwh=kwh,
                    system_price=system_price,
                    final_price=None,
                    status='Pending'
            )
            

            db.session.add(booking)
            db.session.commit()
            send_email(
    to="ev.services.chargemate@gmail.com",
    subject="🔔 New Slot Booking",
    body=f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>New Slot Booking</title>
</head>
<body style="margin:0;padding:0;background:#f4f6f9;font-family:Arial,Helvetica,sans-serif;">

  <table width="100%" cellpadding="0" cellspacing="0" style="padding:20px;">
    <tr>
      <td align="center">

        <table width="520" cellpadding="0" cellspacing="0"
               style="background:#ffffff;border-radius:12px;
                      box-shadow:0 6px 18px rgba(0,0,0,0.15);
                      overflow:hidden;">

          <!-- HEADER -->
          <tr>
            <td style="background:linear-gradient(135deg,#0a7cff,#04befe);
                       color:white;padding:16px 20px;
                       font-size:18px;font-weight:bold;">
              🔔 New Slot Booking Received
            </td>
          </tr>

          <!-- CONTENT -->
          <tr>
            <td style="padding:20px;color:#333;font-size:14px;">

              <p style="margin-top:0;">
                A new EV charging slot has been booked. Please review and take action.
              </p>

              <table width="100%" cellpadding="6" cellspacing="0"
                     style="border-collapse:collapse;font-size:14px;">
                <tr>
                  <td style="font-weight:bold;">User ID</td>
                  <td>{session['user_id']}</td>
                </tr>
                <tr>
                  <td style="font-weight:bold;">Station</td>
                  <td>{station.name}</td>
                </tr>
                <tr>
                  <td style="font-weight:bold;">Slot</td>
                  <td>{slot.slot_number}</td>
                </tr>
                <tr>
                  <td style="font-weight:bold;">Date</td>
                  <td>{date_str}</td>
                </tr>
                <tr>
                  <td style="font-weight:bold;">Time</td>
                  <td>{booking.start_time.strftime('%H:%M')} - {booking.end_time.strftime('%H:%M')}</td>
                </tr>
                <tr>
                  <td style="font-weight:bold;">Energy</td>
                  <td>{kwh} kWh</td>
                </tr>
                <tr>
                  <td style="font-weight:bold;">System Price</td>
                  <td>₹{system_price}</td>
                </tr>
              </table>

              <!-- CTA -->
              <div style="margin-top:20px;text-align:center;">
                <a href="https://evchargemate-xs68.onrender.com/admin/view_bookings"
                   style="background:#0a7cff;color:white;
                          padding:10px 18px;
                          border-radius:8px;
                          text-decoration:none;
                          font-weight:bold;
                          display:inline-block;">
                  Go to Admin Panel
                </a>
              </div>

            </td>
          </tr>

          <!-- FOOTER -->
          <tr>
            <td style="background:#f0f2f5;
                       text-align:center;
                       padding:12px;
                       font-size:12px;
                       color:#777;">
              ChargeMate EV • Automated Notification
            </td>
          </tr>

        </table>

      </td>
    </tr>
  </table>

</body>
</html>
"""

)
            return jsonify({
                'status': 'success',
                'message': 'Slot booked, Awaiting for Station Confirmation',
                'redirect': url_for('main.my_bookings'),
                'start_time': booking.start_time.strftime('%H:%M'),
                'end_time': booking.end_time.strftime('%H:%M')
            })
           

        cursor += step

    return jsonify({
        'status': 'error',
        'message': 'Slot fully occupied'
    }), 409


@bp.route('/available_start_times', methods=['POST'])
def available_start_times():
    if 'user_id' not in session:
        return jsonify({'available_times': []}), 401

    data = request.json
    station_id = data.get('station_id')
    slot_number = int(data.get('slot_number'))
    date_str = data.get('date')
    vehicle_id = data.get('vehicle_id')
    kwh = float(data.get('kwh'))
    
    station = ChargingStation.query.get_or_404(station_id)
    slot = Slot.query.filter_by(
        station_id=station_id,
        slot_number=slot_number
    ).first_or_404()
    vehicle = EVVehicle.query.get_or_404(vehicle_id)

    # Slot window
    base_date = datetime.strptime(date_str, "%Y-%m-%d")
    slot_start = base_date.replace(hour=slot.start_hour, minute=0)
    slot_end = base_date.replace(hour=slot.end_hour, minute=0)

    # Required charging time
    effective_rate = min(vehicle.max_charging_rate, station.charger_power)
    required_minutes = int((kwh / effective_rate) * 60)

    cursor = slot_start
    step = timedelta(minutes=15)
    available_times = []

    while cursor + timedelta(minutes=required_minutes) <= slot_end:
        conflict = Booking.query.filter(
            Booking.slot_id == slot.id,
            Booking.status.in_(['Pending', 'Accepted']),
            Booking.start_time < cursor + timedelta(minutes=required_minutes),
            Booking.end_time > cursor
        ).first()

        if not conflict:
            available_times.append(cursor.strftime("%H:%M"))

        cursor += step

    return jsonify({
        "available_times": available_times
    })


@bp.route('/slot_congestion', methods=['POST'])
def slot_congestion():
    data = request.json

    station_id = data['station_id']
    slot_number = int(data['slot_number'])
    date_str = data['date']

    slot = Slot.query.filter_by(
        station_id=station_id,
        slot_number=slot_number
    ).first_or_404()

    base_date = datetime.strptime(date_str, "%Y-%m-%d")

    slot_start = base_date.replace(hour=slot.start_hour, minute=0, second=0)
    slot_end = base_date.replace(hour=slot.end_hour, minute=0, second=0)

    if slot_end <= slot_start:
        slot_end += timedelta(days=1)

    total_minutes = int((slot_end - slot_start).total_seconds() / 60)

    bookings = Booking.query.filter(
        Booking.slot_id == slot.id,
        Booking.status.in_(["Pending", "Accepted"]),
        Booking.start_time < slot_end,
        Booking.end_time > slot_start
    ).all()

    booked_minutes = 0
    for b in bookings:
        overlap_start = max(b.start_time, slot_start)
        overlap_end = min(b.end_time, slot_end)
        booked_minutes += max(
            0,
            int((overlap_end - overlap_start).total_seconds() / 60)
        )

    percentage = min(100, int((booked_minutes / total_minutes) * 100)) if total_minutes else 0

    level = (
        "GREEN" if percentage <= 40 else
        "YELLOW" if percentage <= 70 else
        "RED"
    )

    return jsonify({
        "percentage": percentage,
        "level": level
    })


@bp.route('/station_congestion/<int:station_id>')
def station_congestion(station_id):
    station = ChargingStation.query.get_or_404(station_id)
    now = datetime.now()

    slots = Slot.query.filter_by(station_id=station_id).all()
    total_minutes = 0
    booked_minutes = 0

    for slot in slots:
        slot_start = now.replace(hour=slot.start_hour, minute=0, second=0)
        slot_end = now.replace(hour=slot.end_hour, minute=0, second=0)

        if slot_end <= slot_start:
            slot_end += timedelta(days=1)

        duration = int((slot_end - slot_start).total_seconds() / 60)
        total_minutes += duration

        bookings = Booking.query.filter(
            Booking.slot_id == slot.id,
            Booking.status.in_(["Pending", "Accepted"]),
            Booking.start_time < slot_end,
            Booking.end_time > slot_start
        ).all()

        for b in bookings:
            overlap_start = max(b.start_time, slot_start)
            overlap_end = min(b.end_time, slot_end)
            booked_minutes += max(
                0,
                int((overlap_end - overlap_start).total_seconds() / 60)
            )

    percentage = min(100, int((booked_minutes / total_minutes) * 100)) if total_minutes else 0

    level = (
        "GREEN" if percentage <= 40 else
        "YELLOW" if percentage <= 70 else
        "RED"
    )

    return jsonify({
        "percentage": percentage,
        "level": level
    })



@bp.route('/battery_health')
def battery_health():
    user = session.get('user_id')  # Assuming you're getting the current user
    vehicles = EVVehicle.query.filter_by(user_id=user).all()  # Fetch all vehicles for the current user

    # Prepare data for Matplotlib graph
    vehicle_data = {}
    for vehicle in vehicles:
        charge_cycles = vehicle.charge_cycles
        battery_health = vehicle.battery_health
        vehicle_data[vehicle.vehicle_name] = {
            'charge_cycles': charge_cycles,
            'battery_health': battery_health
        }

    # Create a Matplotlib graph
    fig, ax = plt.subplots()

    # Ensure there are at least two points (even for small data)
    for vehicle_name, data in vehicle_data.items():
        charge_cycles = data['charge_cycles']
        battery_health = data['battery_health']

        # Plot the data as a line (or scatter for individual points)
        # Even if there's one point, ensure it's plotted to avoid empty graphs
        if charge_cycles and battery_health is not None:
            ax.plot([charge_cycles], [battery_health], marker='o', label=vehicle_name)
    
    ax.set(xlabel='Charge Cycles', ylabel='Battery Health (%)', title='Battery Health Over Charge Cycles')
    ax.legend()

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode('utf-8')

    return render_template('battery_health.html', vehicles=vehicles, graph_url=graph_url)

@bp.route('/energy-tips')
def energy_tips():
    return render_template('energytips.html')



@bp.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        subject = request.form['subject']
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Check if user_id is available in the session
        user_id = session.get('user_id')

        if user_id is None:
            flash("You must be logged in to submit a contact form.", 'danger')
            return redirect(url_for('main.login'))  # Or redirect to your login page

        # Save the contact message to the database
        contact = ContactUs(
            user_id=user_id,  # Automatically assign user_id from session
            subject=subject,
            name=name,
            email=email,
            message=message
        )
        db.session.add(contact)
        db.session.commit()

        flash('Your contact message has been sent successfully!', 'success')
        return redirect(url_for('main.contact_us'))

    return render_template('features.html')


@bp.route('/submit_feedback', methods=['GET', 'POST'])
def submit_feedback():
    if request.method == 'POST':
        name = request.form['name']
        comments = request.form['comments']
        rating = int(request.form['rating'])
        user_id = session.get('user_id')

        if user_id is None:
            flash("You must be logged in to submit a contact form.", 'danger')
            return redirect(url_for('main.login'))  # Or redirect to your login page
        # Save feedback to the database
        feedback = Feedback(user_id=user_id,name=name, comments=comments, rating=rating)
        db.session.add(feedback)
        db.session.commit()
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('main.submit_feedback'))

    return render_template('features.html')
@bp.route('/ping', methods=['GET'])
def ping():
    return "PING OK"





