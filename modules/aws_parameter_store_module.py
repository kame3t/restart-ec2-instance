import boto3


# Function for get_parameters
def get_parameters(param_key, region_name='ap-northeast-1'):
    ssm = boto3.client('ssm', region_name=region_name)
    response = ssm.get_parameters(
        Names=[
            param_key,
        ],
        WithDecryption=True
    )
    return response['Parameters'][0]['Value']


def main():

    # parameter name
    param_key = "RDS-MASTER-PASSWORD"

    # get parameter value
    param_value = get_parameters(param_key)
    print(param_value)


if __name__ == '__main__':
    main()
