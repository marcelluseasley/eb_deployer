#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This is the eb deploy application for manheim hello world app

from progress.spinner import Spinner
from subprocess import Popen, PIPE
import boto3
import os
import os.path
import time


client = boto3.client('elasticbeanstalk')

current_directory = os.getcwd()  # used as app name and environment
git_directory = os.path.join(current_directory, '.git')
eb_directory = os.path.join(current_directory, '.elasticbeanstalk')
app_name = current_directory.split('/')[-1]
environment_name = (app_name.replace('_', '-'))
solution_stack = '64bit Amazon Linux 2016.03 v2.1.3 running Python 2.7'

application_path = current_directory + '/application.py'


# test if there is a .git folder; if not, then there is no repo, so exit
if not os.path.exists(git_directory):
    print("\n==>Cannot create Elastic Beanstalk app.")
    print("==>Run 'git init' first, then tag a branch.")
    exit(1)


def get_latest_tag():
    """check for latest tag and store it for app version number"""
    p = Popen('git describe --tags --candidates 1',
              shell=True, stdin=PIPE, stdout=PIPE)

    latest_tag = p.communicate()
    if len(latest_tag) is not 2 and latest_tag[1] is not None:

        print("\n==>Error retrieving latest tag: {}\n".format(latest_tag[1]))
        return None
    return latest_tag[0].strip()


def create_eb_environment():
    """
    Create an environment for the application.
    This is where the scaling options are set (up to 3 instances),
    based on CPU utilization.
    """
    creation_response = client.create_environment(
        ApplicationName=app_name,
        EnvironmentName=environment_name,
        Description="Manheim test deployment",
        CNAMEPrefix=environment_name,
        Tier={
            'Name': 'WebServer',
            'Type': 'Standard'
        },
        SolutionStackName=solution_stack,
        OptionSettings=[
            {
                'Namespace': 'aws:autoscaling:asg',
                'OptionName': 'Custom Availability Zones',
                'ResourceName': 'AWSEBAutoScalingGroup',
                'Value': 'us-east-1a'
            },
            {
                'Namespace': 'aws:autoscaling:asg',
                'OptionName': 'MaxSize',
                'ResourceName': 'AWSEBAutoScalingGroup',
                'Value': '3'
            },
            {
                'Namespace': 'aws:autoscaling:asg',
                'OptionName': 'MinSize',
                'ResourceName': 'AWSEBAutoScalingGroup',
                'Value': '1'
            },
            {
                'Namespace': 'aws:autoscaling:launchconfiguration',
                'OptionName': 'InstanceType',
                'Value': 't2.micro'
            },
            {
                'Namespace': 'aws:autoscaling:trigger',
                'OptionName': 'BreachDuration',
                'ResourceName': 'AWSEBCloudwatchAlarmLow',
                'Value': '1'
            },
            {
                u'Namespace': 'aws:autoscaling:trigger',
                u'OptionName': 'EvaluationPeriods',
                u'ResourceName': 'AWSEBCloudwatchAlarmLow',
                u'Value': '1'
            },
            {
                u'Namespace': 'aws:autoscaling:trigger',
                u'OptionName': 'LowerBreachScaleIncrement',
                u'ResourceName': 'AWSEBAutoScalingScaleDownPolicy',
                u'Value': '-1'
            },
            {
                u'Namespace': 'aws:autoscaling:trigger',
                u'OptionName': 'LowerThreshold',
                u'ResourceName': 'AWSEBCloudwatchAlarmLow',
                u'Value': '25'
            },
            {
                'Namespace': 'aws:autoscaling:trigger',
                'OptionName': 'MeasureName',
                'ResourceName': 'AWSEBCloudwatchAlarmLow',
                'Value': 'CPUUtilization'
            },
            {
                'Namespace': 'aws:autoscaling:trigger',
                'OptionName': 'Period',
                'ResourceName': 'AWSEBCloudwatchAlarmLow',
                'Value': '1'
            },
            {
                'Namespace': 'aws:autoscaling:trigger',
                'OptionName': 'Statistic',
                'ResourceName': 'AWSEBCloudwatchAlarmLow',
                'Value': 'Average'
            },
            {
                'Namespace': 'aws:autoscaling:trigger',
                'OptionName': 'Unit',
                'ResourceName': 'AWSEBCloudwatchAlarmLow',
                'Value': 'Percent'
            },
            {
                'Namespace': 'aws:autoscaling:trigger',
                'OptionName': 'UpperBreachScaleIncrement',
                'ResourceName': 'AWSEBAutoScalingScaleUpPolicy',
                'Value': '1'
            },
            {
                'Namespace': 'aws:autoscaling:trigger',
                'OptionName': 'UpperThreshold',
                'ResourceName': 'AWSEBCloudwatchAlarmHigh',
                'Value': '85'
            },
            {
                'Namespace': 'aws:autoscaling:updatepolicy:rollingupdate',
                'OptionName': 'RollingUpdateEnabled',
                'ResourceName': 'AWSEBAutoScalingGroup',
                'Value': 'false'
            },
            {
                'Namespace': 'aws:autoscaling:updatepolicy:rollingupdate',
                'OptionName': 'RollingUpdateType',
                'ResourceName': 'AWSEBAutoScalingGroup',
                'Value': 'Time'
            },
            {
                'Namespace': 'aws:elasticbeanstalk:command',
                'OptionName': 'BatchSize',
                'Value': '50'
            },
            {
                'Namespace': 'aws:elasticbeanstalk:command',
                'OptionName': 'BatchSizeType',
                'Value': 'Percentage'
            },
            {
                'Namespace': 'aws:elasticbeanstalk:command',
                'OptionName': 'DeploymentPolicy',
                'Value': 'Rolling'
            },
            {
                'Namespace': 'aws:elasticbeanstalk:command',
                'OptionName': 'IgnoreHealthCheck',
                'Value': 'false'
            },
            {
                'Namespace': 'aws:elasticbeanstalk:command',
                'OptionName': 'Timeout',
                'Value': '600'
            },
            {
               'Namespace': 'aws:elasticbeanstalk:container:python',
               'OptionName': 'WSGIPath',
               'Value': application_path
            }
        ]
    )
    return creation_response


def initialize_app():
    """This function initializes the current directory for Elastic Beanstalk"""

    print("Initializing app (current directory) for Elastic Beanstalk...")
    proc = Popen('eb init --region="us-east-1" -p python {}'.format(app_name),
                 shell=True, stdin=PIPE, stdout=PIPE)

    resp, err = proc.communicate()
    if err is not None:
        print("\n==>Error initializing app {}.\n==>{}\n".format(app_name, err))
        exit(1)
    print("Done.")


def deploy_app():
    """This function deploys the current directory
    to the Elastic Beanstalk environment
    """

    print("Deploying app (current directory) to Elastic Beanstalk...")
    proc = Popen('eb deploy --label {} {}'.format(
                 get_latest_tag(), environment_name),
                 shell=True, stdin=PIPE, stdout=PIPE)
    resp, err = proc.communicate()
    if err is not None:
        print("\n==>Error deploying app {} to environment {}.\n==>{}\n".format(
              app_name, environment_name, err))
        exit(1)
    print(resp)
    print("Done.")


def main():
    if not os.path.exists(eb_directory):
        initialize_app()
    else:
        print("Directory already initialized for Elastic Beanstalk. Skipping.")

    # check if environment has already been created. If so, skip creation
    response = client.describe_environments(
            EnvironmentNames=[
                environment_name,
            ]
        )

    if len(response['Environments']) == 0:
        print('==> Creating environment {}'.format(environment_name))
        create_eb_environment()

    # wait for environment ready state before deploying
    environment_ready = False
    while not environment_ready:
        response = client.describe_environments(
            EnvironmentNames=[
                environment_name,
            ]
        )
        if len(response['Environments']) == 0:
            print("Environment {} does not exist.".format(environment_name))
            exit(1)
        env_status = response['Environments'][0]['Status']
        if env_status == 'Terminated':
            print('\n==>Environment is in terminated state. \
                  It could be visible up to an hour.\n')
            exit(1)

        if env_status != 'Ready':
            spinner = Spinner("Environment setup still in progress... ")
            for i in range(20):
                spinner.next()
                time.sleep(1)
        else:
            environment_ready = True

    print("Environment ready.")

    deploy_app()

if __name__ == '__main__':
    main()
