<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Vehicles</title>

    <!-- Existing CSS (kept) -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/userdashboard.css') }}">

    <!-- Page-specific CSS -->
    <style>
        /* ===== PAGE RESET (SCOPED) ===== */
        body {
            margin: 0;
            background: #f4f6f9;
            font-family: "Segoe UI", Arial, sans-serif;
        }

        /* ===== NAVBAR ===== */
        .vehicles-navbar {
            height: 64px;
            background: linear-gradient(135deg, #00509e, #00509e);
            color: white;
            display: flex;
            align-items: center;
            padding: 0 20px;
            justify-content: space-between;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }

        .nav-left {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .hamburger {
            font-size: 26px;
            cursor: pointer;
            user-select: none;
        }

        .nav-title {
            font-size: 20px;
            font-weight: bold;
        }

        .nav-right button {
            background: rgba(255,255,255,0.15);
            border: none;
            color: white;
            padding: 8px 14px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
        }

        .nav-right button:hover {
            background: rgba(255,255,255,0.25);
        }

        /* ===== DROPDOWN ===== */
        .menu-dropdown {
            position: absolute;
            top: 64px;
            left: 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            width: 200px;
            display: none;
            z-index: 9999;
            overflow: hidden;
        }

        .menu-dropdown a {
            display: block;
            padding: 12px 16px;
            color: #1f2937;
            text-decoration: none;
            font-weight: 500;
        }

        .menu-dropdown a:hover {
            background: #f1f5f9;
        }

        /* ===== FLASH ===== */
        .flash-wrapper {
            position: fixed;
            top: 80px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 9999;
        }

        .flash.vehicle {
            background: #ecfdf5;
            color: #065f46;
            padding: 14px 22px;
            border-radius: 10px;
            font-weight: bold;
            box-shadow: 0 8px 20px rgba(0,0,0,0.25);
        }

        /* ===== CONTENT CARD ===== */
        .vehicles-container {
            max-width: 1000px;
            margin: 40px auto;
            background: white;
            border-radius: 14px;
            padding: 26px 28px;
            box-shadow: 0 12px 30px rgba(0,0,0,0.12);
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th {
            background: #f1f5f9;
            text-align: left;
            padding: 12px;
            font-size: 14px;
        }

        td {
            padding: 12px;
            border-top: 1px solid #e5e7eb;
            font-size: 14px;
        }

        tr:hover {
            background: #f9fafb;
        }

        .danger {
            color: #dc2626;
            font-weight: bold;
        }

        .btn-primary {
            display: inline-block;
            margin-top: 20px;
            background: linear-gradient(135deg, #00509e, #00509e);
            color: white;
            padding: 12px 18px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: bold;
        }

        .btn-primary:hover {
            box-shadow: 0 6px 16px rgba(10,124,255,0.35);
        }
        .btn-back{
         color:#f1f5f9
        }
    </style>
</head>

<body>

<!-- FLASH -->
{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}
<div class="flash-wrapper">
    {% for category, message in messages %}
        {% if category == 'vehicle' %}
        <div class="flash vehicle">{{ message }}</div>
        {% endif %}
    {% endfor %}
</div>
{% endif %}
{% endwith %}

<!-- NAVBAR -->
<div class="vehicles-navbar">
    <div class="nav-left">
        <div class="hamburger" onclick="toggleMenu()">☰</div>
        <div class="nav-title">My Vehicles</div>
    </div>

    <div class="back-button">
    <a href="{{ url_for('main.user_dashboard') }}" class="btn-back">⬅ Back</a>
</div>

</div>

<!-- DROPDOWN -->
<div class="menu-dropdown" id="menuDropdown">
    <a href="{{ url_for('main.profile') }}">👤 Profile</a>
    <a href="{{ url_for('main.change_password') }}">🔑 Change Password</a>
    <a href="{{ url_for('main.logout') }}">🚪 Logout</a>
</div>

<!-- CONTENT -->
<div class="vehicles-container">
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Plate</th>
                <th>Battery (kWh)</th>
                <th>Range (km)</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for v in vehicles %}
            <tr>
                <td>{{ v.vehicle_name }}</td>
                <td>{{ v.vehicle_type }}</td>
                <td>{{ v.license_plate }}</td>
                <td>{{ v.battery_capacity }}</td>
                <td>{{ v.range_per_charge }}</td>
                <td>
                    <a href="{{ url_for('main.update_vehicle', vehicle_id=v.id) }}">Edit</a> |
                    <a href="{{ url_for('main.delete_vehicle', vehicle_id=v.id) }}" class="danger">Delete</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <a href="{{ url_for('main.add_vehicle') }}" class="btn-primary">➕ Add New Vehicle</a>
</div>

<script>
function toggleMenu() {
    const m = document.getElementById("menuDropdown");
    m.style.display = m.style.display === "block" ? "none" : "block";
}

document.addEventListener("click", function(e) {
    const menu = document.getElementById("menuDropdown");
    if (!e.target.closest(".hamburger")) {
        menu.style.display = "none";
    }
});

setTimeout(() => {
    const f = document.querySelector('.flash-wrapper');
    if (f) f.style.display = 'none';
}, 3000);
</script>

</body>
</html>
