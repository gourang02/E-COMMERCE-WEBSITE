from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        # Using raw SQL for migration
        with db.engine.connect() as conn:
            try:
                conn.execute(text('ALTER TABLE "order" ADD COLUMN delivery_option VARCHAR(50) DEFAULT \'Standard\''))
                conn.execute(text('ALTER TABLE "order" ADD COLUMN delivery_charge FLOAT DEFAULT 0.0'))
                conn.commit()
                print("Migration successful: Added columns to 'order' table.")
            except Exception as e:
                print(f"Migration failed (columns might already exist): {e}")

if __name__ == "__main__":
    migrate()
