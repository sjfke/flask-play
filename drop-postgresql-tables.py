from project import db, create_app, models
app=create_app()
with app.app_context():
    db.drop_all()