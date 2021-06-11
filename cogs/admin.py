import discord
import datetime
from discord.ext import commands

async def is_admin(ctx):
    committee = discord.utils.get(ctx.guild.roles, name='Committee')
    elders = discord.utils.get(ctx.guild.roles, name='DevSoc Elders')
    if committee in ctx.message.author.roles or elders in ctx.message.author.roles:
        return True
    else:
        return False

class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['admincommands'])
    @commands.check(is_admin)
    async def adminhelp(self, ctx):
        embed=discord.Embed(title="Admin Commands", description="*This dialog gives you all the admin commands for DevBot.*", color=0xe7ec11)
        embed.add_field(name=".clearchat (AMOUNT)", value="Clears a set number of messages from the chat.", inline=False)
        embed.add_field(name=".servermute @user", value="Server mutes or unmutes a user.", inline=False)
        embed.set_footer(text="Bot created by <J4Y>", icon_url="https://www.j4y.dev/botassets/j4y.gif")
        await ctx.send(embed=embed)

    #By Emi/Peter
    @commands.command()
    @commands.check(is_admin)
    async def servermute(self, ctx, user: discord.Member = None):
        if user:
            servermute = discord.utils.get(ctx.guild.roles, name='Server Muted')
            devsoc = discord.utils.get(ctx.guild.roles, name='DevSoc')
            booster = discord.utils.get(ctx.guild.roles, name='Chosen One')
            if servermute in user.roles:
                await user.remove_roles(servermute)
                await user.add_roles(devsoc)
                await ctx.send("Removed server mute!")
            else:
                for role in user.roles[1:]:
                    if role == booster:
                        continue
                    else:
                        await user.remove_roles(role)
                await user.add_roles(servermute)
                await ctx.send("Server muted!")
        else:
            await ctx.send("Please tag a user!")

    @commands.command(aliases=['cleanchat'])
    @commands.check(is_admin)
    async def clearchat(self, ctx, amount: int = 0):
        if amount <= 0:
            await ctx.send("Please enter a number between 1-24")
        elif amount > 24:
            await ctx.send("You can only clear up to 24 messages at a time")
        else:
            messages = await ctx.channel.purge(limit=amount+1)
            embed=discord.Embed(title="Chat Cleared", description=f"{amount} messages cleared from {ctx.channel.name} \n {str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}", color=0xe7ec11)
            for message in messages:
                if message.embeds:
                    embed.add_field(name=message.author.name, value="Embedded Message", inline=False)
                else:
                    embed.add_field(name=message.author.name, value=message.content, inline=False)
            embed.set_footer(text="Bot created by <J4Y>", icon_url="https://www.j4y.dev/botassets/j4y.gif")
            await self.client.botLogChannel.send(embed=embed)

            
def setup(client):
    client.add_cog(Admin(client))