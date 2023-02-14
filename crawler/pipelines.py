import socket
from urllib.parse import urlparse
from pydispatch import dispatcher
from scrapy import signals
from crawler.item_export import JsonLItemExporter


class GetDomainPipeline:
    """"Processes urls to domain names and finds ip addresses for each domain name
        example output item:
        {
        'domain': 'example.com', 'Address': 'x.x.x.x',
        'linked_to': ['x.x.x.x', 'x.x.x.x']
        }
    """

    def process_item(self, item, spider):
        item['domain'] = urlparse(item['domain']).netloc
        item['address'] = self._address_lookup(item['domain'])

        for i in range(len(item['linked_to'])):
            item['linked_to'][i] = urlparse(item['linked_to'][i]).netloc

        self._names_to_addresses(item['linked_to'])

        # convert list to set to remove duplicates
        item['linked_to'] = set(item['linked_to'])

        item['linked_to'].remove(item['address'])

        return item

    def _names_to_addresses(self, names):
        """Takes a list of names and converts them to addresses"""
        offset = 0
        for index in range(len(names)):
            i = index - offset
            names[i] = self._address_lookup(names[i])
            if names[i] is None:
                # remove addresses that could not be found
                del names[i]
                offset = offset + 1

    def _address_lookup(self, name):
        """Returns an address from a name. Returns None if no address is found."""
        try:
            return socket.gethostbyname(name)
        except socket.gaierror:
            return None


class ExportItemsPipeline:
    """Exports parsed items using JsonLItemExporter"""
    def __init__(self):
        self.file = None
        self.exporter = JsonLItemExporter()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        self.exporter.finish_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
