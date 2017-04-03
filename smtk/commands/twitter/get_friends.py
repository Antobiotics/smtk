import json

import click

from smtk.commands.cli import pass_context
from smtk.collect_twitter import CollectTwitter

class StdioTwitterLogger(CollectTwitter):
    def on_tweet(self, tweet):
        pass

    def on_start(self):
        pass

    def on_profile(self, profile):
        print profile

    def on_connection(self, account, connection, type_):
        edge = {
            'account': account,
            'connection': connection,
            'type_': type_
        }
        print json.dumps(edge)


@click.command('get_friends', short_help='Outputs Twitter friends for users in `--users`')
@click.option('--users', required=True,
              help="CSV list of user_ids")
@pass_context
def cli(ctx, users):
    collector = StdioTwitterLogger()
    collector.get_friends(screen_names=users.split(','))

