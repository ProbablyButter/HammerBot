import os

import disnake
from disnake.ext import commands, tasks
from dotenv import load_dotenv


class ServiceCommands(commands.Cog):
    """Commands for bot services such as help or whatever."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="!help", aliases=["!commands", "!command", "!commandlist"])
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def helpUser(self, ctx: commands.Context):
        """
        Command: !help
        Returns: An embed of all the commands and how to call them.
        """
        embed = disnake.Embed(title="Commands", description="Command Help", color=0xD5D341)
        embed.add_field(name="11", value="[`11`], Returns AoE2 taunt #11.", inline=True)
        embed.add_field(name="13", value="[`13`], Returns AoE2 taunt #13.", inline=True)
        embed.add_field(name="14", value="[`14`], Returns AoE2 taunt #14", inline=True)
        embed.add_field(name="30", value="[`30`], Returns AoE2 taunt #30.", inline=True)
        embed.add_field(name="age?", value="[`age?`], Returns 'Well, duh.'", inline=True)
        embed.add_field(name="!randomciv", value="[`!randomciv <number>`], Returns random Aoe2 civ(s).", inline=True)
        embed.add_field(name="!teamciv", value="[`!teamciv <number>`], Returns a team of Aoe2 civ(s).", inline=True)
        embed.add_field(name="!civ", value="[`!civ <civName>`], Returns AoE2 civ tech tree information.", inline=True)
        embed.add_field(
            name="!does",
            value="[`!does civName<+civNames> <techName>`], Returns information about if a civ(s) has a technology.",
            inline=True,
        )
        embed.add_field(name="!match", value="[`!match`], Returns information about BSHammer's current game.", inline=True)
        embed.add_field(
            name="!rank",
            value="[`!rank <playerName>`], Returns information about BSHammer's or PlayerName's RM ranks.",
            inline=True,
        )
        embed.add_field(
            name="!rankew",
            value="[`!rankew <playerName>`], Returns information about BSHammer's or PlayerName's EW ranks.",
            inline=True,
        )
        embed.add_field(
            name="!rankdm",
            value="[`!rankdm <playerName>`], Returns information about BSHammer's or PlayerName's DM ranks.",
            inline=True,
        )
        embed.add_field(
            name="!unit", value="[`!unit <letter>`], Returns a list of units starting with a single letter.", inline=True
        )
        embed.add_field(
            name="!tech",
            value="[`!tech <letter>`], Returns a list of researchable techs starting with a single letter.",
            inline=True,
        )
        embed.add_field(
            name="!buildings",
            value="[`!buildings <letter>`], Returns a list of buildings starting with a single letter.",
            inline=True,
        )
        embed.add_field(
            name="!stats",
            value="[`!stats <unitName>`], Returns basic information about the unit.",
            inline=True,
        )
        embed.add_field(
            name="!advstats",
            value="[`!advstats <unitName>`], Returns advanced information about the unit.",
            inline=True,
        )
        embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="!contributors")
    async def contribute(self, ctx: commands.Context):
        """
        Command: !contributors
        Returns: An embed of the list of contributors to HammerBot.
        """
        embed = disnake.Embed(title="HammerBot Contributors", description="List of HammerBot Contributors", color=0xD5D341)
        embed.add_field(name="BSHammer", value="\u200b", inline=True)
        embed.add_field(name="quela", value="\u200b", inline=True)
        embed.add_field(name="harristotle", value="\u200b", inline=True)
        embed.add_field(name="Rangebro", value="\u200b", inline=True)
        embed.add_field(name="Brandyn", value="\u200b", inline=True)
        embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="!is")
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def techTreeRedirect(self, ctx: commands.Context):
        """
        Command: !is
        Returns: Redirects user to the !does command due to renaming.
        """
        response = "Please use !does instead."
        await ctx.send(response)


def setup(bot: commands.Bot):
    bot.add_cog(ServiceCommands(bot))
