"""
db.py — деректер базасымен жұмыс.
PostgreSQL қолжетімді болса — онда сақтайды.
Болмаса — leaderboard.json файлына түседі (fallback).
"""
import json
import os
from config import DB_CONFIG, LEADERBOARD_FILE

# ── psycopg2 қолжетімділігін тексеру ────────────────────────────
try:
    import psycopg2
    _PG_AVAILABLE = True
except ImportError:
    _PG_AVAILABLE = False


def _get_conn():
    if not _PG_AVAILABLE:
        return None
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception:
        return None


def init_db():
    """Кестелерді жасайды (бір рет іске қосылады)."""
    conn = _get_conn()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id   SERIAL PRIMARY KEY,
            name VARCHAR(64) UNIQUE NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS game_sessions (
            id         SERIAL PRIMARY KEY,
            player_id  INT REFERENCES players(id),
            score      INT NOT NULL,
            level      INT NOT NULL,
            played_at  TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


def save_score(name: str, score: int, level: int):
    """Нәтижені PG-ге немесе JSON-ға сақтайды."""
    # ── PostgreSQL ───────────────────────────────────────────────
    conn = _get_conn()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO players (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;",
                (name,)
            )
            cur.execute("SELECT id FROM players WHERE name=%s;", (name,))
            player_id = cur.fetchone()[0]
            cur.execute(
                "INSERT INTO game_sessions (player_id, score, level) VALUES (%s,%s,%s);",
                (player_id, score, level)
            )
            conn.commit()
            cur.close()
            conn.close()
            return
        except Exception:
            pass

    # ── JSON fallback ────────────────────────────────────────────
    board = _load_json()
    board.append({'name': name, 'score': score, 'level': level})
    board.sort(key=lambda x: x['score'], reverse=True)
    board = board[:10]
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(board, f, indent=2)


def get_top10():
    """Top 10 тізімін қайтарады."""
    conn = _get_conn()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT p.name, MAX(gs.score) AS best, MAX(gs.level) AS lvl
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                GROUP BY p.name
                ORDER BY best DESC
                LIMIT 10;
            """)
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return [{'name': r[0], 'score': r[1], 'level': r[2]} for r in rows]
        except Exception:
            pass
    return _load_json()[:10]


def get_personal_best(name: str) -> int:
    """Ойыншының жеке рекордын қайтарады."""
    conn = _get_conn()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT MAX(gs.score)
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                WHERE p.name = %s;
            """, (name,))
            row = cur.fetchone()
            cur.close()
            conn.close()
            if row and row[0]:
                return row[0]
        except Exception:
            pass
    # JSON fallback
    board = _load_json()
    for entry in board:
        if entry['name'] == name:
            return entry['score']
    return 0


def _load_json():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return []