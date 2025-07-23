import os

class Settings:
    # Database backend: "sqlite" or "postgres"
    DB_BACKEND: str = os.getenv('DB_BACKEND', 'sqlite')

    # SQLite settings
    SQLITE_DB_PATH: str = os.getenv('SQLITE_DB_PATH', '.././meal_calorie_db.sqlite3')

    # Postgres settings
    DB_USER: str = os.getenv('POSTGRES_USER', 'postgres')
    DB_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', 'postgres')
    DB_HOST: str = os.getenv('POSTGRES_HOST', 'localhost')
    DB_PORT: str = os.getenv('POSTGRES_PORT', '5432')
    DB_NAME: str = os.getenv('POSTGRES_DB', 'meal_calorie_db')

    REDIS_HOST: str = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT: int = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB: int = int(os.getenv('REDIS_DB', 1))
    REDIS_URL: str = os.getenv('REDIS_URL', f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}')

    JWT_SECRET: str = os.getenv('JWT_SECRET', 'supersecretjwt')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', 'HS256')

    @property
    def database_url(self):
        if self.DB_BACKEND == "sqlite":
            return f"sqlite+aiosqlite:///{self.SQLITE_DB_PATH}"
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()