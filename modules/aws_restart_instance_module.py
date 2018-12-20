import os
import boto3


def connect_aws_api():
    session = boto3.Session(
        aws_access_key_id=os.environ['aws_access_key_id'],
        aws_secret_access_key=os.environ['aws_secret_access_key'],
        region_name=os.environ['region_name']
    )
    ec2 = session.resource('ec2')
    elb2 = session.client('elbv2')


def get_target_group_id(tg_name):
    response = elbv2.describe_target_groups(
        Names=[tg_name]
    )
    tg_arn = response['TargetGroups'][0]['TargetGroupArn']
    return tg_arn


def get_instances(tg_arn):
    response = elbv2.describe_target_health(
        TargetGroupArn=tg_arn
    )
    instances = []
    for instance in response['TargetHealthDescriptions']:
        instances.append(instance['Target']['Id'])
    return instances


def detach_elb(tg_arn, instance_id):
    waiter = elbv2.get_waiter('target_deregistered')
    elbv2.deregister_targets(
        TargetGroupArn=tg_arn,
        Targets=[
            {
                'Id': instance_id
            }
        ]
    )
    waiter.wait(
        TargetGroupArn=tg_arn,
        Targets=[
            {
                'Id': instance_id
            }
        ]
    )
    return


def restart_ec2_instance(instance_id):
    instance = ec2.Instance(instance_id)
    instance.stop()
    instance.wait_until_stopped()
    instance.start()
    instance.wait_until_running()
    return


def attach_elb(tg_arn, instance_id):
    waiter = elbv2.get_waiter('target_in_service')
    elbv2.register_targets(
        TargetGroupArn=tg_arn,
        Targets=[
            {
                'Id': instance_id
            }
        ]
    )
    waiter.wait(
        TargetGroupArn=tg_arn,
        Targets=[
            {
                'Id': instance_id
            }
        ]
    )
    return


def main():
    tg_name = 'kamei-test'
    tg_arn = get_target_group_id(tg_name)
    instances = get_instances(tg_arn)
    for instance_id in instances:
        detach_elb(tg_arn, instance_id)
        restart_ec2_instance(instance_id)
        attach_elb(tg_arn, instance_id)

