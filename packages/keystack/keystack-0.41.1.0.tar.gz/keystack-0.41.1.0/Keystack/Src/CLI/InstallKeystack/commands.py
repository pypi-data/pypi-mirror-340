import os
import sys
import click 
import traceback

currentDir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, currentDir.replace('/Src/CLI/InstallKeystack', ''))

# TODO: Need to move Setup to /Keystack folder
#from Setup.setupKeystack import setup

"""
Keystack install/upgrade will perform the followings on the local host:
   - pip install keystack
   - docker compose up

Usage:
   keystack install setup -docker -docker_file <dockerKeystack tar file>
   keystack install upgrade -docker -docker_file <dockerKeystack tar file>
   keystack install setup -linux
   keystack install upgrade -linux
"""

'''
@click.command()
@click.option('-docker',
              required=False, default=False, is_flag=True,
              help='Install Keystack docker container. Must include param -dockerFile <docker tar file>')

@click.option('-linux',   
              required=False, default=False, is_flag=True,  
              help='The saved pipeline name to run')

@click.option('-docker_file',
              required=False, type=str, 
              help='Keystack docker tar file')

@click.command()
@click.argument('setup',
                 required=False, default=False, type=bool)

@click.argument('upgrade',
                 required=False, default=False, type=bool)
'''

# kwargs: all the above click.options in a dict
@click.command()
def setup(**kwargs):
    """ 
    Setup or wipe out existing Keystack
    """
    try:
        click.echo(f'setup: {kwargs}')
        
    except KeyboardInterrupt:
        pass
    
    except Exception as errMsg:
        pass


#kwargs: all the above click.options in a dict
@click.command()
def upgrade(**kwargs):
    """ 
    Upgrade existing Keystack
    """
    try:
        click.echo(f'upgrade: {kwargs}')
        
    except KeyboardInterrupt:
        pass
    
    except Exception as errMsg:
        pass
