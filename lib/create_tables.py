# create_tables.py

from lib.models import Base
from lib import engine

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("✅ Tables created successfully!")