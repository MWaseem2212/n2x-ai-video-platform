from app.db.session import engine

if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            print("Database Connection Successful!")

    except Exception as e:
        print(f"Connection Failed: {e}")
