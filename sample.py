import modules


def main():
    tg_name = 'kamei-test'
    modules.slack_module.send_slack_message('test')
    tg_arn = select_target_group_id(tg_name)
    instances = target_instances(tg_arn)
    for instance_id in instances:
        detach_elb(tg_arn, instance_id)
        restart_ec2_instance(instance_id)
        attach_elb(tg_arn, instance_id)


main()
