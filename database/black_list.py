import nest_asyncio
import database.cmc_db as cmc_db
import sys
sys.path.append('./')
nest_asyncio.apply()


async def init_blacklist_db(loop):
    con = await cmc_db.get_connection_to_database(loop)
    async with con.cursor() as cur:
        await cur.execute('''
        CREATE TABLE IF NOT EXISTS black_list (
            token_address VARCHAR(255),
            token_name VARCHAR(255)
        )''')
        await con.commit()
    con.close()


async def add_token_to_blacklist(loop, token_address, token_name):
    con = await cmc_db.get_connection_to_database(loop)
    async with con.cursor() as cur:
        await cur.execute('''INSERT IGNORE INTO black_list (token_address, token_name) VALUES (%s, %s)''', (token_address, token_name))
        await con.commit()
    con.close()


def add_to_blacklist(token_address, name):
    cmc_db.loop.run_until_complete(init_blacklist_db(cmc_db.loop))
    cmc_db.loop.run_until_complete(
        add_token_to_blacklist(cmc_db.loop, token_address, name))
