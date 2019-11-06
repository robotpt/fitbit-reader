from fitbit_reader import FitbitReader
import yaml

# You'll need to enter these with your own id and secret
# See step 1 here: https://towardsdatascience.com/collect-your-own-fitbit-data-with-python-ff145fa10873
secrets_file = 'secrets.yaml'

with open(secrets_file, 'r') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

client_id_ = data['client_id']
client_secret_ = data['client_secret']

fitbit_reader = FitbitReader(client_id_, client_secret_)
for date_ in [
    '2019-10-16'  # datetime.date(2019, 10, 16) also works
]:
    print('==============================')
    print('== Intraday steps by minute ==')
    steps = fitbit_reader.get_intraday_steps_dataframe(date_)
    print(steps)
    print('==============================')
    print('=== Total steps in the day ===')
    total_steps = fitbit_reader.get_total_steps(date_)
    print(total_steps)
    print('==============================')
    print('===   Active Steps by min  ===')
    active_steps = fitbit_reader.get_active_steps_dataframe(date_)
    print(active_steps)
    print('==============================')
    print('===   Total Active Steps   ===')
    total_active_steps = fitbit_reader.get_total_active_steps(date_)
    print(total_active_steps)
    print('==============================')
    print('===        Last Sync       ===')
    last_sync = fitbit_reader.get_last_sync()
    print(last_sync)
    print('==============================')
