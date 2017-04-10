import csv
import json

import click
import singer

from pattern.web import Element, plaintext

import smtk.utils.logger as l

from smtk.commands.cli import pass_context
from smtk.google import GoogleImageCrawler

class GoogleImageMetaDataLogger(GoogleImageCrawler):

    @property
    def schema(self):
        return {
            'properties': {
                'image': {'type': 'string'},
                'link': {'type': 'string'}
            }
        }

    def build_stream_name(self, keyword):
        return "g_images__meta__%s" % (keyword)

    def on_start(self, keyword):
        l.INFO("""
               Starting GoogleImageCrawler for keyword: %s
               """ % (keyword))
        singer.write_schema(self.build_stream_name(keyword),
                            self.schema, ['image', 'link'])

    def on_entry(self, keyword, entry):
        data = {
            'image': entry['ou'],
            'link': entry['ru']
        }
        stream_name = self.build_stream_name(keyword)
        singer.write_records(stream_name, [data])

    def on_page_source(self, keyword):
        elements = (
            Element(self.page_source)
            .by_tag('div.rg_meta')
        )

        for element in elements:
            meta_data_str = plaintext(element.source)
            try:
                meta_data = json.loads(meta_data_str)
                self.on_entry(keyword, meta_data)
            except Exception as e:
                l.WARN(e)

@click.command('search_images_meta')
@click.option('--scroll_max', required=False, default=2)
@click.option('--from_file', required=False)
@click.option('--from_pipe/--not-from-pipe', default=False)
@pass_context
def cli(ctx, scroll_max, from_file, from_pipe):
    keywords = []

    if not from_file is None:
        reader = csv.reader(from_file)
        for row in reader:
            keywords.append(row[0])

    if from_pipe:
        try:
            stdin_text = (
                click
                .get_text_stream('stdin')
                .read().strip()
            ).split('\n')
            for line in stdin_text:
                keywords.append(line)
        except Exception as e:
            raise RuntimeError("Error while reading pipe: %s" % (e))

    if len(keywords) == 0:
        l.WARN("Nothing to search, got: %s" %(keywords))

    crawler = GoogleImageMetaDataLogger(keywords,
                                        scroll_max=scroll_max)
    crawler.crawl()
