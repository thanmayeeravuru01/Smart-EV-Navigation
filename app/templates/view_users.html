<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Users Management | ChargeMate Admin</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <style>
    body {
      font-family: "Segoe UI", Arial, sans-serif;
      background: #f4f7fb;
      margin: 0;
      padding: 0;
    }

    .container {
      max-width: 1000px;
      margin: 40px auto;
      background: white;
      padding: 26px 30px;
      border-radius: 14px;
      box-shadow: 0 12px 30px rgba(0,0,0,0.12);
    }

    h1 {
      margin-bottom: 20px;
      color: #1e293b;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }

    th, td {
      padding: 12px 14px;
      border-bottom: 1px solid #e5e7eb;
    }

    th {
      background: #0a7cff;
      color: white;
      text-align: left;
    }

    tr:hover td {
      background: #f1f5f9;
    }

    a {
      color: #0a7cff;
      font-weight: 600;
      text-decoration: none;
      margin-right: 8px;
    }

    a:hover {
      text-decoration: underline;
    }

    button {
      background: #ef4444;
      border: none;
      color: white;
      padding: 6px 10px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 13px;
    }

    button:hover {
      background: #dc2626;
    }
    .flash-wrapper {
      margin-bottom: 16px;
    }

    .flash {
      padding: 12px 14px;
      border-radius: 10px;
      font-size: 14px;
      margin-bottom: 10px;
      animation: fadeIn .3s ease;
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

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(-6px); }
      to { opacity: 1; transform: translateY(0); }
    }
  </style>
</head>

<body>
 {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
      <div class="flash-wrapper">
        {% for category, message in messages %}
          <div class="flash {{ category }}">{{ message }}</div>
        {% endfor %}
      </div>
    {% endif %}
    {% endwith %}
  <div class="container">
    <a href="{{ url_for('admin.dashboard') }}" class="back-btn">← Back</a>
    <h1>Users List</h1>

    {% if users %}
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {% for user in users %}
          <tr>
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.phone }}</td>
            <td>
              <a href="{{ url_for('admin.update_user', user_id=user.user_id) }}">Edit</a>
              <form action="{{ url_for('admin.delete_user', user_id=user.user_id) }}" method="POST" style="display:inline;">
                <button onclick="return confirm('Delete this user?')">Delete</button>
              </form>
            </td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    {% else %}
      <p>No users found.</p>
    {% endif %}
  </div>

</body>
</html>
