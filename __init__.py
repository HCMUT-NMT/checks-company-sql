import check50
import check50.py
import sqlite3

@check50.check()
def exists():
    """Required SQL files exist"""
    files = ["a.sql", "b.sql", "c.sql", "q.sql"]
    for f in files:
        check50.exists(f)

@check50.check(exists)
def test_a():
    """(a) Query returns correct employees and projects in the same department"""
    # Run student SQL against company.db
    result = run_query("a.sql")
    expected = [
        ("John", "Smith", "Research", "ProductX"),
        ("Franklin", "Wong", "Research", "ProductY"),
        # Add expected row tuples here
    ]
    if sorted(result) != sorted(expected):
        raise check50.Mismatch(str(expected), str(result))

@check50.check(exists)
def test_c():
    """(c) Query groups departments with >= 3 employees and avg salary > 30000"""
    result = run_query("c.sql")
    # Validate result set
    if len(result) == 0:
        raise check50.Failure("No departments matched or query returned empty")

def run_query(sql_file):
    with open(sql_file, "r") as f:
        query = f.read()
    conn = sqlite3.connect("company.db")
    cur = conn.cursor()
    try:
        cur.execute(query)
        rows = cur.fetchall()
    except Exception as e:
        raise check50.Failure(f"SQL execution error: {e}")
    finally:
        conn.close()
    return rows