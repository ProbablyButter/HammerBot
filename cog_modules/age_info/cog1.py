import asyncio
import csv
import json
import logging
import os
import random
import re
import sys
import time
from itertools import combinations

import aiohttp
import disnake
import numpy as np
from disnake.ext import commands, tasks
from dotenv import load_dotenv

from age_player import *
from cog_modules.error_handler import error_helping
from techTreeInfo import *

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
LUKE = os.getenv("LUKE_ID")


@tasks.loop(seconds=75)
async def get_json_info():
    """
    Helper function for pulling the last AoE2 match played by BSHammer. Is looped every 75 seconds to have up-to-date json info.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get("https://aoe2.net/api/player/lastmatch?game=aoe2de&profile_id=313591") as r:
            r = await r.json(content_type=None)
            await session.close()
            return r


@tasks.loop(seconds=120)
async def get_1v1_player_json():
    """
    Helper function for pulling the top 10,000 AoE2 players' info.
    """
    async with aiohttp.ClientSession() as session2:
        async with session2.get("https://aoe2.net/api/leaderboard?game=aoe2de&leaderboard_id=3&start=1&count=10000") as r:
            r = await r.json(content_type=None)
            await session2.close()
            f = open("Leaderboard1v1PlayerData_1_10000.json", "w")
            json.dump(r, f)
            f.close()
            return r


@tasks.loop(seconds=120)
async def get_tg_player_json():
    """
    Helper function for pulling the top 10,000 AoE2 players' info.
    """
    async with aiohttp.ClientSession() as session2:
        async with session2.get("https://aoe2.net/api/leaderboard?game=aoe2de&leaderboard_id=4&start=1&count=10000") as r:
            r = await r.json(content_type=None)
            await session2.close()
            return r


@tasks.loop(seconds=120)
async def get_1v1_ew_player_json():
    """
    Helper function for pulling the top 10,000 AoE2 players' info.
    """
    async with aiohttp.ClientSession() as session2:
        async with session2.get("https://aoe2.net/api/leaderboard?game=aoe2de&leaderboard_id=13&start=1&count=10000") as r:
            r = await r.json(content_type=None)
            await session2.close()
            return r


@tasks.loop(seconds=120)
async def get_tg_ew_player_json():
    """
    Helper function for pulling the top 10,000 AoE2 players' info.
    """
    async with aiohttp.ClientSession() as session2:
        async with session2.get("https://aoe2.net/api/leaderboard?game=aoe2de&leaderboard_id=14&start=1&count=10000") as r:
            r = await r.json(content_type=None)
            await session2.close()
            return r


@tasks.loop(seconds=120)
async def get_1v1_dm_player_json():
    """
    Helper function for pulling the top 10,000 AoE2 players' info.
    """
    async with aiohttp.ClientSession() as session2:
        async with session2.get("https://aoe2.net/api/leaderboard?game=aoe2de&leaderboard_id=1&start=1&count=10000") as r:
            r = await r.json(content_type=None)
            await session2.close()
            return r


@tasks.loop(seconds=120)
async def get_tg_dm_player_json():
    """
    Helper function for pulling the top 10,000 AoE2 players' info.
    """
    async with aiohttp.ClientSession() as session2:
        async with session2.get("https://aoe2.net/api/leaderboard?game=aoe2de&leaderboard_id=1&start=1&count=10000") as r:
            r = await r.json(content_type=None)
            await session2.close()
            return r


class AgeCommands(commands.Cog):
    """Commands for age of empires calls by players."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="!rank", help="Returns player 1v1 ranking")
    async def rank1v1(self, ctx: commands.Context, arg1=None):
        """
        Command: !rank [player name (optional)]
        Returns: 1v1 & tg ranks of player
        """
        f = open("Leaderboard1v1PlayerData_1_10000.json", "r")
        response1 = json.loads(f.read())

        response = await get_1v1_player_json()
        tg_response = await get_tg_player_json()
        message = disnake.Embed(title="Rank Not Found", description=f"{arg1} Rank Not Found", color=disnake.Color.blurple())
        rankings_1v1 = response["leaderboard"]
        rankings_tg = tg_response["leaderboard"]
        rank_1v1 = "Not Found"
        rank_tg = "Not Found"

        if arg1 == None:
            for i in range(len(rankings_1v1)):
                if rankings_1v1[i]["name"] == "BSHammer":
                    rank_1v1 = rankings_1v1[i]["rating"]
                if rankings_tg[i]["name"] == "BSHammer":
                    rank_tg = rankings_tg[i]["rating"]
            message = disnake.Embed(
                title=f"BSHammer's Random Match Ranks",
                description=f"1v1: {rank_1v1}\nTG: {rank_tg}",
                color=disnake.Color.blurple(),
            )
        else:
            for i in range(len(rankings_1v1)):
                if rankings_1v1[i]["name"] == arg1:
                    rank_1v1 = rankings_1v1[i]["rating"]
                if rankings_tg[i]["name"] == arg1:
                    rank_tg = rankings_tg[i]["rating"]
            message = disnake.Embed(
                title=f"{arg1}'s Random Match Ranks",
                description=f"1v1: {rank_1v1}\nTG: {rank_tg}",
                color=disnake.Color.blurple(),
            )

        await ctx.send(embed=message)

    @commands.command(name="!rankew", help="Returns player 1v1 ranking")
    async def rankew(self, ctx: commands.Context, arg1=None):
        """
        Command: !rankew [player name (optional)]
        Returns: 1v1 & tg ew ranks of player
        """
        response = await get_1v1_ew_player_json()
        tg_response = await get_tg_ew_player_json()
        # message = disnake.Embed(title='Rank Not Found', description=f"BSHammer's Rank Not Found")
        message = disnake.Embed(title="Rank Not Found", description=f"{arg1} Rank Not Found", color=disnake.Color.blurple())
        rankings_1v1 = response["leaderboard"]
        rankings_tg = tg_response["leaderboard"]

        rank_1v1 = "Not Found"
        rank_tg = "Not Found"

        if arg1 == None:
            for i in range(len(rankings_1v1)):
                if rankings_1v1[i]["name"] == "BSHammer":
                    rank_1v1 = rankings_1v1[i]["rating"]
                if rankings_tg[i]["name"] == "BSHammer":
                    rank_tg = rankings_tg[i]["rating"]
            # message = f'BSHammer EW Ranks:\n\t1v1: {rank_1v1}\n\tTG: {rank_tg}'
            message = disnake.Embed(
                title=f"BSHammer's Empire Wars Ranks",
                description=f"1v1: {rank_1v1}\nTG: {rank_tg}",
                color=disnake.Color.blurple(),
            )
        else:
            for i in range(len(rankings_1v1)):
                if rankings_1v1[i]["name"] == arg1:
                    rank_1v1 = rankings_1v1[i]["rating"]
                if rankings_tg[i]["name"] == arg1:
                    rank_tg = rankings_tg[i]["rating"]
            # message = f'{arg1} EW Ranks:\n\t1v1: {rank_1v1}\n\tTG: {rank_tg}'
            message = disnake.Embed(
                title=f"{arg1}'s Empire Wars Ranks",
                description=f"1v1: {rank_1v1}\nTG: {rank_tg}",
                color=disnake.Color.blurple(),
            )

        await ctx.send(embed=message)

    @commands.command(name="!rankdm", help="Returns player 1v1 ranking")
    async def rankdm(self, ctx: commands.Context, arg1=None):
        """
        Command: !rankdm [player name (optional)]
        Returns: 1v1 & tg dm ranks of player
        """
        response = await get_1v1_dm_player_json()
        tg_response = await get_tg_dm_player_json()
        # message = disnake.Embed(title='Rank Not Found', description=f"BSHammer's Rank Not Found")
        message = disnake.Embed(title="Rank Not Found", description=f"{arg1} Rank Not Found", color=disnake.Color.blurple())
        rankings_1v1 = response["leaderboard"]
        rankings_tg = tg_response["leaderboard"]

        rank_1v1 = "Not Found"
        rank_tg = "Not Found"

        if arg1 == None:
            for i in range(len(rankings_1v1)):
                if rankings_1v1[i]["name"] == "BSHammer":
                    rank_1v1 = rankings_1v1[i]["rating"]
                if rankings_tg[i]["name"] == "BSHammer":
                    rank_tg = rankings_tg[i]["rating"]
            # message = f'BSHammer EW Ranks:\n\t1v1: {rank_1v1}\n\tTG: {rank_tg}'
            message = disnake.Embed(
                title=f"BSHammer's Death Match Ranks",
                description=f"1v1: {rank_1v1}\nTG: {rank_tg}",
                color=disnake.Color.blurple(),
            )
        else:
            for i in range(len(rankings_1v1)):
                if rankings_1v1[i]["name"] == arg1:
                    rank_1v1 = rankings_1v1[i]["rating"]
                if rankings_tg[i]["name"] == arg1:
                    rank_tg = rankings_tg[i]["rating"]
            # message = f'{arg1} EW Ranks:\n\t1v1: {rank_1v1}\n\tTG: {rank_tg}'
            message = disnake.Embed(
                title=f"{arg1}'s Death Match Ranks",
                description=f"1v1: {rank_1v1}\nTG: {rank_tg}",
                color=disnake.Color.blurple(),
            )

        await ctx.send(embed=message)

    @commands.command(name="!civ", help="Returns AoE2 civ tech tree information.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def civInfo(self, ctx: commands.Context, arg):
        """
        Command: !civ [civname]
        Returns: The aoe2 tech tree link for that civ.
        """

        if arg.lower() in age_civs:
            response = "https://aoe2techtree.net/#" + str(arg.lower())
            await ctx.send(response)
        else:
            message = disnake.Embed(
                title="Invalid Input",
                description="There was a problem with your input. Please check your input and try again.",
                color=disnake.Color.red(),
            )
            await ctx.send(embed=message)

    @commands.command(name="!teamciv", help="Returns a team of civs.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def teamRandomCiv(self, ctx: commands.Context, arg1=None):
        """
        Command: !teamciv
        Returns: !teamciv                       Returns 2 balanced civs
                 !teamciv [(optional) number]   Returns [number] balanced civs for a team.
        """

        def random_civ_position(position, amount, uniform_size, b1):
            # position: flank = 0, pocket = 1
            b0_values = [flankavg, pocketavg]
            result = []
            for i in range(amount):
                random_civs = []
                for i in range(uniform_size):
                    random_civs.append(age_civs[random.randint(0, 38)].title())

                total_score = 0
                for item in random_civs:
                    total_score += civ_score_dict[item][position]

                weights = []
                b0 = (-b0_values[position] + 0) * b1

                for item in random_civs:
                    p = 1 / (1 + np.exp(-(b0 + b1 * civ_score_dict[item][position])))
                    weights.append(p)
                result.append(random.choices(random_civs, weights, k=1)[0])

            return result

        if arg1 == None:
            user_arg = 2
        else:
            user_arg = int(arg1)

        if user_arg != None:
            if arg1 != None:
                user_arg = int(arg1)
            else:
                user_arg = 2
            flanksum = 0
            pocketsum = 0
            for item in civ_score_dict:
                flanksum += civ_score_dict[item][0]
                pocketsum += civ_score_dict[item][1]
            flankavg = flanksum / 39
            pocketavg = pocketsum / 39

            if (user_arg == None) or user_arg == 2:
                response = f"{random_civ_position(0, 1, 5, 2)[0]}, {random_civ_position(1, 1, 5, 2)[0]}"
            elif user_arg == 3:
                response = (
                    f"Flanks: {', '.join(random_civ_position(0, 2, 5, 2))}\nPocket: {random_civ_position(1, 1, 5, 2)[0]}"
                )
            else:
                response = f"Flanks: {', '.join(random_civ_position(0, 2, 5, 2))}\nPockets: {', '.join(random_civ_position(1, 2, 5, 2))}"
            await ctx.send(response)
        else:
            message = disnake.Embed(
                title="Invalid Input",
                description="There was a problem with your input. Please check your input and try again.",
                color=disnake.Color.red(),
            )
            await ctx.send(embed=message)

    @commands.command(name="!randomciv", help="Returns a random AoE2 civ.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def randomCiv(self, ctx: commands.Context, arg1=None, arg2=None):
        """
        Command: !randomciv [optional (number)]
        Returns: !randomciv                     returns one random civ out of the 39
                 !randomciv [number]            returns [number] of civs
                 If command caller is Luke, will only return Incas unless overridden with !randomciv [r].
        """
        error = False
        reponse = ""
        # age_civs = ['Britons', 'Byzantines', 'Celts', 'Chinese', 'Franks', 'Goths', 'Japanese', 'Mongols', 'Persians', 'Saracens', 'Teutons', 'Turks', 'Vikings', 'Aztecs', 'Huns', 'Koreans', 'Mayans', 'Spanish', 'Incas', 'Hindustanis', 'Italians', 'Magyars', 'Slavs', 'Berbers', 'Ethiopians', 'Malians', 'Portuguese', 'Burmese', 'Khmer', 'Malay', 'Vietnamese', 'Bulgarians', 'Cumans', 'Lithuanians', 'Tatars', 'Burgundians', 'Sicilians', 'Bohemians', 'Poles', 'Dravidians', 'Bengalis', 'Gurjaras']
        pocket_civs = []
        flank_civs = []
        username = ctx.message.author.id
        if str(username) == str(LUKE):
            if arg1 != None and arg1.isnumeric():
                for i in range(int(arg1)):
                    if i == 0:
                        response = "Incas"
                    else:
                        response += "\n" + "Incas"
            elif arg1 != None and arg1 == "r":
                if arg2 == None:
                    response = random.choice(age_civs)
                elif arg2.isnumeric():
                    for i in range(int(arg2)):
                        if i == 0:
                            response = random.choice(age_civs).title()
                        else:
                            response += "\n" + random.choice(age_civs).title()
            elif arg2 != None and arg2.isnumeric():
                for i in range(int(arg2)):
                    if i == 0:
                        response = "Incas"
                    else:
                        response += "\n" + "Incas"
            else:
                response = "Incas"
        elif arg1 == None:
            response = random.choice(age_civs).title()
        elif arg1 == "Lucas" or arg1 == "Luke" or arg1 == "divas" or arg1 == "Divas":
            response = "Incas"
        elif arg1.isnumeric():
            for i in range(int(arg1)):
                if i == 0:
                    response = random.choice(age_civs).title()
                else:
                    response += "\n" + random.choice(age_civs).title()
        else:
            error = True
            message = disnake.Embed(
                title="Invalid Input",
                description="There was a problem with your input. Please check your input and try again.",
                color=disnake.Color.red(),
            )

        if error == True:
            await ctx.send(embed=message)
        else:
            await ctx.send(response)

    @commands.command(
        name="!whichciv",
        aliases=["!which", "!wc"],
        help="Returns which civ has the stated technology(ies)."
        "Encapsulate technology inside double-quotes if you aren't getting what you're looking for.",
    )
    async def civTech(self, ctx: commands.Context, *args):
        """
        Command: !whichciv [technology1 (+technology)] [(optional)technology2] [(optional)technology3] [(optional)technology4] [(optional)technology5]
        Returns: A list of civs that have that technology.
                 !whichciv [tech1+tech2]            returns all civs that have those techs (allows to search for multiple techs)
                 !whichciv [tech1]                  returns all civs that have that tech
                 !whichciv [techpart1] [techpart2]  returns all civs with that tech (accounts for spaces in tech name)
        """
        TITLE = "Invalid Input"
        DESCRIPTION = "There was a problem with your input. Please check your input and try again."
        message = (
            disnake.Embed(
                title=TITLE,
                description=DESCRIPTION,
                color=disnake.Color.red(),
            )
            if not args
            else None
        )
        error = False if not message else True
        if error:
            await ctx.send(embed=message)
        if len(args) >= error_helping.MAX_USER_INPUT_WORD_LENGTH:
            message = disnake.Embed(
                title=f"Input is longer than accepted",
                description=f"acceptable amount = {error_helping.MAX_USER_INPUT_WORD_LENGTH}",
                color=disnake.Color.red(),
            )
            await ctx.send(embed=message)
        else:
            responses = {}
            technologies = [re.sub(r"[^\w]", " ", tech).strip().title() for tech in args]
            if " ".join(technologies) not in techTreeDict.keys():
                for r in range(1, len(technologies) + 1):
                    for permutation in combinations(technologies, r):
                        tech = " ".join(permutation).strip()
                        try:
                            responses[tech] = techTreeDict[tech]
                        except:
                            continue
            else:
                tech = " ".join(technologies)
                responses[tech] = techTreeDict[tech]
            techs = ", ".join(responses.keys())
            civs = list(set.intersection(*map(set, list(responses.values()))))
            civs.sort()
            civs = ", ".join(civs)
            if len(civs) < 1:
                civs = f"Sorry there are no civs with the unit(s): {techs}"
            message = disnake.Embed(
                title=f"{techs} are found in the following civ(s)", description=f"{civs}", color=disnake.Color.green()
            )
            await ctx.send(embed=message)

    @commands.command(name="!does", aliases=["!do", "!doeshave"], help="Returns if a civ(s) has a technology.")
    async def techTree(self, ctx: commands.Context, arg1, arg2, arg3=None, arg4=None, arg5=None):
        """
        Command: !does [civName] [techName]
        Returns: !does [civ] [tech]                     returns whether the civ has the tech
                 !does [civ1+civ2] [tech]               returns whether the civs have the tech
                 !does [civ] [techpart1] [techpart2]    returns whether the civ has the tech
        """
        error = False
        if arg1.lower() in age_civs:
            if arg5 is not None:
                arg2 = arg2.title() + " " + arg3.title() + " " + arg4.title() + " " + arg5.title()
            elif arg4 is not None:
                arg2 = arg2.title() + " " + arg3.title() + " " + arg4.title()
            elif arg3 is not None:
                arg2 = arg2.title() + " " + arg3.title()

            bool = arg1.title() in techTreeDict[arg2.title()]

            if bool:
                response = arg1.title() + " have " + arg2.title()
            elif not bool:
                response = arg1.title() + " do not have " + arg2.title()
            else:
                response = f"Error!"
        elif "+" in arg1:
            arg1 = arg1.split("+")

            if arg5 is not None:
                arg2 = arg2.title() + " " + arg3.title() + " " + arg4.title() + " " + arg5.title()
            elif arg4 is not None:
                arg2 = arg2.title() + " " + arg3.title() + " " + arg4.title()
            elif arg3 is not None:
                arg2 = arg2.title() + " " + arg3.title()

            if len(arg1) > 0:
                for i in range(len(arg1)):
                    if arg1[i].lower() in age_civs:
                        bool = arg1[i].title() in techTreeDict[arg2.title()]
                        if bool:
                            if i == 0:
                                response = arg1[i].title() + " have " + arg2.title()
                            else:
                                response += "\n" + arg1[i].title() + " have " + arg2.title()
                        elif not bool:
                            if i == 0:
                                response = arg1[0].title() + " do not have " + arg2.title()
                            else:
                                response += "\n" + arg1[i].title() + " do not have " + arg2.title()
                        else:
                            response = f"Error!"
            else:
                error = True
                message = disnake.Embed(
                    title="Invalid Input",
                    description="There was a problem with your input. Please check your input and try again.",
                    color=disnake.Color.red(),
                )
        else:
            error = True
            message = disnake.Embed(
                title="Invalid Input",
                description="There was a problem with your input. Please check your input and try again.",
                color=disnake.Color.red(),
            )

        if error == True:
            await ctx.send(embed=message)
        else:
            await ctx.send(response)

    @commands.command(name="!match", aliases=["!game"], help="Returns BSHammer's current match information")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def match(self, ctx: commands.Context, arg1=None):
        """
        Command: !match
        Returns: Both teams, each player has a color, civ, and ELOs, also returns map, game type, and server.
        """
        if arg1 == None:
            resp = await get_json_info()
            lastmatch = resp["last_match"]
            players = []
            team1 = []
            team2 = []
            hammerTeam1 = False
            hammerTeam2 = False
            team1players = ""
            team2players = ""
            response = None
            server = lastmatch["server"]

            players = await getPlayerIDs(resp)

            for player in players:
                await player.info()
                if player.team == 1:
                    team1.append(player)
                elif player.team == 2:
                    team2.append(player)

            count = len(players)
            i = 0
            if (player.game == "1v1 Empire Wars") or (player.game == "Team Empire Wars"):
                for i in range(count // 2):
                    player1 = team1[i]
                    if i == 0:
                        team1players = f"{player1.color} {player1.name} [{player1.country} {player1.ew_tg_rating} {player1.ew_rating}] as {player1.civ} "
                    else:
                        team1players += f"{player1.color} {player1.name} [{player1.country} {player1.ew_tg_rating} {player1.ew_rating}] as {player1.civ} "
                    player2 = team2[i]
                    if i == 0:
                        team2players = f"{player2.color} {player2.name} [{player2.country} {player2.ew_tg_rating} {player2.ew_rating}] as {player2.civ} "
                    else:
                        team2players += f"{player2.color} {player2.name} [{player2.country} {player2.ew_tg_rating} {player2.ew_rating}] as {player2.civ} "
                response = f"{team1players}-- VS -- {team2players}playing {player1.game} on {player1.map}\nServer: {server}"
            else:
                for i in range(count // 2):
                    player1 = team1[i]
                    if i == 0:
                        team1players = f"{player1.color} {player1.name} [{player1.country} {player1.tg_rating} {player1.rating}] as {player1.civ} "
                    else:
                        team1players += f"{player1.color} {player1.name} [{player1.country} {player1.tg_rating} {player1.rating}] as {player1.civ} "
                    player2 = team2[i]
                    if i == 0:
                        team2players = f"{player2.color} {player2.name} [{player2.country} {player2.tg_rating} {player2.rating}] as {player2.civ} "
                    else:
                        team2players += f"{player2.color} {player2.name} [{player2.country} {player2.tg_rating} {player2.rating}] as {player2.civ} "
                response = f"{team1players}-- VS -- {team2players}playing {player1.game} on {player1.map}\nServer: {server}"
            await ctx.send(response)
        else:
            response = disnake.Embed(
                title="Invalid Input",
                description="There was a problem with your input. Please check your input and try again.",
                color=disnake.Color.red(),
            )
            await ctx.send(embed=response)


get_json_info.start()
get_1v1_player_json.start()
get_tg_player_json.start()
get_1v1_ew_player_json.start()
get_tg_ew_player_json.start()


def setup(bot: commands.Bot):
    bot.add_cog(AgeCommands(bot))
