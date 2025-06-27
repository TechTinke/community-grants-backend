from app import create_app, db
from app.models import Grant, Application, Feedback

app = create_app()
with app.app_context():
    print("Database URL:", db.engine.url)
    print("Models in metadata:", db.metadata.tables.keys())
    db.drop_all()
    db.create_all()
    print("Tables created successfully!")
    tables = db.engine.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    print("Tables in database:", tables)