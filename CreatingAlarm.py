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

def get_asg_name(event):
    try:
        return event['detail']['AutoScalingGroupName']
    except KeyError as err:
        LOGGER.error(err)
        return False
               

def lambda_handler(event, context):

    session = boto3.session.Session()
    ec2session = session.client('ec2')
    ec2 = boto3.resource('ec2')
    instanceid = get_instance_id(event)
    asgname = get_asg_name(event)
    print(instanceid)

        
   
    # Create Metric "DiskSpaceUtilization"
    cloudwatch.put_metric_alarm(
    AlarmName="%s %s Disk-Space-Utilization is high" % (name_tag, instanceid),
    AlarmDescription='DiskSpaceUtilization Greater than 95% for 1 Minute',
    ActionsEnabled=True,
    AlarmActions=[
        sns_topic,
    #    "arn:aws:automate:%s:ec2:terminate" % region
    ],
    MetricName='DiskSpaceUtilization',
    Namespace='System/Linux',
    Statistic='Average',
    Period=300,
    EvaluationPeriods=1,
    Threshold=70,
    ComparisonOperator='GreaterThanOrEqualToThreshold',
     
    Dimensions =[{'Name': 'MountPath', 'Value': '/'},
                #{'Name': 'Namespace', 'Value': 'System/Linux'},
                 {'Name': 'Filesystem', 'Value':'/dev/xvda1'},
                #{'Name': 'AutoScalingGroupName', 'Value': asgname},
                #{'Name': 'InstanceName', 'Value': 'CodeDeploy_ASG'},
                 {'Name': 'InstanceId', 'Value': instanceid}]
    
    )
    
    # Create Metric "MemoryUtilization"
    cloudwatch.put_metric_alarm(
    AlarmName="%s %s Memory-Utilization is high" % (name_tag, instanceid),
    AlarmDescription='Memory-Utilization Greater than 95% for 1 Minute',
    ActionsEnabled=True,
    AlarmActions=[
        sns_topic,
    #    "arn:aws:automate:%s:ec2:terminate" % region
    ],
    MetricName='MemoryUtilization',
    Namespace='System/Linux',
    Statistic='Average',
    Period=300,
    EvaluationPeriods=1,
    Threshold=50,
    ComparisonOperator='GreaterThanOrEqualToThreshold',
     
    Dimensions =[{'Name': 'InstanceId', 'Value': instanceid}]
                #{'Name': 'MountPath', 'Value': '/'},
                #{'Name': 'Namespace', 'Value': 'System/Linux'},
                #{'Name': 'Filesystem', 'Value':'/dev/xvda1'},
                #{'Name': 'AutoScalingGroupName', 'Value': asgname},
                #{'Name': 'InstanceName', 'Value': 'CodeDeploy_ASG'},
                 
    )
    
    
    
     # Create Metric "CPUUtilization"
    cloudwatch.put_metric_alarm(
    AlarmName="%s %s CPU-Utilization is high" % (name_tag, instanceid),
    AlarmDescription='CPU-Utilization Greater than 95% for 1 Minute',
    ActionsEnabled=True,
    AlarmActions=[
        sns_topic,
    #    "arn:aws:automate:%s:ec2:terminate" % region
    ],
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Statistic='Average',
    Period=300,
    EvaluationPeriods=1,
    Threshold=25,
    ComparisonOperator='GreaterThanOrEqualToThreshold',
     
    Dimensions =[{'Name': 'InstanceId', 'Value': instanceid}]
                #{'Name': 'MountPath', 'Value': '/'},
                #{'Name': 'Namespace', 'Value': 'System/Linux'},
                #{'Name': 'Filesystem', 'Value':'/dev/xvda1'},
                #{'Name': 'AutoScalingGroupName', 'Value': asgname},
                #{'Name': 'InstanceName', 'Value': 'CodeDeploy_ASG'},
                 
    )
    
    
    # Create Metric "StatusCheckFailed"
    cloudwatch.put_metric_alarm(
    AlarmName="%s %s Status-Check-Failed" % (name_tag, instanceid),
    AlarmDescription='StatusCheckFailed',
    ActionsEnabled=True,
    AlarmActions=[
        sns_topic,
    #    "arn:aws:automate:%s:ec2:terminate" % region
    ],
    MetricName='StatusCheckFailed',
    Namespace='AWS/EC2',
    Statistic='Average',
    Period=300,
    EvaluationPeriods=1,
    Threshold=1,
    ComparisonOperator='GreaterThanOrEqualToThreshold',
     
    Dimensions =[{'Name': 'InstanceId', 'Value': instanceid}]
                #{'Name': 'MountPath', 'Value': '/'},
                #{'Name': 'Namespace', 'Value': 'System/Linux'},
                #{'Name': 'Filesystem', 'Value':'/dev/xvda1'},
                #{'Name': 'AutoScalingGroupName', 'Value': asgname},
                #{'Name': 'InstanceName', 'Value': 'CodeDeploy_ASG'},
                 
    )
