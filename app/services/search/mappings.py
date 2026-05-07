"""Per-language Elasticsearch index mappings for AzTU content types."""

# Core ES does not ship dedicated Azerbaijani / Russian analyzers without
# extra plugins, so we use `standard` for `az`/`ru` and `english` for `en`.
LANG_TO_ANALYZER = {
    "az": "standard",
    "en": "english",
    "ru": "standard",
}


def _text_mapping(analyzer: str) -> dict:
    return {
        "properties": {
            "id": {"type": "keyword"},
            "type": {"type": "keyword"},
            "lang": {"type": "keyword"},
            "title": {
                "type": "text",
                "analyzer": analyzer,
                "fields": {"raw": {"type": "keyword"}},
            },
            "snippet": {"type": "text", "analyzer": analyzer},
            "extra": {"type": "text", "analyzer": analyzer},
            "url": {"type": "keyword"},
            "image": {"type": "keyword"},
            "category_id": {"type": "integer"},
            "created_at": {"type": "date"},
            "updated_at": {"type": "date"},
        }
    }


def index_settings(analyzer: str) -> dict:
    return {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
            }
        },
        "mappings": _text_mapping(analyzer),
    }
