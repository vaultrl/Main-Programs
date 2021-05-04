import discord
from discord.ext import commands, tasks
import datetime as dt
import time
from fuzzywuzzy import fuzz, process
import asyncio
import yaml

client = commands.Bot(command_prefix = "--")
client.remove_command("help")

TOKEN = "INSERT BOT TOKEN"
bot_ids = [INSERT BOT APP ID, INSERT BOT CLIENT ID]
linkFilter = ["images-ext-2.discordapp.net/external/6oBpB-YkSMvaSGOEUyGbGXvS0jTrt-Jl_QCC9_RDdaM/https/giant.gfycat.com/TartAdolescentBird.mp4", "gfycat.com/hotterrificfritillarybutterfly"]
blacklist0 = ["nigger", "coon", "faggot", "nigga", "niggers", "nibba", "n1gg3r", "fag00t", "niggervirus", "fag", "N1gger","N1gg3r","Nigg3r","Fag00t","Fag0ot","Fago0t", "N1gga","Fagsucker", "Niggerdog", "Nlgger", "nig", "niggy", "nibby", "nigtard", "nigg", "niggg", "niggerr", "niger" ]
blacklist1 = ["fuck", "shit", "bitch", "penis", "fucking", "motherfucker", "retard", "fucked", "retarded", "bitches", "retards", "cucked", "whores", "pussy", "dumbass", "slut", "tranny", "fucker", "bitch", "beaner", "shitty", "b1tch", "cock", "hentai", "cum", "cunt", "shat", "whore", "bastard", "shithole", "porn", "boobs", "dogshit", "fuckboy", "cumrag", "cocksucker", "shiteater", "shiteating", "Dogfucker","Lolifucker","D0gshit","C0cksucker","Sh1teater","Sh1teating","L0lifucker","L0l1fucker","Lol1fucker","Cumbag","Shitbag","Sh1tbag","Sh1t","Fuuck","Fuuuck","Fuuuuck","Shitbag ","Sh1tbag","Shitter","Sh1tter","R3tard","Motherfucker","M0th3rfucker","Moth3rfucker","Wh0re","Wh0r3","Whor3","Henta1","Hental","Shlteater","Shlteating","C0ck","Cocksucker","cockeater","C0cksucker","C0cksucker","C0ckeater","B1tch","Bltch",]
logging_channel = INSERT LOG CHANNEL ID
nickChannel = INSERT NICKNAME LOG CHANNEL ID
reportChannel = INSERT REPORT LOG CHANNEL ID
mutedRole = INSERT MUTED ROLE ID
confidenceThreshold = 93
allowedWords = ["tycoon", "racoon", "barracoon", "cacoon", "carcoon", "cocoon", "cocooned","cocoonery", "cocooneries", "cocooning", "cocoons", "racoons", "tycoon", "tycoons", "tycoonate", "niger"]

@client.event
async def on_connect():
    print("Connecting to Discord...")

@client.event
async def on_ready():
    print("Bot ready")
    print(f"Logged in as {client.user.name}#{client.user.discriminator}")
    print(f"Watching {len(client.guilds)} server(s)")
    print("-------------------------------------------------")
    


@client.command(brief="Brings up this command", usage="(command)", help="Use this command to get detailed info on any command or general info if left blank.")
async def help(ctx, cmd=None):
    try:
        embed = discord.Embed(title="Help Command", color=0x34a4eb)
        embed.add_field(name="Key", value="() - Optional\n[] - Required")
        embed.add_field(name="⠀",value="Commands", inline=False)
        prfx = await client.get_prefix(ctx)
        if cmd is None:
            for command in client.commands:
                embed.add_field(name=f"{prfx}{command.name} {command.usage}", value=f"{command.brief}", inline=False)

            await ctx.channel.send(embed=embed)
            return

        for command in client.commands:
            if cmd == command.name:
                embed = discord.Embed(title=f"", color=0x34a4eb)
                embed.set_author(name="Key: () - Optional | [] - Required")
                embed.add_field(name=f"{prfx}{command.name} {command.usage}", value=f"{command.help}")
                await ctx.channel.send(embed=embed)
                return
        embed = discord.Embed(title="", color=0x34a4eb)
        embed.set_author(name=f"Error, no command called {cmd} found.")
        await ctx.channel.send(embed=embed)
        return
    except Exception as e:
        print(e)
        user = await client.fetch_user(744318685061185588)
        message = await user.send(f"An error has occurred. ```{e}```\nCTX```{ctx}```")
        print("Error message sent to jacob")

@client.command(brief="Sends a request to change you nickname", usage="[nickname]", help="Sends a nickname request to moderators to approve or deny. If approved your nickanme changes to what you requested.")
async def nick(ctx, *, nick=""):
    try:
        if nick == "":
            await ctx.channel.send(f"<@{ctx.author.id}> You need to choose a nick.")
        if len(nick) > 32 :
            await ctx.channel.send(f"<@{ctx.author.id}> Your nick is too long. Please choose a nick that is 32 characters or fewer.")
            return

        embed = discord.Embed(title="Nick Request", color=0x34a4eb)
        embed.add_field(name="User Requesting", value=f"<@{ctx.author.id}>", inline=True)
        embed.add_field(name="Requested Name", value=f"{nick}")
        fTime = dt.datetime.utcnow().strftime("%H:%M")
        embed.set_footer(text=f"Requested at: {fTime} • User ID: {ctx.author.id}")
        channel = client.get_channel(nickChannel)
        message = await channel.send(embed=embed)

        await ctx.message.delete()
        await message.add_reaction("✅")
        await message.add_reaction("❌")

        embed = discord.Embed(title="", color=0x34a4eb)
        embed.add_field(name="Nick Request Sent", value="Your request was sent, please wait for a moderator to approve.")
        response = await ctx.channel.send(embed=embed)
        await response.delete(delay=5)
        return
    except Exception as e:
        print(e)
        user = await client.fetch_user(744318685061185588)
        message = await user.send(f"An error has occurred. ```{e}```\nCTX```{ctx}```")
        print("Error message sent to jacob")

@client.command(brief="Reports a user", usage="[member]", help="Sends a report to moderators to review. You can submit a reason as well as evidence for the moderators.")
async def report(ctx, member:discord.Member=None):
    try:
        await ctx.message.delete()
        if ctx.message.author == member:
            selfMsg = await ctx.channel.send("You cannot report yourself!")
            await selfMsg.delete(delay=5)
            return
        if member == None:
            noMember = await ctx.channel.send("You need to choose who to report")
            await noMember.delete(delay=5)
            return


        reasonMsg = await ctx.channel.send("Why are you reporting this user?")
        def check(m):
            return m.author == ctx.author
        try:
            reason = await client.wait_for("message", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await reasonMsg.delete()
            timeOutMsg = await ctx.channel.send("Timed out, report deleted.")
            await timetimeOutMsg.delete(delay=5)
        await reasonMsg.delete()
        await reason.delete()

        evidenceMsg = await ctx.channel.send("If you have evidence send it now, otherwise type 'No'")
        def check(m):
            return m.author == ctx.author
        try:
            evidence = await client.wait_for("message",timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await evidenceMsg.delete()
            timeOutMsg = await ctx.channel.send("Timed out, report deleted.")
            await timeOutMsg.delete(delay=5)
            return
        await evidenceMsg.delete()
        await evidence.delete()
        if evidence.content.lower() == "no" or evidence.content.lower() == "n":
            evidence.content = "None"


        embed = discord.Embed(title="", color=0x34a4eb)
        embed.add_field(name="Report Succesfully Submitted", value="Please wait for a moderator to review it")
        successMsg = await ctx.channel.send(embed=embed)
        await successMsg.delete(delay=10)

        channel = client.get_channel(reportChannel)
        embed = discord.Embed(title="User Report", color=0x34a4eb)
        embed.add_field(name="Reporter", value=f"<@{ctx.author.id}>", inline=True)
        embed.add_field(name="Reporter Nick", value=f"{ctx.author.display_name}")
        embed.add_field(name="Reporter ID", value=f"{ctx.author.id}")
        embed.add_field(name="Reported User", value=f"<@{member.id}>")
        embed.add_field(name="Reported User Nick", value=f"{member.display_name}")
        embed.add_field(name="Reported User ID", value=f"{member.id}")
        embed.add_field(name="Reason For Report", value=f"{reason.content}")
        embed.add_field(name="Evidence For Report", value=f"{evidence.content}")
        embed.add_field(name="Chat Link", value=f"{ctx.message.jump_url}")
        fTime = dt.datetime.utcnow().strftime("%H:%M")
        embed.set_footer(text=f"Reported at {fTime}")
        message = await channel.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")
    except Exception as e:
        print(e)
        user = await client.fetch_user(744318685061185588)
        message = await user.send(f"An error has occurred. ```{e}```\nCTX```{ctx}```")
        print("Error message sent to jacob")

@report.error
async def report_error(ctx, error):
    try:
        if isinstance(error, commands.MemberNotFound):
            errorMsg = await ctx.send("No such member found.")
            await ctx.message.delete()
            await errorMsg.delete(delay=10)
    except Exception as e:
        print(e)
        user = await client.fetch_user(744318685061185588)
        message = await user.send(f"An error has occurred. ```{e}```\nCTX```{ctx}```")
        print("Error message sent to jacob")

@client.event
async def on_message(ctx):
    try:
        if ctx.author.id in bot_ids:
            return
        if ctx.channel.id == logging_channel:
            return

        linkText = str(ctx.content).replace("https://","").replace("http://","").replace("www.","")
        links = linkText.split(" ")
        text = str(ctx.content).replace(".","").replace(",","").replace("!","").replace("?","").lower()
        words = text.split(" ")

    
    
        for word in links:
            for link in linkFilter: #link filter
                try:
                    if word[-1] == "/":
                        word = word[0:-1]
                except:
                    pass
                if word.replace("https://","").replace("http://","").replace("www.","") == link:
                    await ctx.delete()


                    embed = discord.Embed(title="", color=0xff1c1c)
                    embed.add_field(name="User", value=f"<@{ctx.author.id}>", inline=True)
                    embed.add_field(name="User ID", value=f"{ctx.author.id}", inline=True)
                    embed.add_field(name="Link Detected", value=f"{link}", inline=False)
                    embed.add_field(name="Message Content", value=f"{str(ctx.content)}", inline=True)
                    embed.set_thumbnail(url=ctx.author.avatar_url)

                    channel = client.get_channel(logging_channel)
                    try:
                        await channel.send(embed=embed)
                    except Exception as e:
                        pass

                    messageSent = await ctx.channel.send(f"<@{ctx.author.id}> You cannot say that! :rage:")
                    await messageSent.delete(delay=5)

                    return
       
        for word in words: #starts the loop to check each word                 
            allowedChannels = []
            
            for swearWord in blacklist0: #starts the loop to check the slurs

                confidence = fuzz.token_set_ratio(word, swearWord) 
            
                if confidence >= confidenceThreshold:
                    await ctx.delete()


                    embed = discord.Embed(title="", color=0xff1c1c)
                    embed.add_field(name=":wastebasket:", value=f"**Message sent by <@{ctx.author.id}> deleted in <#{ctx.channel.id}>**\n{ctx.content}", inline=False)
                    embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
                    embed.add_field(name="Confidence", value=f"{confidence}% sure")
                    embed.add_field(name="Word Detected", value=f"{swearWord}")
                    now = dt.datetime.utcnow()

                    fTime = now.strftime("%H:%M")
                    embed.set_footer(text=f"Message ID:{ctx.id} • Today at {fTime} • User ID:{ctx.author.id}")
                    channel = client.get_channel(logging_channel)

                    await channel.send(embed=embed)

                    messageSent = await ctx.channel.send(f"<@{ctx.author.id}> You cannot say that! :rage:")
                    await messageSent.delete(delay=5)
                    return

            if ctx.channel.id in allowedChannels:
                await client.process_commands(ctx)
                return

            for swearWord in blacklist1: #starts the loop to check swears
                confidence = fuzz.token_set_ratio(word, swearWord)
                if swearWord in word:
                    confidence = 100
                if confidence >= confidenceThreshold:
                
                    await ctx.delete()
                    try:
                        user = client.get_user_info(ctx.author.id)
                        await client.send_message(user, f"You can not say that word :rage:!")
                    except Exception as e:
                        pass

                    embed = discord.Embed(title="", color=0xff1c1c)
                    embed.add_field(name=":wastebasket:", value=f"**Message sent by <@{ctx.author.id}> deleted in <#{ctx.channel.id}>**\n{ctx.content}", inline=False)
                    embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
                    embed.add_field(name="Confidence", value=f"{confidence}% sure")
                    embed.add_field(name="Word Detected", value=f"{swearWord}")
                    now = dt.datetime.utcnow()

                    fTime = now.strftime("%H:%M")
                    embed.set_footer(text=f"Message ID:{ctx.id} • Today at {fTime} • User ID:{ctx.author.id}")
                    channel = client.get_channel(logging_channel)

                    await channel.send(embed=embed)

                    messageSent = await ctx.channel.send(f"<@{ctx.author.id}> You cannot say that! :rage:")
                    await messageSent.delete(delay=5)
                    return
    
        await client.process_commands(ctx)
        return
    except Exception as e:
        print(e)
        user = await client.fetch_user(744318685061185588)
        message = await user.send(f"An error has occurred. ```{e}```\nCTX```{ctx}```")
        print("Error message sent to jacob")

@client.event
async def on_reaction_add(reaction, user):
    try:
        if user.id in bot_ids:
            return

        if reaction.message.author.id not in bot_ids:
            return
    
        title = reaction.message.embeds[0].title

        if title == "Nick Request":

            user = await client.get_guild(reaction.message.guild.id).fetch_member(int(str(reaction.message.embeds[0].fields[0].value).replace("<@","").replace(">","")))
            requested_name = str(reaction.message.embeds[0].fields[1].value)

            if reaction.emoji == "✅":
                await user.edit(reason="Requested Nick Change", nick=requested_name)
                await user.send("Your nickname was reviewed and approved.")
                await reaction.message.delete()
            if reaction.emoji == "❌":
                await reaction.message.delete()
    
        if title == "User Report":

            if reaction.emoji == "✅":
                reportingUser = await client.get_guild(reaction.message.guild.id).fetch_member(int(str(reaction.message.embeds[0].fields[2].value).replace("<@","").replace(">","")))
                reportedUser = await client.get_guild(reaction.message.guild.id).fetch_member(int(str(reaction.message.embeds[0].fields[5].value).replace("<@","").replace(">","")))
                role = client.get_guild(reaction.message.guild.id).get_role(mutedRole)
                await reportedUser.add_roles(role, reason="Report Accepted")
                try:
                    await reportingUser.send("Thank you for reporting. Your report was reviewed and approved.")
                except:
                    pass
                await reaction.message.delete()
            if reaction.emoji == "❌":
                await reaction.message.delete()
            

            return
    except Exception as e:
        print(e)
        user = await client.fetch_user(744318685061185588)
        message = await user.send(f"An error has occurred. ```{e}```\nREACTION```{reaction}```USER```{user}```")
        print("Error message sent to jacob")

client.run(TOKEN)
