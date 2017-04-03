import csv

import click
import singer

import smtk.utils.logger as l
from smtk.commands.cli import pass_context
from smtk.collect_twitter import CollectTwitter

class GetFriendsLogger(CollectTwitter):
    @property
    def schema(self):
        return {
            'properties': {
                'account': {'type': 'string'},
                'connection': {'type': 'string'},
                'type_': {'type': 'string'}
            }
        }

    def on_tweet(self, tweet):
        pass

    def on_start(self):
        singer.write_schema('get_friends', self.schema)

    def on_profile(self, profile):
        print profile

    def on_connection(self, account, connection, type_):
        edge = {
            'account': account,
            'connection': connection,
            'type_': type_
        }
        singer.write_records('get_friends', [edge])


@click.command('get_friends', short_help='Outputs Twitter friends for users in `--users`')
@click.option('--users', required=False,
              help="CSV list of user_ids")
@click.option('--input_data', type=click.File('rb'))
@pass_context
def cli(ctx, users, input_data):
    collector = GetFriendsLogger()
    screen_names = []

    if not users is None:
        screen_names = users.split(',')
    elif not input_data is None:
        reader = csv.reader(input_data)
        for row in reader:
            screen_names.append(row[0])

    l.INFO("Getting user relationship for users: %s" %(screen_names))
    collector.get_friends(screen_names=screen_names)
