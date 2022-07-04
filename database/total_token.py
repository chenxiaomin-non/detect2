import sys
import database.cmc_db as cmc_db
import datetime
# import nest_asyncio
import database.result as rs
# nest_asyncio.apply()
sys.path.append('./database')


# this variable is used to store the result of the query execution
result = []


async def init_total_token_table(loop):
    # Connect to the database
    con = await cmc_db.get_connection_to_database(loop)
    # delete the table if it exists
    # create a new ones
    async with con.cursor() as cursor:
        await cursor.execute("DROP TABLE IF EXISTS total_token")
        await cursor.execute('''
            CREATE TABLE total_token (
                token_address varchar(255),
                token_name varchar(255),
                symbol varchar(255),
                chain VARCHAR(255),
                lastest_result VARCHAR(255),
                timestamp VARCHAR(255)
            )''')
        await con.commit()
    con.close()


async def init_value(loop):
    # Connect to the database
    con = await cmc_db.get_connection_to_database(loop)

    async with con.cursor() as cursor:
        await cursor.execute('''
            INSERT INTO total_token
            SELECT token_address, name, symbol, chain, NULL, NULL FROM cmc_metadata ''')
        await con.commit()
    con.close()


async def update_value(loop, lastest_result: str, token_address: str):
    # Connect to the database
    con = await cmc_db.get_connection_to_database(loop)

    async with con.cursor() as cursor:
        await cursor.execute('''
            UPDATE total_token
            SET lastest_result = %s, timestamp = %s
            WHERE token_address = %s''',
                             (lastest_result, datetime.datetime.now(), token_address))
        await con.commit()
    con.close()


async def insert_value(loop, data: dict):
    # Connect to the database
    con = await cmc_db.get_connection_to_database(loop)

    async with con.cursor() as cursor:
        await cursor.execute('''
            INSERT INTO total_token
            VALUES (%s, %s, %s, %s, %s, %s)''',
                             (data['token_address'], data['token_name'], data['symbol'], data['chain'], data['lastest_result'], datetime.datetime.now()))
        await con.commit()
    con.close()


def insert_processed_data(data: dict):
    loop = cmc_db.loop
    loop.run_until_complete(insert_value(loop, data))
    return True


async def find_by_address(loop, index: int, address: str):
    con = await cmc_db.get_connection_to_database(loop)

    async with con.cursor() as cursor:
        await cursor.execute('''
            SELECT * FROM total_token WHERE token_address = %s''', (address,))
        rs.result_bag.update_result(index, await cursor.fetchone())
        await con.commit()
    con.close()


async def find_by_name(loop, index: int, name: str):
    con = await cmc_db.get_connection_to_database(loop)

    async with con.cursor() as cursor:
        await cursor.execute('''
            SELECT * FROM total_token WHERE token_name = %s''', (name,))
        rs.result_bag.update_result(index, await cursor.fetchone())
        await con.commit()
    con.close()


async def find_by_symbol(loop, index: int, symbol: str):
    con = await cmc_db.get_connection_to_database(loop)

    async with con.cursor() as cursor:
        await cursor.execute('''
            SELECT * FROM total_token WHERE symbol = %s''', (symbol,))
        rs.result_bag.update_result(index, await cursor.fetchone())
        await con.commit()
    con.close()


def find(type: str, index: int, value: str):
    loop = cmc_db.loop
    if type == "address":
        loop.run_in_executor(None, lamda=find_by_address(loop, index, value))
    elif type == "name":
        loop.run_in_executor(None, lamda=find_by_name(loop, index, value))
    elif type == "symbol":
        loop.run_in_executor(None, lamda=find_by_symbol(loop, index, value))
    else:
        print("Invalid type")


def clear_result():
    global result
    result = []
