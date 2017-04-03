import sys
import json

import codecs

import click
import singer

from pymongo import MongoClient

import smtk.utils.logger as l
from smtk.commands.cli import pass_context

def emit_state(state):
    if not state is None:
        line = json.dumps(state)
        l.INFO('Emitting state %s' %(line))
        sys.stdout.write("{}\n".format(line))
        sys.stdout.flush()

def insert_lines(collection, lines):
    state = None
    schemas = {}

    for line in lines:
        try:
            o = json.loads(line)
        except json.decoder.JSONDecodeError:
            raise Exception("Unable to parse:\n{}".format(line))

        if 'type' not in o:
            raise Exception("Line is missing required key 'type': {}".format(line))
        t = o['type']

        if t == 'RECORD':
            if 'stream' not in o:
                raise Exception("Line is missing required key 'stream': {}".format(line))
            if o['stream'] not in schemas:
                raise Exception("A record for stream {} was encountered before a corresponding schema".format(o['stream']))

            schema = schemas[o['stream']]

            record = o['record']

            collection.insert_one(record)

            state = None
        elif t == 'STATE':
            l.INFO('Setting state to %s' %(o['value']))
            state = o['value']
        elif t == 'SCHEMA':
            """
            if 'stream' not in o:
                raise Exception("Line is missing required key 'stream': {}".format(line))
            stream = o['stream']
            schemas[stream] = o['schema']
            if 'key_properties' not in o:
                raise Exception("key_properties field is required")
            key_properties[stream] = o['key_properties']
            """
        else:
            raise Exception("Unknown message type {} in message {}"
                            .format(o['type'], o))
    return state


@click.command('mongodb', short_help="Write JSON data to mongodb")
@click.option('--config')
@pass_context
def cli(ctx, config):
    client = MongoClient('localhost', 27017)
    db = client.twitter_connections
    collection = db.relationships

    input_ = codecs.getreader("utf-8")(sys.stdin)

    state = None
    state = insert_lines(collection, input_)
    emit_state(state)
