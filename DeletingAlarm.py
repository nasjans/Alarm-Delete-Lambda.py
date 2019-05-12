from __future__ import print_function
import boto3
import logging

#Declaring variables
acid = '989062577142'
region = 'us-east-1'
name_tag = 'WebServer'
sns_topic = 'arn:aws:sns:us-east-1:989062577142:config-topic'

# Create AWS client session
ec2session = boto3.client('ec2')
cloudwatch = boto3.client('cloudwatch')

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

# Retrives instance id from cloudwatch event
def get_instance_id(event):
    print(event) 
    try:
        return event['detail']['EC2InstanceId']
    except KeyError as err:
        LOGGER.error(err)
        return False
    

def lambda_handler(event, context):

    session = boto3.session.Session()
    ec2session = session.client('ec2')
    instanceid = get_instance_id(event)
    print(instanceid)
   
    # Delete Metric "DiskSpaceUtilization"
    cloudwatch.delete_alarms(
    AlarmNames=["%s %s Disk-Space-Utilization is high" % (name_tag, instanceid)]
    )
    
    # Delete Metric "CPUUtilization"
    cloudwatch.delete_alarms(
    AlarmNames=["%s %s CPU-Utilization is high" % (name_tag, instanceid)]
    )
    
    # Delete Metric "MemoryUtilization"
    cloudwatch.delete_alarms(
    AlarmNames=["%s %s Memory-Utilization is high" % (name_tag, instanceid)]
    )
    
    # Delete Metric "StatusCheckFailed"
    cloudwatch.delete_alarms(
    AlarmNames=["%s %s Status-Check-Failed" % (name_tag, instanceid)]
    )
