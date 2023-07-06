from config import settings
from sqlalchemy import create_engine

engine = create_engine(
    f"oracle+oracledb://{settings.db_username.get_secret_value()}:{settings.db_pwd.get_secret_value()}@{settings.db_host}:{settings.db_port}/{settings.db_sid}",
    thick_mode={"lib_dir": "/lib/oracle/21/client64/instantclient_21_10"},
    echo=False,
)
