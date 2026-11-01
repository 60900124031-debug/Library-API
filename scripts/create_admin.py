import getpass

import app.main  # noqa: F401  (memastikan semua model dan tabel terdaftar)
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.modules.auth.models import Role, User


def main():
    username = input("Username admin: ").strip()
    password = getpass.getpass("Password (min 8 karakter): ")
    if len(username) < 3 or len(password) < 8:
        print("Username minimal 3 karakter dan password minimal 8 karakter")
        return

    with SessionLocal() as db:
        if db.query(User).filter(User.username == username).first():
            print("Username sudah ada")
            return
        db.add(
            User(
                username=username,
                hashed_password=hash_password(password),
                role=Role.ADMIN,
            )
        )
        db.commit()
    print("Admin berhasil dibuat")


if __name__ == "__main__":
    main()