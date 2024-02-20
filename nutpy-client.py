from nut2 import PyNUTClient
import configparser
import time
import logging
import os



def start_client():
    logger.info('Starting Single Simple NUT Client')
    on_battery = False
    shutdown_triggered = False

    while True:
        try:
            ups_info = client.list_vars("ups")
            #ups_power_consumption = round(int(config.get('UPS', 'UPS_POWER')) * int(ups_info["ups.load"]) / 100)
            ups_status = ups_info["ups.status"]
            ups_battery_percentage = ups_info["battery.charge"]

            if 'OL' in ups_status:
                shutdown_triggered = False
                if on_battery:
                    logger.info('Power restored')
                    on_battery = False

            elif 'OB' in ups_status:

                current_time = time.time()
                if not on_battery:
                    logger.info('Running on battery and starting the timer')
                    on_battery = True
                    start_time = current_time

                action = False

                if int(ups_battery_percentage) <= int(shutdown_percentage):
                    action = 'Battery low! Shutting down'

                if round(current_time - start_time) >= int(shutdown_time):
                    action = 'Running on battery for too long! Shutting down'

                if action:
                    if not shutdown_triggered:
                        logger.warning(action)
                        shutdown_triggered = True
                        start_shutdown_procedure()

            time.sleep(5)  # Sleep for 5 seconds before fetching UPS info again

        except Exception as e:
            oldErrorString = ''
            logger.warning(f'Not connected to NUT server: {e}')
            logger.info('Initializing NUT connection')

            nut_host = config.get('UPS', 'NUT_HOST')
            nut_port = config.get('UPS', 'NUT_PORT')
            nut_username = config.get('UPS', 'NUT_USERNAME')
            nut_password = config.get('UPS', 'NUT_PASSWORD')
            shutdown_time = config.get('UPS', 'SHUTDOWN_TIME')
            shutdown_percentage = config.get('UPS', 'SHUTDOWN_PERCENTAGE')
            while True:
                try:
                    client = PyNUTClient(host=nut_host, port=nut_port, login=nut_username, password=nut_password)
                    logger.info('Connected to NUT server')
                    break
                except Exception as e:
                    errorString = f'Could not connect to NUT server (retrying in 5 seconds): {e}'
                    if oldErrorString != errorString:
                        logger.error(errorString)
                        oldErrorString = errorString
                    time.sleep(5)


def start_shutdown_procedure():
    logger.info('Starting shutdown procedure')
    shutdown_command = config.get('UPS', 'SHUTDOWN_COMMAND')
    os.system(shutdown_command)

if __name__ == '__main__':
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logger = logging.getLogger('nut-client')
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(script_dir + '/nut-client.log')
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    config = configparser.ConfigParser()
    config.read(script_dir + '/client.conf')
    start_client()
