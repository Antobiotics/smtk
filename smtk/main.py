import click

import smtk.utils.logger as l


@click.group()
def main(**kwargs):
    l.INFO("Starting SMTK")


if __name__ == '__main__':
    main()
