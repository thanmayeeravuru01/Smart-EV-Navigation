<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Admin – Bookings</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f6f8;
        }

        h1 {
            text-align: center;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
        }

        th, td {
            border: 1px solid #ccc;
            padding: 10px;
            text-align: center;
        }

        th {
            background: #004d99;
            color: white;
        }

        input[type="number"] {
            width: 90px;
        }

        button {
            padding: 5px 10px;
            margin-top: 5px;
            cursor: pointer;
        }

        .accept {
            background: green;
            color: white;
        }

        .reject {
            background: red;
            color: white;
        }
        .flash-wrapper {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 2000;
}

.flash {
    padding: 12px 16px;
    border-radius: 8px;
    font-size: 14px;
    margin-bottom: 10px;
    box-shadow: 0 8px 18px rgba(0,0,0,0.15);
    animation: slideIn 0.3s ease;
}

.flash.success {
    background: #e6f9f0;
    color: #065f46;
    border-left: 5px solid #10b981;
}

.flash.error {
    background: #fee2e2;
    color: #7f1d1d;
    border-left: 5px solid #ef4444;
}

@keyframes slideIn {
    from { transform: translateX(20px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}.back-btn {
    position: fixed;
    top: 16px;
    right: 20px;
    padding: 8px 14px;
    background: #004d99;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
    z-index: 1500;
}

.back-btn:hover {
    background: #003366;
}

    </style>
</head>

<body>
<!-- FLASH NOTIFICATIONS -->
{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}
<div class="flash-wrapper">
    {% for category, message in messages %}
        <div class="flash {{ category }}">{{ message }}</div>
    {% endfor %}
</div>
{% endif %}
{% endwith %}

<h1>Pending Bookings</h1>
<button class="back-btn" onclick="window.location.href='{{ url_for('admin.dashboard') }}'">
    ← Dashboard
  </button>
<table>
    <thead>
        <tr>
            <th>Station</th>
            <th>Slot</th>
            <th>Time</th>
            <th>KWh</th>
            <th>System Price</th>
            <th>Final Price</th>
          
            <th>Status</th>
            <th>Action</th>
        </tr>
    </thead>

    <tbody>
    {% for booking in bookings %}
        <tr>
            <td>{{ booking.station.name }}</td>

            <td>Slot {{ booking.slot.slot_number }}</td>

            <td>
                {{ booking.start_time.strftime('%H:%M') }}
                –
                {{ booking.end_time.strftime('%H:%M') }}
            </td>

            <td>{{ booking.kwh }}</td>

            <td>₹ {{ booking.system_price }}</td>

            <td>
    {% if booking.status == 'Pending' %}
    <form method="POST">
        <input type="hidden" name="booking_id" value="{{ booking.id }}">
        <input type="hidden" name="action" value="accept">

        <input
            type="number"
            name="price"
            value="{{ booking.final_price or booking.system_price }}"
            step="0.01"
            required
        >

        <div class="mt-2">
            <textarea
                name="price_reason"
                rows="3"
                class="form-control"
                placeholder="Reason for price change"
                required
            >{{ booking.price_reason or "" }}</textarea>
        </div>

        <button class="accept" type="submit">Accept</button>
    </form>
    {% else %}
        —
    {% endif %}
</td>


            <td>{{ booking.status }}</td>

            <td>
                {% if booking.status == 'Pending' %}
                <form method="POST">
    <input type="hidden" name="booking_id" value="{{ booking.id }}">
    <input type="hidden" name="action" value="reject">

    <textarea
        name="price_reason"
        rows="3"
        placeholder="Reason for rejection"
        required
    ></textarea>

    <button class="reject" type="submit">Reject</button>
</form>

                {% else %}
                    —
                {% endif %}
            </td>
        </tr>
    {% else %}
        <tr>
            <td colspan="8">No bookings available</td>
        </tr>
    {% endfor %}
    </tbody>
</table>

</body>
<script>
setTimeout(() => {
    const f = document.querySelector('.flash-wrapper');
    if (f) f.style.display = 'none';
}, 3000);
</script>

</html>

