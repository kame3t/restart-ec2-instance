from os import environ
from datadog import initialize, api
import time


def connect_datadog(datadog_api_key=environ['datadog_api_key'], datadog_app_key=environ['datadog_app_key']):
    options = {
        'api_key': datadog_api_key,
        'app_key': datadog_app_key
    }
    initialize(**options)


def get_downtime(hostname, maintenance_time=3600, tz='JST'):
    downtime_target = 'host:'+hostname
    start_ts = int(time.time())
    end_ts = start_ts + maintenance_time
    message = 'start restarting '+hostname
    response = api.Downtime.create(scope=downtime_target, message=message, start=start_ts, end=end_ts, timezone=tz)
    downtime_id = response['id']
    return downtime_id


def delete_downtime(downtime_id):
    api.Downtime.delete(downtime_id)
    return


def main():
    hostname = 'api1'
    connect_datadog()
    downtime_id = get_downtime(hostname)
    delete_downtime(downtime_id)
