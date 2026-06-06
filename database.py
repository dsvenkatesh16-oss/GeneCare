import sqlite3

def save_report(name, risk, disease):

    conn = sqlite3.connect("gencare.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO reports
        (name, risk, disease)

        VALUES (?, ?, ?)
        """,
        (name, risk, disease)
    )

    conn.commit()
    conn.close()


def get_reports():

    conn = sqlite3.connect("gencare.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM reports
        ORDER BY id DESC
        """
    )

    reports = cursor.fetchall()

    conn.close()

    return reports


def get_analytics():

    conn = sqlite3.connect("gencare.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM reports")
    total_reports = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM reports WHERE risk='Low'"
    )
    low_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM reports WHERE risk='Medium'"
    )
    medium_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM reports WHERE risk='High'"
    )
    high_count = cursor.fetchone()[0]

    conn.close()

    return (
        total_reports,
        low_count,
        medium_count,
        high_count
    )