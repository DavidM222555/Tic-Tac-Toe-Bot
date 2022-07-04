import sqlite3
    

class SqlLiteWrapper():

    def __init__(self):
        self.conn = sqlite3.connect('game.db')
        self.cur = self.conn.cursor()

        self.cur.execute('''CREATE TABLE IF NOT EXISTS 
                    games   (
                                game_id INTEGER PRIMARY KEY,
                                creator_user TEXT NOT NULL,
                                opponent_user TEXT NOT NULL,
                                game_string TEXT NOT NULL
                            )
                        ''')

    def get_max_id(self) -> int:

        # First test whether or not the database is empty
        empty_db_test = '''SELECT COUNT(game_id) FROM games'''

        self.cur.execute(empty_db_test)
        db_size = self.cur.fetchone()[0]

        if(db_size == 0):
            return 0

        # If the database is non-empty then we select the maximum id in the table -- typically
        # it should work out that this is equivalent to the count but just to safe guard against accidental placements
        command_str =   '''SELECT MAX(game_id) FROM games;''' 

        self.cur.execute(command_str)
        max_id: int = self.cur.fetchone()[0]

        return max_id


    def add_game(self, game_id: int, creator_user: str, opponent_user: str) -> None:

        self.cur.execute('''INSERT INTO games
                            VALUES (?, ?, ?, ?)
                        ''', (game_id, str(creator_user), str(opponent_user), "---------"))

        self.conn.commit()

    
    def get_game_string(self, game_id: int) -> str:
        self.cur.execute("SELECT game_string FROM games WHERE game_id = ?", (game_id,))
        result_game: str = self.cur.fetchall()[0][0]

        return result_game


    def modify_game_string(self, game_id: int, new_game_string: str) -> None:
        self.cur.execute("UPDATE games SET game_string = ? WHERE game_id = ?", (new_game_string, game_id,))
        self.conn.commit()

    