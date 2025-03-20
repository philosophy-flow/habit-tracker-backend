import os
from dotenv import load_dotenv
from datetime import timedelta


load_dotenv(override=True)

JWT_VERIFY_KEY = os.getenv("JWT_VERIFY_KEY")
JWT_VERIFY_MINUTES = float(os.getenv("JWT_VERIFY_EXPIRE_MINUTES", "5"))
JWT_AUTH_KEY = os.getenv("JWT_AUTH_KEY")
JWT_AUTH_MINUTES = float(os.getenv("JWT_AUTH_EXPIRE_MINUTES", "15"))
JWT_REFRESH_KEY = os.getenv("JWT_REFRESH_KEY")
JWT_REFRESH_DAYS = float(os.getenv("JWT_REFRESH_DAYS", "3"))
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


jwt_verify_config = {
    "key": JWT_VERIFY_KEY,
    "time_diff": timedelta(minutes=JWT_VERIFY_MINUTES),
    "algorithm": JWT_ALGORITHM,
}

jwt_auth_config = {
    "key": JWT_AUTH_KEY,
    "time_diff": timedelta(minutes=JWT_AUTH_MINUTES),
    "algorithm": JWT_ALGORITHM,
}

jwt_refresh_config = {
    "key": JWT_REFRESH_KEY,
    "time_diff": timedelta(days=JWT_REFRESH_DAYS),
    "algorithm": JWT_ALGORITHM,
}
