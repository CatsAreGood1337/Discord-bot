import requests, discord, random, asyncio, json, datetime
from discord.ext import commands
from config import settings
from discord.utils import get
from asyncio import sleep 

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(intents=intents, command_prefix = settings['prefix'])
bot.remove_command( 'help' )
text_filter = ['@everyone']

@bot.event
async def on_ready():
     while True:
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(" | *help"))
        await sleep(15)

@bot.event
async def on_member_join(member: discord.Member):
    await member.send(f'{member.mention} `Приветствуем на нашем сервере !` :cat:')

@bot.command(pass_context=True)
async def help(ctx, *, server: discord.Guild = None):	
        embed = discord.Embed(title="CatsAreGood | `bot prefix *`", color = 0x9b59b6)
        icon = str(ctx.guild.icon_url)
        embed.set_thumbnail(url=icon)
        embed.add_field( name = 'cat'.format( command_prefix = settings['prefix'] ), value = '`Random cat`')
        embed.add_field( name = 'members'.format( command_prefix = settings['prefix'] ), value = '`Member counter`' )
        embed.add_field( name = 'penis'.format( command_prefix = settings['prefix'] ), value = '`Long your penis`' )
        embed.add_field( name = 'clear'.format( command_prefix = settings['prefix'] ), value = '`Clear amount messages`' )
        embed.add_field( name = 'kick'.format( command_prefix = settings['prefix'] ), value = '`Kick member`' )
        embed.add_field( name = 'mute'.format( command_prefix = settings['prefix'] ), value = '`Give mute role`' )
        embed.add_field( name = 'info'.format( command_prefix = settings['prefix'] ), value = '`Server info`' )
        embed.add_field( name = 'userinfo'.format( command_prefix = settings['prefix'] ), value = '`Send user info`' )
        await ctx.send(embed = embed)

@bot.command()
async def members(ctx):
    await ctx.send(f':cat: Количество человек на сервере `{ctx.guild.member_count}`')

@bot.command()
async def info(ctx, *, server: discord.Guild = None):

  name = str(ctx.guild.name)
  owner = str(ctx.guild.owner)
  region = str(ctx.guild.region)
  memberCount = str(ctx.guild.member_count)
  botCount = sum(member.bot for member in ctx.guild.members)
  date_format = "%d, %m, %Y"
  create = str(ctx.guild.created_at.strftime(date_format))

  icon = str(ctx.guild.icon_url)
   
  embed = discord.Embed(
      title=name + " Информация сервера",
      color=discord.Color.purple()
    )

  embed.set_thumbnail(url=icon)
  embed.add_field(name="Создатель", value=owner, inline=True)
  embed.add_field(name="Количество Ботов", value=botCount, inline=True)
  embed.add_field(name="Регион", value=region, inline=True)
  embed.add_field(name="Количество участников", value=memberCount, inline=True)
  embed.add_field(name="Создан:", value=create, inline=True)

  await ctx.send(embed=embed)

@bot.command()
async def penis(ctx):
    penis = "8" + ("=" * random.randint(0, 25)) + "D" 
    await ctx.send(penis)

@bot.command()
async def userinfo(ctx, *, user: discord.User = None):
    if user is None:
        user = ctx.author      
    date_format = "%d, %m, %Y"
    embed = discord.Embed(color=0xdfa3ff, description=user.mention)
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Вступил на сервер", value=user.joined_at.strftime(date_format))
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    embed.add_field(name="Позиция входа на сервер", value=str(members.index(user)+1))
    embed.add_field(name="Дата регистрации", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Роли [{}]".format(len(user.roles)-1), value=role_string, inline=False)
    embed.set_footer(text='ID Пользователя: ' + str(user.id))
    return await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions( administrator = True )
async def mute(ctx, member: discord.Member = None, *, reason=None):

    guild = ctx.guild
    mute_role = discord.utils.get(ctx.guild.roles, name='mute')
   
    await member.add_roles(mute_role)
    await member.send("Вы были заглушены: " + reason)

    await ctx.send(f'{member.mention} `Вы имеете заглушение! По причине:` ' + reason)

@bot.command()
async def cat(ctx):
    response = requests.get('https://some-random-api.ml/img/cat')
    json_data = json.loads(response.text)

    embed = discord.Embed(color = 0x9b59b6, title = 'Random cat')
    embed.set_image(url = json_data['link'])
    await ctx.send(embed = embed)

@bot.command()
@commands.has_permissions( administrator = True )
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member} `Был кикнут.`')

@bot.event
async def on_message( message ):
	await bot.process_commands( message )

	msg = message.content.lower()

	if msg in text_filter:
		await message.delete()
		await message.author.send( f'{ message.author.name}, `Вы не имеете право писать` "@everyone"')

@bot.command()
@commands.has_permissions( administrator = True )
async def clear( ctx, amount : int ):
	await ctx.channel.purge( limit = amount )

@clear.error
async def clear_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.send(f'{ctx.author.mention}, `укажите аргумент`')

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(f'{ctx.author.mention}, `Вы не имеете  право использовать данную комманду !`')

@mute.error
async def mute_error(ctx, error):
	if isinstance(error, commands.MissingPermissions ):
		await ctx.send(f'{ctx.author.mention}, `Вы не имеете право использовать комманду` :no_entry_sign: `!`')

@kick.error
async def kick_error(ctx, error):
	if isinstance(error, commands.MissingPermissions ):
		await ctx.send(f'{ctx.author.mention}, `Вы не имеете право использовать комманду` :no_entry_sign: `!`')

print('Bot setup!')

bot.run(settings['token'])