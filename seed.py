from werkzeug.security import generate_password_hash

from app import User, app, db


def create_users():
    with app.app_context():
        # This creates the new database structure (including the role column)
        db.create_all()

        # Clean up any partial data
        db.session.query(User).delete()

        users = [
            User(
                username="admin",
                password=generate_password_hash("peb_admin_1"),
                role="admin",
            ),
            User(
                username="manager",
                password=generate_password_hash("peb_manager_2"),
                role="manager",
            ),
            User(
                username="researcher",
                password=generate_password_hash("peb_researcher_3"),
                role="researcher",
            ),
        ]

        db.session.add_all(users)
        db.session.commit()
        print("--- SUCCESS ---")
        print("Database recreated and users added.")


if __name__ == "__main__":
    create_users()
