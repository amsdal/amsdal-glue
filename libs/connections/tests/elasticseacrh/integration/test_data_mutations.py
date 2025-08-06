from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.mutations.data import InsertData

from amsdal_glue_connections.elasticsearch_connection.sync_connection import ElasticsearchConnection

from ..testcases.data_mutations import delete_customer
from ..testcases.data_mutations import insert_customers_and_orders
from ..testcases.data_mutations import simple_customer_insert
from ..testcases.data_mutations import update_two_customers


def _get_all_docs(connection: ElasticsearchConnection, index_name: str) -> list[dict]:
    """Helper function to get all documents from an Elasticsearch index."""
    try:
        full_index = connection._build_index(index_name)  # noqa: SLF001
        response = connection.connection.search(index=full_index, body={'query': {'match_all': {}}, 'size': 1000})
        docs = [hit['_source'] for hit in response['hits']['hits']]
        # Sort in Python instead of Elasticsearch to avoid fielddata issues
        return sorted(docs, key=lambda x: x.get('id', ''))
    except Exception:  # noqa: BLE001
        return []


def test_insert(database_connection: ElasticsearchConnection) -> None:
    simple_customer_insert(database_connection)

    docs = _get_all_docs(database_connection, 'customers')
    assert len(docs) == 1
    assert docs[0]['id'] == '1'
    assert docs[0]['name'] == 'customer'


def test_insert_multiple(database_connection: ElasticsearchConnection) -> None:
    insert_customers_and_orders(database_connection)

    customer_docs = _get_all_docs(database_connection, 'customers')
    assert len(customer_docs) == 2

    # Sort by id for consistent comparison
    customer_docs.sort(key=lambda x: x['id'])
    assert customer_docs[0]['id'] == '1'
    assert customer_docs[0]['name'] == 'customer'
    assert customer_docs[1]['id'] == '2'
    assert customer_docs[1]['name'] == 'customer'
    assert customer_docs[1]['age'] == 25

    order_docs = _get_all_docs(database_connection, 'orders')
    assert len(order_docs) == 1
    assert order_docs[0]['id'] == '1'
    assert order_docs[0]['customer_id'] == '1'
    assert order_docs[0]['amount'] == 100


def test_update(database_connection: ElasticsearchConnection) -> None:
    update_two_customers(database_connection)

    docs = _get_all_docs(database_connection, 'customers')
    assert len(docs) == 1
    assert docs[0]['id'] == '1'
    assert docs[0]['name'] == 'new_customer'


def test_delete(database_connection: ElasticsearchConnection) -> None:
    database_connection.run_mutations([
        InsertData(
            schema=SchemaReference(name='customers', version=Version.LATEST),
            data=[
                Data(
                    data={'id': '1', 'name': 'customer'},
                ),
                Data(
                    data={'id': '2', 'name': 'customer', 'age': 25},
                ),
                Data(
                    data={'id': '3', 'name': 'customer', 'age': 30},
                ),
            ],
        ),
    ])

    docs = _get_all_docs(database_connection, 'customers')
    assert len(docs) == 3

    delete_customer(database_connection)

    docs = _get_all_docs(database_connection, 'customers')
    # Should have deleted documents with age < 27, so only id=1 (no age) and id=3 (age=30) remain
    assert len(docs) == 2
    doc_ids = [doc['id'] for doc in docs]
    assert '1' in doc_ids
    assert '3' in doc_ids
    assert '2' not in doc_ids  # This one should be deleted (age=25 < 27)
