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

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise e