from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, Admin, Slot, Booking, User, ChargingStation, ContactUs, Feedback
from werkzeug.security import check_password_hash, generate_password_hash
import requests
from app.utils.email import send_email



admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin login
from flask import get_flashed_messages

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            session.clear()  # 🔥 CLEAR OLD FLASHES + SESSIONS
            session['admin_id'] = admin.admin_id
            flash('Login successful!', 'success')
            return redirect(url_for('admin.dashboard'))

        flash('Invalid credentials.', 'error')
        return redirect(url_for('admin.login'))

    return render_template('admin_login.html')


# Admin dashboard
@admin_bp.route('/dashboard')
def dashboard():
    if 'admin_id' not in session:
        flash('You must log in to access this page.', 'error')
        return redirect(url_for('admin.login'))
    return render_template(
    "admin.html",
    total_stations=ChargingStation.query.count(),
    pending_bookings=Booking.query.filter_by(status="Pending").count(),
    total_users=User.query.count(),
    
    recent_activity=[
        "New booking created",
        "Station added",
        "User registered"
    ]
)

@admin_bp.route('/appup')
def appup():
    if 'admin_id' not in session:
        flash('You must log in to access this page.', 'error')
        return redirect(url_for('admin.login'))

    stations = ChargingStation.query.all()
    return render_template('appup.html', stations=stations)
# Logout
@admin_bp.route('/logout')
def logout():
    session.pop('admin_id', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('admin.login'))

# Manage Stations (Admin View)
@admin_bp.route('/stations')
def stations_admin():
    if 'admin_id' not in session:
        flash('You must log in to access this page.', 'error')
        return redirect(url_for('admin.login'))

    stations = ChargingStation.query.all()
    return render_template('managestations.html', stations=stations)



@admin_bp.route('/view_bookings', methods=['GET', 'POST'])
def view_bookings():
    # Fetch all pending bookings
    bookings = Booking.query.filter_by(status='Pending').all()
    
    if request.method == 'POST':
        booking_id = request.form['booking_id']
        action = request.form['action']
        price = request.form.get('price')
        price_reason = request.form.get("price_reason") or ""
        
        booking = Booking.query.get(booking_id)
        user = User.query.get(booking.user_id)

        if action == 'accept':
            booking.status = 'Accepted'
            booking.final_price = float(price) if price else booking.system_price
            booking.price_reason = price_reason

            db.session.commit()

            # Send Booking Confirmed Email
            send_email(
                to=user.email,
                subject="✅ Booking Confirmed – ChargeMate",
                body=f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Booking Confirmed</title>
</head>
<body style="margin:0;padding:0;background:#f4f6f9;font-family:Arial,Helvetica,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="padding:20px;">
    <tr>
      <td align="center">
        <table width="520" cellpadding="0" cellspacing="0"
               style="background:#ffffff;border-radius:12px;
                      box-shadow:0 6px 18px rgba(0,0,0,0.15);
                      overflow:hidden;">
          <tr>
            <td style="background:linear-gradient(135deg,#2ecc71,#27ae60);
                       color:white;padding:16px 20px;
                       font-size:18px;font-weight:bold;">
              ✅ Booking Confirmed
            </td>
          </tr>
          <tr>
            <td style="padding:20px;color:#333;font-size:14px;">
              <p style="margin-top:0;">
                Hi <b>{user.name}</b>,
              </p>
              <p>
                Your EV charging slot has been <b style="color:#27ae60;">successfully confirmed</b>.
                Below are the booking details:
              </p>
              <table width="100%" cellpadding="6" cellspacing="0"
                     style="border-collapse:collapse;font-size:14px;margin-top:10px;">
                <tr><td style="font-weight:bold;">Station</td><td>{booking.station.name}</td></tr>
                <tr><td style="font-weight:bold;">Slot</td><td>{booking.slot.slot_number}</td></tr>
                <tr><td style="font-weight:bold;">Time</td><td>{booking.start_time.strftime('%H:%M')} – {booking.end_time.strftime('%H:%M')}</td></tr>
                <tr><td style="font-weight:bold;">Energy</td><td>{booking.kwh} kWh</td></tr>
                <tr><td style="font-weight:bold;">Final Price</td><td style="color:#27ae60;font-weight:bold;">₹{booking.final_price}</td></tr>
              </table>
              <div style="margin-top:16px;padding:12px;background:#f9fafb;border-left:4px solid #27ae60;font-size:13px;">
                <b>Price Note:</b><br>{booking.price_reason or "No additional charges"}
              </div>
              <div style="margin-top:20px;text-align:center;">
                <a href="https://evchargemate-xs68.onrender.com/my_bookings"
                   style="background:#27ae60;color:white;
                          padding:10px 18px;
                          border-radius:8px;
                          text-decoration:none;
                          font-weight:bold;
                          display:inline-block;">
                  View My Bookings
                </a>
              </div>
            </td>
          </tr>
          <tr>
            <td style="background:#f0f2f5;text-align:center;padding:12px;font-size:12px;color:#777;">
              ⚡ ChargeMate EV • Thank you for choosing us
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

        elif action == 'reject':
            booking.status = 'Rejected'
            booking.price_reason = price_reason
            db.session.commit()

            # Send Booking Rejected Email
            send_email(
                to=user.email,
                subject="❌ Booking Rejected – ChargeMate",
                body=f"""
Hi {user.name},

Your booking at {booking.station.name}, Slot {booking.slot.slot_number} on 
{booking.start_time.strftime('%H:%M')} – {booking.end_time.strftime('%H:%M')} 
has been <b>rejected</b>.

Reason: {booking.price_reason or "No reason provided"}

View your bookings: https://evchargemate-xs68.onrender.com/my_bookings
"""
            )

        elif action == 'cancel':
            booking.status = 'Cancelled'
            db.session.commit()
            # Optional: send cancelled email here

        return redirect(url_for('admin.view_bookings'))

    return render_template('view_bookings.html', bookings=bookings)


def calculate_generated_price(kwh):
    # Your price calculation logic based on kWh or other criteria
    return kwh * 0.2  # Example rate per kWh

@admin_bp.route('/all_bookings')
def all_bookings():
    if 'admin_id' not in session:
        flash('Admin login required', 'error')
        return redirect(url_for('admin.login'))

    bookings = (
        Booking.query
        .order_by(Booking.created_at.desc())
        .all()
    )

    return render_template('all_bookings.html', bookings=bookings)


# Get Coordinates from Location Name
def get_coordinates_from_location(location_name):
    api_key = "pk.218199c167e2d299d7a2ac441eac33b2"  # Replace with your LocationIQ API key
    url = f"https://us1.locationiq.com/v1/search.php?key={api_key}&q={location_name}&format=json"
    response = requests.get(url)
    data = response.json()

    if data:
        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])
        return lat, lon
    else:
        return None, None

# Add Station
@admin_bp.route('/add_update_delete_view_stations', methods=['GET', 'POST'])
def add_update_delete_view_stations():
    stations = ChargingStation.query.all()

    if request.method == 'POST':
        # Handle different form operations
        if 'add_station' in request.form:
            name = request.form['name']
            location = request.form['location']
            latitude = request.form['latitude']
            longitude = request.form['longitude']
            if name and location and latitude and longitude:
                new_station = ChargingStation(name=name, location=location, latitude=latitude, longitude=longitude)
                db.session.add(new_station)
                db.session.commit()
                flash('Station added successfully!', 'success')
            else:
                flash('All fields are required to add a station.', 'error')

        if 'delete_station' in request.form:
            station_id = int(request.form['station_id'])
            station = ChargingStation.query.get_or_404(station_id)
            db.session.delete(station)
            db.session.commit()
            flash('Station deleted successfully!', 'success')

        if 'update_station' in request.form:
            station_id = int(request.form['station_id'])
            station = ChargingStation.query.get_or_404(station_id)
            station.name = request.form['station_name']
            station.location = request.form['station_location']
            db.session.commit()
            flash('Station updated successfully!', 'success')

        return redirect(url_for('admin.add_update_delete_view_stations'))

    return render_template('appup.html', stations=stations)




SLOT_WINDOWS = {
    1: (0, 3),
    2: (3, 6),
    3: (6, 9),
    4: (9, 12),
    5: (12, 15),
    6: (15, 18),
    7: (18, 21),
    8: (21, 23)
}
@admin_bp.route('/add_station', methods=['GET', 'POST'])
def add_station():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        if not latitude or not longitude:
            flash('Invalid location name or coordinates not selected.', 'error')
            return redirect(url_for('admin.stations_admin'))

        # 1️⃣ Create station
        station = ChargingStation(
            name=name,
            location=location,
            latitude=latitude,
            longitude=longitude,
            charger_power=22,
            total_slots=8,
            status='Enabled'
        )
        db.session.add(station)
        db.session.flush()  # IMPORTANT: get station ID

        # 2️⃣ Create 8 fixed slots for this station
        for slot_no, (start, end) in SLOT_WINDOWS.items():
            db.session.add(
                Slot(
                    station_id=station.id,
                    slot_number=slot_no,
                    start_hour=start,
                    end_hour=end
            )
        )

        db.session.commit()

        flash('Charging station added successfully with 7 slots!', 'success')
        return redirect(url_for('admin.stations_admin'))

    return render_template('admin/stations.html')



# Edit Station
@admin_bp.route('/update_station', methods=['POST'])
def edit_station():
    station_id = int(request.form['station-id'])
    station = ChargingStation.query.get_or_404(station_id)

    # Update name and location only
    station.name = request.form.get('station-name-edit', station.name)
    station.location = request.form.get('station-location-edit', station.location)

    db.session.commit()
    flash('Station updated successfully!', 'success')
    return redirect(url_for('admin.appup'))


# Delete Station
@admin_bp.route('/delete_station', methods=['POST'])
def delete_station():
    station_id = int(request.form['station-id-delete'])
    station = ChargingStation.query.get_or_404(station_id)

    # Remove manual check and allow database cascade delete to handle it
    db.session.delete(station)
    db.session.commit()

    flash("Station deleted successfully!", "success")
    return redirect(url_for('admin.stations_admin'))



# Toggle Station Status
# Toggle Station Status


from flask import flash, redirect, url_for, render_template, request

@admin_bp.route('/toggle_station', methods=['GET', 'POST'])
def toggle_station():
    if request.method == 'POST':
        station_id = request.form.get('station_id')
        status = request.form.get('status')

        # Validate input
        if not station_id or not status:
            flash("Invalid station or status selection.", "error")
            return redirect(url_for('admin.toggle_station'))

        station = ChargingStation.query.get(station_id)

        if not station:
            flash("Station not found.", "error")
            return redirect(url_for('admin.toggle_station'))

        # Update status
        station.status = status
        db.session.commit()

        flash(
            f"Station '{station.name}' has been {status.lower()} successfully.",
            "success"
        )

        return redirect(url_for('admin.toggle_station'))

    # GET request
    stations = ChargingStation.query.all()
    return render_template('toggle_station.html', stations=stations)



@admin_bp.route('/view_slot_bookings')
def view_slot_bookings():
    bookings = Booking.query.filter_by(status='Pending').all()  
    slots = Slot.query.all()# Fetch all pending bookings
    return render_template('view_slot_bookings.html', bookings=bookings)



@admin_bp.route('/accept_booking/<int:booking_id>', methods=['POST'])
def accept_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    final_price = float(request.form['price'])
    print(final_price)
    booking.final_price = final_price
    booking.status = 'Accepted'

    db.session.commit()
    flash(
    f"Your booking at {booking.station_id} was accepted. Final price ₹{booking.final_price}",
    "booking_user"
)

    return redirect(url_for('admin.view_bookings'))




@admin_bp.route('/reject_booking/<int:booking_id>', methods=['POST'])
def reject_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.status = 'Rejected'

    try:
        db.session.commit()
        flash("Booking rejected.", 'success')
    except Exception as e:
        db.session.rollback()
        flash("Error rejecting booking: " + str(e), 'danger')

    return redirect(url_for('admin.view_slot_bookings'))


@admin_bp.route('/update_slot/<int:slot_id>', methods=['GET', 'POST'])
def update_slot(slot_id):
    slot = Slot.query.get_or_404(slot_id)

    if request.method == 'POST':
        slot.station_id = request.form['station_id']
        slot.slot_name = request.form['slot_name']
        slot.price = request.form['price']
        
        db.session.commit()
        flash('Slot updated successfully', 'success')
        return redirect(url_for('admin.manage_slots'))

    # Fetch all stations for the dropdown in the form
    stations = ChargingStation.query.all()
    return render_template('update_slot.html', slot=slot, stations=stations)

@admin_bp.route('/delete_slot/<int:slot_id>', methods=['POST'])
def delete_slot(slot_id):
    slot = Slot.query.get_or_404(slot_id)

    # Delete all bookings that reference the slot
    bookings = Booking.query.filter_by(slot_id=slot_id).all()
    for booking in bookings:
        db.session.delete(booking)

    # Now delete the slot
    db.session.delete(slot)
    db.session.commit()

    flash('Slot and its associated bookings deleted successfully', 'success')
    return redirect(url_for('admin.manage_slots'))


@admin_bp.route('/manage_slots')
def manage_slots():
    slots = Slot.query.all()  # Fetch all slots
    return render_template('manage_slots.html', slots=slots)

# Admin Registration
@admin_bp.route('/register', methods=['GET', 'POST'])
def register_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for('admin.register_admin'))

        if Admin.query.filter_by(username=username).first():
            flash("Admin with this username already exists.", "error")
            return redirect(url_for('admin.register_admin'))

        hashed_password = generate_password_hash(password)
        new_admin = Admin(username=username, password=hashed_password)
        db.session.add(new_admin)
        db.session.commit()

        flash("Admin registered successfully!", "success")
        return redirect(url_for('admin.login'))

    return render_template('admin_register.html')



@admin_bp.route('/view_users')
def view_users():
    users = User.query.all()  # Fetch all users from the database
    return render_template('view_users.html', users=users)

@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)  # Fetch user by ID or return 404 if not found
    try:
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully", 'success')
    except Exception as e:
        db.session.rollback()
        flash("Error deleting user: " + str(e), 'danger')
    return redirect(url_for('admin.view_users'))  # Redirect back to the user list

@admin_bp.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)  # Fetch user by ID or return 404 if not found
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.phone = request.form['phone']
        
        try:
            db.session.commit()
            flash("User updated successfully", 'success')
            return redirect(url_for('admin.view_users'))
        except Exception as e:
            db.session.rollback()
            flash("Error updating user: " + str(e), 'danger')
    
    return render_template('update_user.html', user=user)



@admin_bp.route('/contact_us', methods=['GET'])
def admin_contact_us():
    # Ensure the user is an admin, you can check by user role if needed
   
    # Retrieve all contact messages
    contact_messages = ContactUs.query.all()

    # Fetch user details for each contact message (if needed)
    for contact in contact_messages:
        user = User.query.get(contact.user_id)  # Fetch user details for each contact message
        contact.user_name = user.name if user else 'Unknown'  # Add user name to contact message
    
    return render_template('admin_contact_us.html', contact_messages=contact_messages)

from flask_mail import Message


@admin_bp.route('/close_contact/<int:contact_id>', methods=['POST'])
def close_contact(contact_id):
    contact = ContactUs.query.get_or_404(contact_id)

    admin_reply = request.form['admin_reply']
    contact.status = "Closed"
    contact.admin_reply = admin_reply
    db.session.commit()

    user = User.query.get(contact.user_id)

    # 📧 Send Email to User
    html = render_template(
        "emails/contact_closed.html",
        user_name=user.name,
        subject=contact.subject,
        solution=admin_reply
    )

    email_sent = send_email(
        user.email,
        "Your Query Has Been Resolved – ChargeMate",
        html
    )

    if email_sent:
        flash("Query closed and user notified via email.", "success")
    else:
        flash("Query closed, but email delivery failed.", "error")

    return redirect(url_for('admin.admin_contact_us'))


@admin_bp.route('/feedback', methods=['GET'])
def admin_feedback():
    # Ensure the user is an admin
  # Redirect non-admin users to home page

    # Retrieve all feedback messages
    feedback_messages = Feedback.query.all()

    # Fetch user details for each feedback (if needed)
    for feedback in feedback_messages:
        user = User.query.get(feedback.user_id)  # Fetch user details for each feedback
        feedback.user_name = user.name if user else 'Unknown'  # Add user name to feedback

    return render_template('admin_feedback.html', feedback_messages=feedback_messages)









