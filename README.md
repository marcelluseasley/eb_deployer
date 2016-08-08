==============
eb_deployer
==============



.. image:: https://img.shields.io/travis/marcelluseasley/eb_deployer.svg
        :target: https://travis-ci.org/marcelluseasley/eb_deployer

.. image:: https://pyup.io/repos/github/marcelluseasley/eb_deployer/shield.svg
     :target: https://pyup.io/repos/github/marcelluseasley/eb_deployer/
     :alt: Updates


Utility to deploy app to EB


* Free software: MIT license


Assumptions
--------

* The AWS ElasticBeanstalk (EB) command-line tool is installed on system (where this utility is used)
* This utility is ran in an application directory that uses Git (.git folder must be present)
* At least one Git commit has been made and a tag (for EB app versioning)

        - [example]: git tag -a 1.7 -m "test tagging"

Usage
----


* In order to use the utility, clone the Git repo, then run: "python setup.py install"

        - The command line utility "eb_deploy" will then be available on your system.

* As long as the application is associated with a Git repo and has at least one tag,
it can be deployed to AWS ElasticBeanstalk.

