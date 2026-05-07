import os

class Config:
   
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret-key"
    SECURITY_PASSWORD_SALT = "reset-password-salt"

    SQLALCHEMY_DATABASE_URI = "postgresql://meghana:xRTPgAWePWuh2JpfhcT31KBfcQkQZUNy@dpg-d7ken9vavr4c73f7iucg-a.oregon-postgres.render.com/evchargemate?options=-csearch_path=chargemate"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
   
    MAIL_DEFAULT_SENDER = os.environ.get(
        "MAIL_DEFAULT_SENDER",
        "ChargeMate <ev.services.chargemate@gmail.com>"
    )



