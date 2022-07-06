# import discord
# from discord.ext import commands

import disnake
from disnake.ext import commands

from SqlLiteWrapper import SqlLiteWrapper
from dotenv import load_dotenv

import os

from TicTacToeFuncs import move_legal, make_move, format_game_string_for_output, has_player_won

load_dotenv('.env')

class TicTacToeBot(commands.Bot):
    
    def __init__(self, *args, **kwargs):
        intents = disnake.Intents.default()
        intents.members = True 
        intents.message_content = True 

        super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=intents, *args, **kwargs)

        self.add_commands()
        self.sqlWrapper = SqlLiteWrapper()
        self.game_count = self.sqlWrapper.get_max_id() + 1

        self.run(os.getenv('discord-token'))


    async def on_ready(self):
        print("We have logged in as {}".format(self.user))


    def add_commands(self):

        @self.command(name='play', pass_context=True)
        async def play(ctx, player_to_face):
            def check(reaction, user):
                print("Reaction: ", reaction.emoji)

                return user == ctx.message.author and reaction.emoji == "✅"

            try:
                # See if the player_to_face is a valid user

                player_to_face = int(player_to_face[2:-1])
                print("Modified player_to_face: ", player_to_face)

                player_to_face = await self.fetch_user(player_to_face)
                player_to_face_id = player_to_face.id
                print("Player to face: ", player_to_face)

            except:
                response_message = "Invalid player " + player_to_face
                await ctx.send(response_message)

            else:
                # If the user is valid, ping them and verify that they want to play
                response_message = "<@" + str(player_to_face_id) + "> react to this message with ✅ to accept" 
                await ctx.send(response_message)

                reaction_response = await self.wait_for("reaction_add", check=check)
                
                if reaction_response:
                    self.sqlWrapper.add_game(self.game_count, ctx.message.author, player_to_face)

                    response_str = "ID for your game is " + str(self.game_count)

                    await ctx.send(response_str)

                    self.game_count += 1


        @self.command(name='move', pass_context=True)
        async def move(ctx, game_id, move_string):
            player_requesting = str(ctx.message.author)
            player_requesting_id = ctx.message.author.id
            current_player = self.sqlWrapper.get_current_player(game_id, move_string)
            current_game_string = self.sqlWrapper.get_game_string(game_id)
            game_active = self.sqlWrapper.is_game_active(game_id)

            if(game_active == 0):
                await ctx.send("Game is over already!")
                return

            if(player_requesting != current_player):
                await ctx.send("It is not currently your move")
                return

            move_character = ''


            # Determine which move it is based off the last character of the game string
            if(current_game_string[-1] == 'A'):
                move_character = 'x'
            else:
                move_character = 'o'

            
            if move_legal(move_string, current_game_string):
                new_game_string = make_move(move_string, current_game_string, move_character)

                self.sqlWrapper.modify_game_string(game_id, new_game_string)
                current_board = format_game_string_for_output(new_game_string)

                if(has_player_won(new_game_string, move_character)):
                    congrats_string = "You won the game " + "<@" + str(player_requesting_id) + "> ! Congrats."

                    await ctx.send(congrats_string)

                    await ctx.send("Here is the final board state: ")
                    await ctx.send(current_board)

                    self.sqlWrapper.set_game_to_inactive(game_id)

                else:
                    await ctx.send("Move successful. Here is the board currently: ")
                    await ctx.send(current_board)

            else:
                await ctx.send("Move was invalid. Try again")
            

            

