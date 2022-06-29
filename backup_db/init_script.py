import sys
sys.path.append('./')
import database.cmc_db as cmc_db
import database.total_token as total_token
import coin_marketcap.metadata_api as cmc_api


# init coin marketcap db
def init_cmc_db():
    loop = cmc_db.loop

    loop.run_until_complete(cmc_db.cmc_init_database(loop))
    print('Completed initial metadata table')
    loop.run_until_complete(total_token.init_total_token_table(loop))
    print('Completed initial total_token table')

    loop.run_until_complete(cmc_db.fill_to_price(loop))

    packet_of_data = cmc_api.get_active_token_metadata()
    loop.run_until_complete(cmc_db.fill_to_metadata(loop, packet_of_data))
    print('Completed filling to metadata: active token')

    packet_of_data = cmc_api.get_inactive_token_metadata()
    loop.run_until_complete(cmc_db.fill_to_metadata(loop, packet_of_data))
    print('Completed filling to metadata: inactive token')

    packet_of_data = cmc_api.get_untracked_token_metadata()
    loop.run_until_complete(cmc_db.fill_to_metadata(loop, packet_of_data))
    print('Completed filling to metadata: untracked token')

    # loop.run_until_complete(total_token.init_value(loop))

# update the coin marketcap db
def update():
    loop = cmc_db.loop
    print('************************************************************************')
    print('**              Start updating coin marketcap database                **')
    loop.run_until_complete(cmc_db.update_init(loop))
    print('**              Completed Init phase of db                            **')
    loop.run_until_complete(cmc_db.fill_to_metadata(loop, name='new_cmc_metadata'))
    print('**              Completed filling to metadata                         **')
    loop.run_until_complete(cmc_db.fill_to_price(loop, name='new_cmc_price'))
    print('**              Completed filling to price                            **')
    print('**              Completed updating coin marketcap database            **')
    loop.run_until_complete(cmc_db.change_name(loop))
    print('************************************************************************')



# init_cmc_db()