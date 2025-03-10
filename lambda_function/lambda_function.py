import boto3
import logging

# Seting up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Initializing EC2 client
    ec2 = boto3.client('ec2')

    try:
        # Fetching all snapshots owned by the account
        snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']

        # Fetching all active EC2 instances (running and stopped)
        instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'stopped']}])
        active_volumes = set()

        # Extractracting volume IDs from active instances
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                for volume in instance.get('BlockDeviceMappings', []):
                    active_volumes.add(volume['Ebs']['VolumeId'])

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise e