import os
from Booking.booking import Booking

try:
    with Booking(teardown=False) as bot:

        bot.land_first_page()
        bot.fill_details()
        bot.select_cheapest_flight()
        bot.add_travellers_details()
        bot.confirm_booking()
        bot.make_payment()
        table = bot.print_ticket_summary()
        bot.print_details(table)
        
    


except Exception as e:

    if 'in PATH' in str(e):
        print(
            'You are trying to run the bot from command line \n'
            'Please add to PATH your Selenium Drivers \n'
            'Windows: \n'
            '    set PATH=%PATH%;C:path-to-your-folder \n \n'
            'Linux: \n'
            '    PATH=$PATH:/path/toyour/folder/ \n'
        )
    else:
        raise
