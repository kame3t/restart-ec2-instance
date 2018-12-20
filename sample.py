from modules import *


def main():
    tg_name = 'kamei-test'

    datadog_api_key = aws_parameter_store_module.get_parameters('/datadog/api_key')
    datadog_app_key = aws_parameter_store_module.get_parameters('/datadog/app_key')
    datadog_module.connect_datadog(datadog_api_key, datadog_app_key)
    slack_webhook_url = aws_parameter_store_module.get_parameters('/slack/incoming_webhook/url')
    slack_channel_name = 'biz_dev_notify'

    tg_arn = aws_restart_instance_module.get_target_group_id(tg_name)
    instances = aws_restart_instance_module.get_instances(tg_arn)
    for instance_id in instances:
        slack_module.send_slack_message('create datadog downtime: %s', instance_id, slack_webhook_url, slack_channel_name)
        downtime_id = datadog_module.get_downtime(instance_id)
        slack_module.send_slack_message('start detatch instance: %s', instance_id, slack_webhook_url, slack_channel_name)
        aws_restart_instance_module.detach_elb(tg_arn, instance_id)
        slack_module.send_slack_message('start restart instance: %s', instance_id, slack_webhook_url, slack_channel_name)
        aws_restart_instance_module.restart_ec2_instance(instance_id)
        slack_module.send_slack_message('start attach instance: %s', instance_id, slack_webhook_url, slack_channel_name)
        aws_restart_instance_module.attach_elb(tg_arn, instance_id)
        slack_module.send_slack_message('delete datadog downtime: %s', instance_id, slack_webhook_url, slack_channel_name)
        datadog_module.delete_downtime(downtime_id)
        slack_module.send_slack_message('restart instance success: %s', instance_id, slack_webhook_url, slack_channel_name)

main()
