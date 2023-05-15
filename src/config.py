from decouple import config

BASE_PATH = config("BASE_PATH", default="/api")
DATABASE_URL = config("DATABASE_URL", default="postgresql://postgres:password@localhost:5432/setter")
