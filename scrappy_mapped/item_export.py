from scrapy.exporters import BaseItemExporter
from scrapy.utils.serialize import ScrapyJSONEncoder


class JsonLItemExporter(BaseItemExporter):
    """Merges items with the same domain key before exporting them as jsonl file"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.queue = set()
        kwargs.setdefault('ensure_ascii', not self.encoding)
        self.encoder = ScrapyJSONEncoder(**kwargs)

    def export_item(self, item):
        """Merge items with same domain name into one item."""
        domain_enqueued = False
        for i in self.queue:
            if i['domain'] == item['domain']:
                domain_enqueued = True
                i['linked_to'].update(item['linked_to'])
        if not domain_enqueued:
            self.queue.add(item)

    def finish_exporting(self):
        """Save items in queue to jsonl file"""
        file = open('exported_results.jsonl', 'w')
        for item in self.queue:
            item_dict = dict(self._get_serialized_fields(item))
            data = self.encoder.encode(item_dict) + "\n"
            file.write(data)
        file.close()
