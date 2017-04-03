import click
from smtk.commands.cli import pass_context


@click.command('get_friends', short_help='Outputs Twitter friends for users in `--users`')
@click.option('--users', required=True,
              help="CSV list of user_ids")
@pass_context
def cli(ctx, users):
    print users

