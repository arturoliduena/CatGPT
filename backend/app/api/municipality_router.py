import structlog
from fastapi import APIRouter

from app.core.supabase_con.connect import connect

_logger = structlog.get_logger()
router = APIRouter()

@router.get("/municipalities")
async def municipalities():
    _logger.info("GET /municipalities")
    conn = connect()
    cur = conn.cursor()

    cur.execute('SELECT codimuni, nommuni FROM municipalities')
    result = cur.fetchall()
    return result