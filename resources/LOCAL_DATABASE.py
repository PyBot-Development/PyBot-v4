import sqlite3
try: from resources import support
except: import support
from datetime import datetime
import string
con = sqlite3.connect(f'{support.path}/data/local.db')
c = con.cursor()

async def GET_GUILD_LETTERS(guild_id):
    text = "".join(string.ascii_lowercase[int(i)] for i in str(guild_id))
    return f"{str(text).upper()}_"

async def GUILD_CHECK(guild):
    c.execute(f'''CREATE TABLE IF NOT EXISTS {await GET_GUILD_LETTERS(guild.id)}users (id text, username text, admin text, banned text, ban_reason text, banned_by text, banned_date text, ban_duration text)''')
    c.execute(f'''CREATE TABLE IF NOT EXISTS {await GET_GUILD_LETTERS(guild.id)}badwords (word text, added_by text)''')
    c.execute(f'''CREATE TABLE IF NOT EXISTS {await GET_GUILD_LETTERS(guild.id)}banned_channels (id text, channel_name text, added_by text)''')
    c.execute(f'''CREATE TABLE IF NOT EXISTS {await GET_GUILD_LETTERS(guild.id)}disabled_cmds (command text, added_by text)''')

async def GET_USER(guild, user):
    u = c.execute(f'''SELECT * FROM {await GET_GUILD_LETTERS(guild.id)}users WHERE id="{user.id}"''').fetchone()
    if u is None:
        c.execute(f'INSERT INTO {await GET_GUILD_LETTERS(guild.id)}users VALUES (?, ?, "0", "0", "Null", "Null", "Null", "Null")', (user.id, str(user), ))
        con.commit()
    return c.execute(f'''SELECT * FROM {await GET_GUILD_LETTERS(guild.id)}users WHERE id="{user.id}"''').fetchone()

async def ADMIN_CHECK(guild, user):
    u = c.execute(f'''SELECT * FROM {await GET_GUILD_LETTERS(guild.id)}users WHERE id="{user.id}" AND admin="1"''').fetchone()
    return u is not None

async def BANNED_CHECK(guild, user):
    u = c.execute(f'''SELECT * FROM {await GET_GUILD_LETTERS(guild.id)}users WHERE id="{user.id}" AND banned="1"''').fetchone()
    return u is not None

async def GET_USER_DATA(guild, user):
    u = c.execute(f'''SELECT * FROM {await GET_GUILD_LETTERS(guild.id)}users WHERE id="{user.id}"''').fetchone()
    if u is None:
        return f"User {user} not found in database."
    else:
        return u

async def OP_USER(guild, user):
    u = c.execute(f'''SELECT * FROM {await GET_GUILD_LETTERS(guild.id)}users WHERE id="{user.id}"''').fetchone()
    if u is None:
        c.execute(f'INSERT INTO {await GET_GUILD_LETTERS(guild.id)}users VALUES (?, ?, "1", "0", "Null", "Null", "Null", "Null")', (user.id, str(user), ))
    else:
        c.execute(f'''UPDATE {await GET_GUILD_LETTERS(guild.id)}users SET admin="1" WHERE id="{user.id}"''')
    con.commit()
    return True

async def DEOP_USER(guild, user):
    u = c.execute(f'''SELECT * FROM {await GET_GUILD_LETTERS(guild.id)}users WHERE id="{user.id}" AND admin="1"''').fetchone()
    if u is None:
        return False
    c.execute(f'''UPDATE {await GET_GUILD_LETTERS(guild.id)}users SET admin="0" WHERE id="{user.id}"''')
    con.commit()
    return True

async def BAN_USER(guild, user, reason, author):
    u = c.execute(f'''SELECT * FROM {await GET_GUILD_LETTERS(guild.id)}users WHERE id="{user.id}"''').fetchone()
    if u is None:
        c.execute(f'INSERT INTO {await GET_GUILD_LETTERS(guild.id)}users VALUES (?, ?, "0", "1", ?, ?, ?, "Null")', (str(user.id), str(user), str(reason), str(author.mention), str(datetime.utcnow()), ))
    else:
        c.execute(f'''UPDATE {await GET_GUILD_LETTERS(guild.id)}users SET banned=?, ban_reason=?, banned_by=?, banned_date=?, ban_duration="Null" WHERE id="{user.id}"''', ("1", str(reason), str(author.mention), str(datetime.utcnow())), )
    con.commit()
    return True

async def TEMPBAN_USER(guild, user, reason, author, timestamp):
    u = c.execute(f'''SELECT * FROM {await GET_GUILD_LETTERS(guild.id)}users WHERE id="{user.id}"''').fetchone()
    if u is None:
        c.execute(f'INSERT INTO {await GET_GUILD_LETTERS(guild.id)}users VALUES (?, ?, "0", "1", ?, ?, ?, ?)', (user.id, str(user), str(reason), str(author.mention), str(datetime.utcnow()), str(timestamp)), )
    else:
        c.execute(f'''UPDATE {await GET_GUILD_LETTERS(guild.id)}users SET banned=?, ban_reason=?, banned_by=?, banned_date=?, ban_duration="{timestamp}" WHERE id="{user.id}"''', ("1", str(reason), str(author.mention), str(datetime.utcnow())), )
    con.commit()
    return True

async def UNBAN_USER(guild, user):
    u = c.execute(f'''SELECT * FROM {await GET_GUILD_LETTERS(guild.id)}users WHERE id="{user.id}" AND banned="1"''').fetchone()
    if u is None:
        return False
    c.execute(f'''UPDATE {await GET_GUILD_LETTERS(guild.id)}users SET banned="0", ban_reason="Null", banned_by="Null", banned_date="Null", ban_duration="Null" WHERE id="{user.id}"''')
    con.commit()
    return True

async def CHECK_TEMPBAN(guild, user):
    u = c.execute(f'''SELECT * FROM {await GET_GUILD_LETTERS(guild.id)}users WHERE id="{user.id}"''').fetchone()
    if (
        u is not None
        and await BANNED_CHECK(guild, user)
        and c.execute(
            f'''SELECT ban_duration FROM {await GET_GUILD_LETTERS(guild.id)}users WHERE id="{user.id}"'''
        ).fetchone()[0]
        != "Null"
    ):
        time=c.execute(f'''SELECT ban_duration FROM {await GET_GUILD_LETTERS(guild.id)}users WHERE id="{user.id}"''').fetchone()
        if int(time[0]) > int(datetime.timestamp(datetime.utcnow())):
            return True
        await UNBAN_USER(user)
    return False

async def GET_BANNED(guild):
    u = c.execute(f'''SELECT id FROM {await GET_GUILD_LETTERS(guild.id)}users WHERE banned="1"''').fetchall()
    banned = []
    u = list(u)
    for item in u:
        i = list(item)
        banned.append(i[0])
    return banned

async def GET_OPS(guild):
    u = c.execute(f'''SELECT id FROM {await GET_GUILD_LETTERS(guild.id)}users WHERE admin="1"''').fetchall()
    banned = []
    u = list(u)
    for item in u:
        i = list(item)
        banned.append(i[0])
    return banned

async def REMOVE_BADWORD(guild, word:str):
    u = c.execute(f'''SELECT * FROM {await GET_GUILD_LETTERS(guild.id)}badwords WHERE word=?''', (word.lower(), )).fetchone()
    if u is None:
        return False
    c.execute(f'''DELETE FROM {await GET_GUILD_LETTERS(guild.id)}badwords WHERE word=?''', (word.lower(), ))
    con.commit()
    return True

async def ADD_BADWORD(guild, word, author):
    u = c.execute(f'''SELECT * FROM {await GET_GUILD_LETTERS(guild.id)}badwords WHERE word=?''', (word.lower(), )).fetchone()
    if u is None:
        c.execute(f'INSERT INTO {await GET_GUILD_LETTERS(guild.id)}badwords VALUES (?, ?)', (str(word.lower()), str(author), ))
        con.commit()
        return True
    else:
        return False

async def GET_BADWORDS(guild):
    return [row[0] for row in c.execute(f"SELECT word FROM {await GET_GUILD_LETTERS(guild.id)}badwords")]

async def WHO_CREATED_BADWORD(guild, word):
    return c.execute(f"SELECT added_by FROM {await GET_GUILD_LETTERS(guild.id)}badwords WHERE word=?", (word, )).fetchone()[0]

async def REMOVE_CHANNEL(guild, channel):
    u = c.execute(f'''SELECT * FROM {await GET_GUILD_LETTERS(guild.id)}banned_channels WHERE id=?''', (str(channel.id), )).fetchone()
    if u is None:
        return False
    c.execute(f'''DELETE FROM {await GET_GUILD_LETTERS(guild.id)}banned_channels WHERE id=?''', (str(channel.id), ))
    con.commit()
    return True

async def ADD_CHANNEL(guild, channel, author):
    u = c.execute(f'''SELECT * FROM {await GET_GUILD_LETTERS(guild.id)}banned_channels WHERE id=?''', (str(channel.id), )).fetchone()
    if u is None:
        c.execute(f'INSERT INTO {await GET_GUILD_LETTERS(guild.id)}banned_channels VALUES (?, ?, ?)', (str(channel.id), str(channel), str(author), ))
        con.commit()
        return True
    else:
        return False

async def CHANNEL_CHECK(guild, channel):
    i = c.execute(f"SELECT * FROM {await GET_GUILD_LETTERS(guild.id)}banned_channels WHERE id=?", (str(channel.id), )).fetchone()
    return i != None

async def GET_ALL_ADMINS(guild):
    return c.execute(f"SELECT * FROM {await GET_GUILD_LETTERS(guild.id)}users WHERE admin='1'").fetchall()

async def GET_ALL_BANNED(guild):
    return c.execute(f"SELECT * FROM {await GET_GUILD_LETTERS(guild.id)}users WHERE banned='1'").fetchall()

async def ENABLE_COMMAND(guild, cmd:str):
    u = c.execute(f'''SELECT * FROM {await GET_GUILD_LETTERS(guild.id)}disabled_cmds WHERE command=?''', (cmd, )).fetchone()
    if u is None:
        return False
    c.execute(f'''DELETE FROM {await GET_GUILD_LETTERS(guild.id)}disabled_cmds WHERE command=?''', (cmd, ))
    con.commit()
    return True

async def DISABLE_COMMAND(guild, cmd:str, author):
    u = c.execute(f'''SELECT * FROM {await GET_GUILD_LETTERS(guild.id)}disabled_cmds WHERE command=?''', (cmd, )).fetchone()
    if u is None:
        c.execute(f'INSERT INTO {await GET_GUILD_LETTERS(guild.id)}disabled_cmds VALUES (?, ?)', (str(cmd), str(author), ))
        con.commit()
        return True
    else:
        return False

async def GET_COMMANDS(guild):
    return [row[0] for row in c.execute(f"SELECT command FROM {await GET_GUILD_LETTERS(guild.id)}disabled_cmds")]

async def COMMAND_CHECK(guild, cmd):
    cmd = str(cmd)
    u = c.execute(f'''SELECT * FROM {await GET_GUILD_LETTERS(guild.id)}disabled_cmds WHERE command=?''', (cmd, )).fetchone()
    return u is not None

async def WHO_CREATED_COMMANDS(guild, cmd:str):
    return c.execute(f"SELECT added_by FROM {await GET_GUILD_LETTERS(guild.id)}disabled_cmds WHERE command=?", (cmd, )).fetchone()[0]