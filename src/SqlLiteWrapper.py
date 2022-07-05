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
                                game_string TEXT NOT NULL,
                                game_active INTEGER
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
                            VALUES (?, ?, ?, ?, ?)
                        ''', (game_id, str(creator_user), str(opponent_user), "---------A", 1))

        self.conn.commit()

    
    def get_game_string(self, game_id: int) -> str:
        self.cur.execute("SELECT game_string FROM games WHERE game_id = ?", (game_id,))
        result_game: str = self.cur.fetchall()[0][0]

        return result_game


    def modify_game_string(self, game_id: int, new_game_string: str) -> None:
        self.cur.execute("UPDATE games SET game_string = ? WHERE game_id = ?", (new_game_string, game_id,))
        self.conn.commit()


    def get_creator_player(self, game_id: int):
        '''
            Returns the player that started a given game
        '''

        self.cur.execute("SELECT creator_user FROM games WHERE game_id = (?)", (game_id,))

        return self.cur.fetchone()[0]


    def get_opponent_player(self, game_id: int):
        '''
            Returns the player that was challenged 
        '''

        self.cur.execute("SELECT opponent_user FROM games WHERE game_id = (?)", (game_id,))

        return self.cur.fetchone()[0]


    def get_current_player(self, game_id: int, game_string: str):
        '''
            Returns the player whose move it currently is. 
            Every game string has at the end either A or B, which symbolizes whether it is the creating player's
            turn or the opponent's turn
        '''

        current_player = ""

        if game_string[-1] == 'A':
            current_player = self.get_creator_player(game_id)
        else:
            current_player = self.get_opponent_player(game_id)

        return current_player


    def is_game_active(self, game_id: int) -> int:
        self.cur.execute('SELECT game_active FROM games WHERE game_id=(?)', (game_id,))

        result = self.cur.fetchone()[0]

        return result


    def set_game_to_inactive(self, game_id: int) -> None:
        self.cur.execute("UPDATE games SET game_active = ? WHERE game_id = ?", (0, game_id,))
        self.conn.commit()
