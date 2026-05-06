from app.database import get_engine
from sqlalchemy import text
engine = get_engine()
with engine.connect() as conn:
    result = conn.execute(text("SELECT DISTINCT request_channel_code FROM intake_requests"))
    for row in result:
        print(row[0])
