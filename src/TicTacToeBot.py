import discord
from discord.ext import commands

from SqlLiteWrapper import SqlLiteWrapper
from dotenv import load_dotenv
import os

load_dotenv('.env')

class TicTacToeBot(commands.Bot):
    
    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix='$', *args, **kwargs)

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
            print("Hello")

