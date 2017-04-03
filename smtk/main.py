import click

import smtk.utils.logger as l

from smtk.commands.cli import TwitterCommand

@click.group()
def main(**kwargs):
    l.INFO("Starting SMTK")

@main.command(cls=TwitterCommand)
def twitter():
    l.INFO("Twitter Command Detected")

if __name__ == '__main__':
    main()
