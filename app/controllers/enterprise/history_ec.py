'''
Enterprise controller for History objects.
'''
import sqlite3

from app.models import db_path


class HistoryEC(object):

    def get(self) -> list:
        '''
        Fetch the urls of all records in History table.
        # Returns:
            list of pattern names in history.
        '''
        with sqlite3.connect(db_path) as conn:
            history = conn.execute('SELECT * FROM History').fetchall()
            return [record[1] for record in history]

    def add(self, pat_name: str) -> None:
        '''
        Insert new History record for a given pattern name.
        # Arguements:
            pat_name: name of the viewed pattern.  
        '''
        with sqlite3.connect(db_path) as conn:
            visit_count = conn.execute('''
                SELECT visitCount FROM History
                WHERE patternName = ?''', (pat_name,)
            ).fetchone()
            visit_count = 0 if not visit_count else visit_count[0]

            conn.execute('''
                INSERT INTO History (patternName, visitCount)
                VALUES (?, ?)''', (pat_name, visit_count + 1))

    def clear(self) -> None:
        '''Drop all records for History table.'''
        with sqlite3.connect(db_path) as conn:
            conn.execute('DELETE FROM History')


history_ec = HistoryEC()
