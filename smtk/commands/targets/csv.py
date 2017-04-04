import json
import click

import smtk.utils.logger as l
from smtk.commands.cli import pass_context

PARSING_ERROR = "Unable to parse:\n%s \nReason: %s"
MISSING_KEY_ERROR = "Line is missing required key '%s':\n%s"

def convert(lines):
    for line in lines:
        try:
            data = json.loads(line)
        except Exception as e:
            raise Exception(PARSING_ERROR%(line, e))

        if 'type' not in data:
            raise Exception(MISSING_KEY_ERROR%('type', line))

        data_type = data['type']

        if data_type == 'RECORD':
            if 'stream' not in data:
                raise Exception(MISSING_KEY_ERROR%('stream', line))

            record = data['record']
            record_values = []
            for key in record:
                record_values.append(str(record[key]))

            print ','.join(record_values)

        else:
            l.WARN("""
                   Unexpected message type %s in message %s
                   """ %(data['type'], data))

@click.command('csv', short_help="Write JSON data to CSV")
@click.option('--config')
@pass_context
def cli(ctx, config):
    input_ = click.get_text_stream('stdin')
    convert(input_)
