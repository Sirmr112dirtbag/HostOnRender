import discord
from discord.ext import commands
import asyncio
import requests
import random
import webserver

spamming_status = {}

bot = commands.Bot(command_prefix='.', self_bot=True, help_command=None)

TOKEN = "MTI2MTMyODAzMTA3MTYwMDY4Mw.G-PBhj.k9J6DY_TOYFwT9JECfdjTNqv1EjMEqrv8UQZd0"

# Global flags to control the stop functionality
spamming_server = False
spamming_general = False
purge_in_progress = False
nuking = False
repeating = True
repeating_anywhere = True

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.command()
async def ping(ctx):
    await ctx.send('``Pong!``')


@bot.command()
async def massBan(ctx):
    guild = ctx.guild

    if guild is None:
        await ctx.send('``This command can only be used in a server guild.``')
        return

    await ctx.send('``Starting to ban all members``')

    for member in guild.members:
        if member.top_role >= ctx.author.top_role or member == ctx.author:
            print(f"skipping {member} due to higher role or being the bot itself.")
            continue
        try:
            await guild.ban(member, reason="Mass ban by self-bot")
            print(f"Banned {member}")
        except Exception as e:
            print(f"Failed to ban {member}: {e}")

    await ctx.send("``Ban process completed.``")


@bot.command()
async def grabUserAvatar(ctx, user: discord.User = None):
    # If no user is mentioned, default to the command author
    if user is None:
        user = ctx.author

    # Get the user's avatar URL
    avatar_url = user.avatar.url if user.avatar else user.default_avatar.url

    # Send the avatar URL to the current context (channel or DM)
    await ctx.send(f"{user}'s avatar: {avatar_url}")


@bot.command()
async def massDm(ctx, *, message: str):
    global spamming_general
    spamming_general = True  # Set the flag to True when starting general mass DM

    guild = ctx.guild
    if guild is None:
        await ctx.send("``This command can only be used in a guild server.``")
        return
    await ctx.send(f"``Starting to send DMs to all members with the message: {message}``")

    for member in guild.members:
        if not spamming_general:  # Check if we should stop the process
            await ctx.send("``Mass DM process has been stopped.``")
            break

        await asyncio.sleep(5)
        if member == bot.user:
            continue
        try:
            await member.send(message)
            print(f"Sent DM to {member}")
        except Exception as e:
            print(f"Failed to DM {member}: {e}")

    await ctx.send("``DM process completed.``")


@bot.command()
async def massDmStop(ctx):
    global spamming_general
    spamming_general = False  # Set the flag to False to stop general mass DM
    await ctx.send("``Mass DM process will stop shortly.``")


@bot.command()
async def massDmServer(ctx, guild_id: int, *, message: str):
    global spamming_server
    spamming_server = True  # Set the flag to True when starting mass DM

    guild = bot.get_guild(guild_id)
    if guild is None:
        await ctx.send(f"``Could not find a guild with ID {guild_id}``")
        return
    await ctx.send(f"``Starting to send DMs to all members in {guild.name} with the message: {message}``")

    for member in guild.members:
        if not spamming_server:  # Check if we should stop the process
            await ctx.send("``Mass DM Server process has been stopped.``")
            break

        await asyncio.sleep(5)
        if member == bot.user:
            continue
        try:
            await member.send(message)
            print(f"Sent DM to {member}")
            await ctx.send(f"``Sent DM to {member}``")
        except Exception as e:
            print(f"Failed to DM {member}: {e}")
            await ctx.send(f"``Failed DM to {member}: {e}``")

    await ctx.send("``DM process completed.``")


@bot.command()
async def massDmServerStop(ctx):
    global spamming_server
    spamming_server = False  # Set the flag to False to stop mass DM server
    await ctx.send("``Mass DM Server process will stop shortly.``")


@bot.command()
async def grabServerIcon(ctx):
    guild = ctx.guild
    if guild is None:
        await ctx.send("``This command can only be used in a server.``")
        return
    icon_url = guild.icon.url if guild.icon else "``This server has no icon.``"

    await ctx.send(f"{guild.name}'s icon: {icon_url}")


@bot.command()
async def grabServerBanner(ctx):
    guild = ctx.guild
    if guild is None:
        await ctx.send("``This command can only be used in a server.``")
        return
    banner_url = guild.banner.url if guild.banner else "``This server has no banner icon set.``"

    await ctx.send(f"{guild.name}'s banner: {banner_url}")


@bot.command()
async def grabServerIconById(ctx, guild_id: int):
    guild = bot.get_guild(guild_id)
    if guild is None:
        await ctx.send(f"``Could not find a server with ID {guild_id}.``")
        return
    icon_url = guild.icon.url if guild.icon else "``This server has no icon.``"
    await ctx.send(f"{guild.name}'s icon: {icon_url}")


@bot.command()
async def grabServerBannerById(ctx, guild_id: int):
    guild = bot.get_guild(guild_id)
    if guild is None:
        await ctx.send(f"``Could not find a server with ID {guild_id}.``")
        return
    banner_url = guild.banner.url if guild.banner else "``This server has no banner icon set.``"
    await ctx.send(f"{guild.name}'s banner: {banner_url}")


@bot.command()
async def grabUserAvatarById(ctx, user_id: int):
    user = bot.get_user(user_id)
    if user is None:
        await ctx.send(f"``Could not find a user with ID {user_id}")
        return
    avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
    await ctx.send(f"{user}'s avatar: {avatar_url}")


@bot.command()
async def grabUserBanner(ctx, user_id: int):
    user = bot.get_user(user_id)
    if user is None:
        await ctx.send(f"``Could not find a user with ID {user_id}")
        return
    banner_url = user.banner.url if user.banner else "``This server does not have a banner icon set.``"
    await ctx.send(f"{user}'s banner: {banner_url}")


@bot.command()
async def grabBanner(ctx, user: discord.User = None):
    # If no user is mentioned, default to the command author
    if user is None:
        user = ctx.author

    # Get the user's avatar URL
    banner_url = user.banner.url if user.banner else "``This server does not have a banner icon set.``"

    # Send the avatar URL to the current context (channel or DM)
    await ctx.send(f"{user}'s banner: {banner_url}")


@bot.command()
async def purge(ctx):
    global purge_in_progress
    purge_in_progress = True

    await ctx.send("``Starting to delete your messages. use '.stopPurge' to stop.``")

    async for message in ctx.channel.history(limit=None):
        if message.author == ctx.author:
            try:
                await message.delete()
                await asyncio.sleep(0.5)
            except Exception as e:
                await ctx.send(f"``An error occurred: {e}``")
                break
        if not purge_in_progress:
            await ctx.send("``Purge progress stopped.``")
            break
    await ctx.send("``Finished purging your messages.``" if purge_in_progress else "``purge progress was stopped``")


@bot.command()
async def purgeStop(ctx):
    global purge_in_progress

    purge_in_progress = False
    await ctx.send("``Purge progress will be stopped shortly.``")


@bot.command()
async def purgeLimit(ctx, limit: int):
    if limit <= 0:
        await ctx.send("``Please provide a positive number of messages to delete.``")
        return

    limit += 2
    await ctx.send(f"``Starting to delete your last {limit} messages.``")
    deleted = 0
    async for message in ctx.channel.history(limit=None):
        if message.author == ctx.author:
            try:
                await message.delete()
                deleted += 1
                if deleted >= limit:
                    break
                await asyncio.sleep(0.5)
            except Exception as e:
                await ctx.send(f"``an error occurred: {e}``")
                break
    await ctx.send(f"``deleted {deleted} messages.``")


@bot.command()
async def sendWebhook (ctx, webhook_url: str, *, message: str):
    try:
        if not webhook_url.startswith("https://discord.com/api/webhooks/"):
            await ctx.send("``invalid webhook URL. please provide a correct discord webhook URL``")
            return
        response = requests.post(webhook_url, json={"content":message})
        if response.status_code == 204:
            await ctx.send("``message successfully sent to the webhook.``")
        else:
            await ctx.send(f"``failed to send message. error code: {response.status_code}``")
    except Exception as e:
        await ctx.send(f"``an error occurred: {e}``")


@bot.command()
async def gore(ctx):
    await ctx.send("https://files.catbox.moe/ad011t.mp4")


@bot.command()
async def nuke(ctx, channel_name: str, *, message: str):
    global nuking
    nuking = True

    # Check if the command is used in a guild (server)
    if ctx.guild is None:
        await ctx.send("``This command can only be used in a server.``")
        return

    # Step 1: Delete all channels
    await ctx.send("``Deleting all channels...``")
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
            await asyncio.sleep(1)  # Avoid rate limit
        except discord.Forbidden:
            # Skip channels where deletion is not allowed
            print(f"Skipped deleting channel {channel.name} due to insufficient permissions.")
            continue
        except Exception as e:
            print(f"Failed to delete channel {channel.name}: {e}")
            continue

    # Step 2: Create up to 500 new channels and send the message
    # await ctx.send("Mass creating up to 500 channels and sending a message in each one...")
    created_count = 0

    while nuking and created_count < 500:
        try:
            # Create new channel
            new_channel = await ctx.guild.create_text_channel(channel_name)
            created_count += 1
            await asyncio.sleep(1)  # Avoid rate limit

            # Send the message in the newly created channel
            try:
                await new_channel.send(message)
            except Exception as e:
                print(f"Failed to send message in {new_channel.name}: {e}")

        except Exception as e:
            print(f"Failed to create channel: {e}")
            break

    # Indicate the end of the nuking process
    nuking = False
    await ctx.send(f"``Nuking completed. {created_count} channels created.``")


@bot.command()
async def nukeStop(ctx):
    global nuking
    nuking = False
    await ctx.send("``Nuking stopped.``")
    print("Nuking has been stopped.")


@bot.command()
async def deleteAllChannels(ctx):
    # Ensure the command is used within a server
    guild = ctx.guild
    if guild is None:
        await ctx.send("``This command can only be used in a guild server.``")
        return

    await ctx.send(f"``Starting to delete all channels in {guild.name}``")

    # Loop through all channels in the guild
    for channel in guild.channels:
        try:
            await channel.delete()
            print(f"Deleted channel: {channel.name}")
            # await ctx.send(f"``Deleted channel: {channel.name}``")
        except Exception as e:
            # Skip channels that cannot be deleted and log the error
            print(f"Failed to delete channel {channel.name}: {e}")
            # await ctx.send(f"``Failed to delete channel {channel.name}: {e}``")

    # await ctx.send("``Channel deletion process completed.``")


@bot.command()
async def remoteDeleteAllChannels(ctx, guild_id: int):
    # Retrieve the guild by ID
    guild = bot.get_guild(guild_id)
    if guild is None:
        await ctx.send(f"``Could not find a guild with ID {guild_id}``")
        return

    await ctx.send(f"``Starting to delete all channels in {guild.name}``")

    # Loop through all channels in the specified guild
    for channel in guild.channels:
        try:
            await channel.delete()
            print(f"Deleted channel: {channel.name}")
            await ctx.send(f"``Deleted channel: {channel.name}``")
        except Exception as e:
            # Skip channels that cannot be deleted and log the error
            print(f"Failed to delete channel {channel.name}: {e}")
            await ctx.send(f"``Failed to delete channel {channel.name}: {e}``")

    await ctx.send("``Channel deletion process completed.``")


@bot.command()
async def remoteNuke(ctx, guild_id: int, channel_name: str, *, message_to_spam: str):
    global nuking
    nuking = True

    # Get the guild by ID
    guild = bot.get_guild(guild_id)
    if guild is None:
        await ctx.send(f"``Could not find a guild with ID {guild_id}``")
        return

    await ctx.send(f"``Starting nuke in {guild.name}``")

    # Delete all existing channels
    for channel in guild.channels:
        try:
            await channel.delete()
            await ctx.send(f"``Deleted channel: {channel.name}``")
        except Exception as e:
            # Log any error if a channel can't be deleted
            print(f"Failed to delete channel {channel.name}: {e}")
            await ctx.send(f"``Failed to delete channel {channel.name}: {e}``")

    # Mass create new channels and spam the provided message
    channel_count = 0
    while nuking and channel_count < 500:  # Limit to creating 500 channels
        try:
            new_channel = await guild.create_text_channel(channel_name)
            await new_channel.send(message_to_spam)
            channel_count += 1
            print(f"Created and spammed in channel: {new_channel.name}")
            await ctx.send(f"``Created and spammed in channel: {new_channel.name}``")
        except Exception as e:
            print(f"Failed to create or spam in channel: {e}")
            await ctx.send(f"``Failed to create or spam in channel: {e}``")

        # Wait before creating the next channel
        await asyncio.sleep(2)

    await ctx.send("``Nuke process completed.``")


@bot.command()
async def remoteNukeStop(ctx):
    global nuking
    nuking = False
    await ctx.send("``Nuke process stopped.``")


import discord


@bot.command()
async def createEmbed3(ctx, title: str, color: str, *, content: str):
    # Convert the color from a hex string to a Discord Color
    try:
        embed_color = discord.Color(int(color, 16))  # Color should be in hex format, e.g., "0xff5733"
    except ValueError:
        await ctx.send("``Invalid color format. Please use a hex code like 0xff5733``")
        return

    # Create the embed
    embed = discord.Embed(title=title, description=content, color=embed_color)

    # Optional: Add more fields if desired
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_footer(text="Sent by " + ctx.author.display_name)

    # Send the embed
    await ctx.send(embed=embed)


@bot.command()
async def createEmbed(ctx, title: str, description: str, color: str = "0x3498db", image_url: str = None,
                      footer_text: str = None, thumbnail_url: str = None):
    # Create the embed object
    embed = discord.Embed(
        title=title,
        description=description,
        color=int(color, 16)  # Convert hex color to an integer
    )

    # Add an image if provided
    if image_url:
        embed.set_image(url=image_url)

    # Add a thumbnail if provided
    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)

    # Add a footer if provided
    if footer_text:
        embed.set_footer(text=footer_text)

    # Send the embed
    await ctx.send(embed=embed)


@bot.command()
async def repeat(ctx, times: int, *, message: str):
    """Repeats a message a specified number of times in the current channel."""
    for _ in range(times):
        await ctx.send(message)


@bot.command()
async def repeatAnywhere0(ctx, channel_id: int, times: int, *, message: str,):
    """Repeats a message a specified number of times in a specified channel."""
    channel = bot.get_channel(channel_id)
    if channel is None:
        await ctx.send("Invalid channel ID provided.")
        return
    for _ in range(times):
        await channel.send(message)


@bot.command()
async def repeatInfinite(ctx, message: str):
    """Repeats a message infinitely in the current channel until stopped."""
    global repeating
    repeating = True
    await ctx.send("``Started infinite repeat. Use '.repeatInfiniteStop to stop'.``")
    while repeating:
        await ctx.send(message)
        await asyncio.sleep(1)  # Add a small delay to avoid spamming too fast


@bot.command()
async def repeatInfiniteStop(ctx):
    """Stops the infinite repeat started with !repeatInfinite."""
    global repeating
    repeating = False
    await ctx.send("``Stopped infinite repeat.``")


@bot.command()
async def repeatAnywhereInfinite(ctx, channel_id: int, *, message: str):
    """Repeats a message infinitely in the specified channel until stopped."""
    global repeating_anywhere
    channel = bot.get_channel(channel_id)
    if channel is None:
        await ctx.send("Invalid channel ID provided.")
        return
    repeating_anywhere = True
    await ctx.send("``Started infinite repeat in the specified channel. Use '.repeatAnywhereInfiniteStop' to stop.``")
    while repeating_anywhere:
        await channel.send(message)
        await asyncio.sleep(1)  # Add a small delay to avoid spamming too fast


@bot.command()
async def repeatAnywhereInfiniteStop(ctx):
    """Stops the infinite repeat started with !repeatAnywhereInfinite."""
    global repeating_anywhere
    repeating_anywhere = False
    await ctx.send("``Stopped infinite repeat in the specified channel.``")


@bot.command()
async def help(ctx):
    await ctx.send("``╔═╗──────────────╔╦═╗\n║╔╬═╦══╦══╦═╗╔═╦╦╝║═╣\n║╚╣╬║║║║║║║╬╚╣║║║╬╠═║\n╚═╩═╩╩╩╩╩╩╩══╩╩═╩═╩═╝``\n"
                   "``Command Prefix: '.'``\n"
                   "``.helpNuke : Nuke Commands.``\n"
                   "``.helpFun : Fun Commands.``")


@bot.command()
async def helpNuke(ctx):
    await ctx.send("``╔═╦╗─╔╗───\n║║║╠╦╣╠╦═╗\n║║║║║║═╣╩╣\n╚╩═╩═╩╩╩═╝\n \n╔═╗──────────────╔╦═╗\n║╔╬═╦══╦══╦═╗╔═╦╦╝║═╣\n║╚╣╬║║║║║║║╬╚╣║║║╬╠═║\n╚═╩═╩╩╩╩╩╩╩══╩╩═╩═╩═╝``\n"
                   "``Nuke Commands``\n"
                   "``.nuke/.nukeStop (Ex: .nuke {channel_name} {message_to_spam}) : This command does 1. Clears out all the channels. 2. Mass create channels. 3. Spam messages in per new channel created.``\n \n"
                   "``.spam/.spamStop (Ex: .spam {message_to_spam}) : This command spams all channel - the bot got access to - with the message provided.``\n \n"
                   "``.remoteSpam/.remoteSpamStop (Ex: .remoteSpam {server_id} {message_to_spam} : This command spams all channel - the bot got access to - with the message provided. And it can be used from anywhere on discord.``\n \n"
                   "``.remoteNuke/.remoteNukeStop (Ex: .remoteNuke {server_id} {channel_name} {message_to_spam}) : This command can be used from DMs as well as outter guild servers, and does 1. Clears out all the channels. 2. Mass create channels. 3. Spam messages in per new channel created.``\n \n"
                   "``.repeat (Ex: .repeat {times} {message_to_repeat}) : This command repeats a given message a given number of times.``\n \n"
                   "``.repeatInfinite/.repeatInfiniteStop (Ex: .repeatInfinite {message_to_repeat}) : This command repeat a given message an infinite number of times, untill '.repeatInfiniteStop' is used to stop it.``\n \n"
                   "``.repeatAnywhere0 (Ex: .repeatAnywhere0 {server_id/group-chat_id/chat_id} {times} {message_to_repeat}) : This command repeats a given message a given number of times from anywhere on discord.``\n \n"
                   "``.repeatAnywhere (Ex: .repeatAnywhere {server_id} {times} {message_to_repeat} : This command repeats a given message a given number of times in all the channels of a given guild server id from anywhere on discord.)``\n \n"
                   "``.repeatAnywhereInfinite/.repeatAnywhereInfiniteStop (Ex: .repeatAnywhereInfinite {server_id/group-chat_id/chat_id} {message_to_repeat}) : This command repeats a given message an infinite number of times from anywhere on discord.``\n \n")

    await ctx.send("\n \n``.massDm/.MassDmStop (Ex: .massDm {message_to_send}) :  This command mass DM messages to all members within a guild server, untill '.massDmStop' is performed.``\n \n"
                   "``.massDmServer/.MassDmServerStop (Ex: .massDmServer {message_to_send}) : This command mass DM messages to all members within a guild server, untill '.massDmStop' is performed. And it can be used anywhere on discord.``\n \n"
                   "``.deleteAllChannels (Ex: .deleteAllChannels) : This command clears out all the channel within a guild server on which the command is performed.``\n \n"
                   "``.remoteDeleteAllChannels (Ex: .remoteDeleteAllChannels {server_id}) : This command clears out all the channel within a guild server on which the command is performed. And it can be executed from anywhere on discord``\n \n"
                   "``.sendWebhook (Ex: .sendWebhook {webhook_URL} {message_to_send}) : This command use a discord webhook to send a message``\n \n"
                   "``.purge/.purgeStop (Ex: .purge) : This command deletes all the messages sent by you at where the command is executed. You can stop it using '.purgeStop'``\n \n"
                   "``.purgeLimit (Ex: .purgeLimit {number_of_messages_to_delete}) : This command deletes a given number of messages sent by you at where the command is executed.``\n \n")

    await ctx.send("\n \n``.grabUserAvatar (Ex: .grabUserAvatar {user.mention}) : Grabs the avatar of a mentioned user.``\n \n"
                   "``.grabUserAvatarById (Ex: .grabUserAvatarById {user_ID}) : Grabs the avatar of a user by his or her ID.``\n \n"
                   "``.grabUserBanner (Ex: .grabUserBanner {user.mention}) : Grabs the banner of a mentioned user.``\n \n"
                   "``.grabUserBannerById (Ex: .grabUserBannerById {user_ID}) : Grabs the banner of a user by his or her ID.``\n \n"
                   "``.grabServerIcon (Ex: .grabServerIcon) : Grabs the server's icon from where the command is performed.``\n \n"
                   "``.grabServerIconById (Ex: .grabServerIconById {server_ID}) : Grabs the icon of a server by its ID.``\n \n"
                   "``.grabServerBanner (Ex: .grabServerBanner) : Grabs the banner of a server from where the command is performed.``\n \n"
                   "``.grabServerBannerById (Ex: .grabServerBannerById {server_ID}) : Grabs the banner of a server by its ID.``")



@bot.command()
async def helpFun(ctx):
    await ctx.send("``╔══╗─────\n║═╦╬╦╦═╦╗\n║╔╝║║║║║║\n╚╝─╚═╩╩═╝\n \n╔═╗──────────────╔╦═╗\n║╔╬═╦══╦══╦═╗╔═╦╦╝║═╣\n║╚╣╬║║║║║║║╬╚╣║║║╬╠═║\n╚═╩═╩╩╩╩╩╩╩══╩╩═╩═╩═╝``\n"
                   "``Fun Games``\n"
                   "``.hangman : Guess the country, you have 6 attempts.``\n"
                   "``More coming soon...``")


# Extended list of countries for the hangman game
countries = [
    "afghanistan", "albania", "algeria", "andorra", "angola",
    "antigua", "argentina", "armenia", "australia", "austria",
    "azerbaijan", "bahamas", "bahrain", "bangladesh", "barbados",
    "belarus", "belgium", "belize", "benin", "bhutan",
    "bolivia", "bosnia", "botswana", "brazil", "brunei",
    "bulgaria", "burkinafaso", "burundi", "cabo verde", "cambodia",
    "cameroon", "canada", "centralafricanrepublic", "chad", "chile",
    "china", "colombia", "comoros", "congo", "costa rica",
    "croatia", "cuba", "cyprus", "czech republic", "denmark",
    "djibouti", "dominica", "dominican republic", "ecuador", "egypt",
    "el salvador", "equatorialguinea", "eritrea", "estonia", "eswatini",
    "ethiopia", "fiji", "finland", "france", "gabon",
    "gambia", "georgia", "germany", "ghana", "greece",
    "grenada", "guatemala", "guinea", "guinea-bissau", "guyana",
    "haiti", "honduras", "hungary", "iceland", "india",
    "indonesia", "iran", "iraq", "ireland", "israel",
    "italy", "jamaica", "japan", "jordan", "kazakhstan",
    "kenya", "kiribati", "korea", "kyrgyzstan", "laos",
    "latvia", "lebanon", "lesotho", "liberia", "libya",
    "liechtenstein", "lithuania", "luxembourg", "madagascar", "malawi",
    "malaysia", "maldives", "mali", "malta", "marshall islands",
    "mauritania", "mauritius", "mexico", "micronesia", "moldova",
    "monaco", "mongolia", "montenegro", "morocco", "mozambique",
    "myanmar", "namibia", "nauru", "nepal", "netherlands",
    "new zealand", "nicaragua", "niger", "nigeria", "north macedonia",
    "norway", "oman", "pakistan", "palau", "panama",
    "papua new guinea", "paraguay", "peru", "philippines", "poland",
    "portugal", "qatar", "romania", "russia", "rwanda",
    "saint kitts and nevis", "saint lucia", "saint vincent and the grenadines", "samoa", "san marino",
    "sao tome and principe", "saudi arabia", "senegal", "serbia", "singapore",
    "slovakia", "slovenia", "solomon islands", "somalia", "south africa",
    "south korea", "south sudan", "spain", "sri lanka", "sudan",
    "sweden", "switzerland", "syria", "taiwan", "tajikistan",
    "tanzania", "thailand", "timor-leste", "togo", "tonga",
    "trinidad and tobago", "tunisia", "turkey", "turkmenistan", "tuvalu",
    "uganda", "ukraine", "united arab emirates", "united kingdom", "united states",
    "uruguay", "uzbekistan", "vanuatu", "vatican city", "venezuela",
    "vietnam", "yemen", "zambia", "zimbabwe"
]


# Function to start the hangman game
async def start_hangman(ctx):
    country = random.choice(countries)
    guessed_letters = []
    attempts = 6
    word_completion = "_" * len(country)

    await ctx.send("``Starting Hangman! Guess the country name. You have 6 attempts.``")

    while attempts > 0 and "_" in word_completion:
        await ctx.send(f"``Word: {word_completion}``")
        await ctx.send(f"``Attempts left: {attempts}``")
        await ctx.send("``Guess a letter (or type .stop to end the game):``")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            guess = await ctx.bot.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send("``Time's up! The game has ended.``")
            return

        if guess.content.lower() == ".stop":
            await ctx.send("``Game stopped.``")
            return

        guess = guess.content.lower()

        if len(guess) != 1 or not guess.isalpha():
            await ctx.send("``Please guess a single letter!``")
            continue

        if guess in guessed_letters:
            await ctx.send("``You've already guessed that letter!``")
            continue

        guessed_letters.append(guess)

        if guess in country:
            word_completion = ''.join(
                [letter if letter in guessed_letters else "_" for letter in country]
            )
            await ctx.send("``Good guess!``")
        else:
            attempts -= 1
            await ctx.send("``Wrong guess!``")

    if "_" not in word_completion:
        await ctx.send(f"``Congratulations! You've guessed the country: {country}!``")
    else:
        await ctx.send(f"``Game over! The country was: {country}.``")


# To run the game command in your Discord bot
@bot.command()
async def hangman(ctx):
    await start_hangman(ctx)


# Spam command to spam all channels in the current server
@bot.command()
async def spam(ctx, *, message: str):
    guild = ctx.guild
    if not guild:
        await ctx.send("``This command can only be used in a server.``")
        return

    spamming_status[guild.id] = True
    await ctx.send(f"``Spamming all channels in {guild.name} with the message: {message}``")

    while spamming_status.get(guild.id, False):
        for channel in guild.text_channels:
            try:
                await channel.send(message)
                await asyncio.sleep(2)  # Adjust delay to avoid being rate-limited
            except Exception as e:
                print(f"Failed to send message to {channel.name}: {e}")

        await asyncio.sleep(5)  # Delay before repeating to avoid overwhelming the server

    await ctx.send("``Spam has been stopped.``")

# Stop command for spam
@bot.command()
async def spamStop(ctx):
    guild = ctx.guild
    if not guild:
        await ctx.send("``This command can only be used in a server.``")
        return

    spamming_status[guild.id] = False
    await ctx.send(f"``Spam stopped in {guild.name}.``")

# Remote spam command to spam a server from anywhere using server ID
@bot.command()
async def remoteSpam(ctx, guild_id: int, *, message: str):
    guild = bot.get_guild(guild_id)
    if not guild:
        await ctx.send(f"``Could not find a server with ID {guild_id}``")
        return

    spamming_status[guild_id] = True
    await ctx.send(f"``Starting remote spam in {guild.name} with the message: {message}``")

    while spamming_status.get(guild_id, False):
        for channel in guild.text_channels:
            try:
                await channel.send(message)
                await asyncio.sleep(2)  # Adjust delay to avoid being rate-limited
            except Exception as e:
                print(f"Failed to send message to {channel.name}: {e}")

        await asyncio.sleep(5)  # Delay before repeating to avoid overwhelming the server

    await ctx.send("``Remote spam has been stopped.``")

# Stop command for remote spam
@bot.command()
async def remoteSpamStop(ctx, guild_id: int):
    if guild_id not in spamming_status:
        await ctx.send(f"``No spam was active for server ID {guild_id}``")
        return

    spamming_status[guild_id] = False
    await ctx.send(f"``Remote spam stopped in server with ID {guild_id}.``")


@bot.command()
async def repeatAnywhere(ctx, guild_id: int, repeat_count: int, *, message: str):
    guild = bot.get_guild(guild_id)
    if not guild:
        await ctx.send(f"``Could not find a server with ID {guild_id}``")
        return

    if repeat_count <= 0:
        await ctx.send("``Repeat count must be greater than zero.``")
        return

    await ctx.send(f"``Repeating the message {repeat_count} times in all channels of {guild.name}.``")

    for _ in range(repeat_count):
        for channel in guild.text_channels:
            try:
                await channel.send(message)
                await asyncio.sleep(2)  # Adjust delay to avoid rate-limiting
            except Exception as e:
                print(f"Failed to send message to {channel.name}: {e}")

        await asyncio.sleep(5)  # Delay before the next iteration to avoid overwhelming the server

    await ctx.send("``Repeat process completed.``")


webserver.keep_alive()
bot.run(TOKEN)