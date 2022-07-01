import define

import evaluate_token.evaluate_token as evaluate_token
import json
from fastapi import FastAPI
import backup_db.init_script as backup
import database.black_list as black_list


app = FastAPI()

# validate input from user


def validate_input(token_address: str):
    if token_address is None:
        return False
    if token_address.startswith('0x') is False:
        return False
    if len(token_address) != 42:
        return False
    for i in range(2, len(token_address)):
        if token_address[i] not in '1234567890abcdefABCDEF':
            return False
    return True

def check_secret_code(secret_code: str):
    SECRET_CODE = define.SECRET_CODE
    HASH = define.HASH
    HASH.update(secret_code.encode('utf-8'))
    if HASH.digest() == SECRET_CODE:
        return True
    return False

# input: /address/0x1234567890123456789012345678901234567890

@app.get("/address/{token_address}")
async def is_scam(token_address: str):

    if validate_input(token_address) is False:
        return json.dumps({
            "status": "ERR",
            "developer_message": "Only accept ETH/BSC/BNB token address",
            "result": []
        }, indent=4)

    #
    # this code will process the data
    #

    # get the result from evaluate_token
    try:
        result = evaluate_token.evaluate_token(token_address)
    except Exception:
        return json.dumps({
            "status": "ERR",
            "developer_message": "Error when evaluating token",
            "result": []
        }, indent=4)

    # this above code just process for ETH/BSC/BNB token address
    # other platform will be processed in the future
    #

    return json.dumps({
        "status": "OK",
        "result": result
    }, indent=4)


@app.get('/name/{token_name}')
async def is_scam(token_name: str):
    for i in range(len(token_name)):
        if token_name[i] in '!#$&?':
            return json.dumps({
                "status": "ERR",
                "result": {}})
    #
    # this code will process the data
    #

    result = evaluate_token.evaluate_token(name=token_name)

    return json.dumps({
        "status": "OK",
        "result": result
    }, indent=4)


@app.get('/update/{secret_code}')
async def update_db(secret_code: str):
    if check_secret_code(secret_code) is False:
        return json.dumps({
            "status": "ERR",
            "developer_message": "Invalid secret code",
        }, indent=4)
    backup.update()
    return json.dumps({
        "status": "OK",
        "result": "update database successfully"
    }, indent=4)


@app.get('/backup/{secret_code}')
async def backup_db(secret_code: str):
    if check_secret_code(secret_code) is False:
        return json.dumps({
            "status": "ERR",
            "developer_message": "Invalid secret code",
        }, indent=4)
    backup.backup()
    return json.dumps({
        "status": "OK",
        "result": "backup database successfully"
    }, indent=4)


@app.get('/blacklist/add/{secret_code}')
async def add_blacklist(token_address: str = None, secret_code: str = None, token_name: str = None):
    if check_secret_code(secret_code) is False:
        return json.dumps({
            "status": "ERR",
            "developer_message": "Invalid secret code",
        }, indent=4)
    if token_address is None and token_name is None:
        return json.dumps({
            "status": "ERR",
            "developer_message": "Invalid token address or token name",
        }, indent=4)
    black_list.add_to_blacklist(token_address, token_name)
    return json.dumps({
        "status": "OK",
        "result": "add blacklist successfully"
    }, indent=4)

if __name__ == "__main__":
    # scheeduler hourly update/backup cmc_metadata/price table
    # from apscheduler.schedulers.blocking import BlockingScheduler
    # sched = BlockingScheduler()
    # print('start scheduler')
    # sched.add_job(backup.update, 'interval', hours=1)
    # sched.start()

    import uvicorn
    uvicorn.run(
        app, 
        host=define.IP_ADDR, 
        port=define.PORT
    )
