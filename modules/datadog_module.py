from os import environ
from datadog import initialize, api
import time

options = {
    'api_key': environ['datadog_api_key'],
    'app_key': environ['datadog_app_key']
}
initialize(**options)


def set_downtime(hostname, maintenance_time, tz):
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
    hostname = "api1"
    maintenance_time = 1 * 60 * 60
    timezone = 'JST'
    downtime_id = set_downtime(hostname, maintenance_time, timezone)
    delete_downtime(downtime_id)
