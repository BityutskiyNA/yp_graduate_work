from elasticsearch import Elasticsearch
from helpers import backoff

if __name__ == "__main__":

    @backoff()
    def connect_to_elastic():
        es_client = Elasticsearch(
            hosts="http://elasticsearch:9200", validate_cert=False, use_ssl=False
        )

        return es_client
