==============
eb_deployer
==============



Utility to deploy app to EB


* Free software: MIT license


Assumptions
--------

* The AWS ElasticBeanstalk (EB) command-line tool ()awsebcli) is installed on system (where this utility is used)
* This utility is run in an application directory that uses Git (.git folder must be present)
* At least one Git commit has been made and a tag (for EB app versioning)

        - [example]: git tag -a 1.7 -m "test tagging"

Usage
----


* In order to use the utility, clone the Git repo, then run: "python setup.py install"

        - The command line utility "eb_deploy" will then be available on your system.

* As long as the application is associated with a Git repo and has at least one tag,
it can be deployed to AWS ElasticBeanstalk.

* Subsequent calls to "eb_deploy" will upload to EB instantly with a rolling deployment of 50%.
* Application will be scaled up to 3 EC2 instances if CPU utilization reaches 85% and will be scaled down if CPU utilization reaches 25%.

