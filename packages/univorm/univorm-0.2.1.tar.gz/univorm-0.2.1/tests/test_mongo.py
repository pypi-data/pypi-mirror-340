# mypy: disable_error_code="type-arg"

import pytest
from bson.objectid import ObjectId
from polars import DataFrame
from pymongo import AsyncMongoClient

from xin.reader.nosql import find_in_collection
from xin.writer.nosql import insert_into_collection


@pytest.mark.asyncio
async def test_query_with_result(mongo_client: AsyncMongoClient) -> None:
    documents = [{"name": "test1"}, {"name": "test2"}]
    object_ids = await insert_into_collection(
        documents=documents, client=mongo_client, dbname="test", collection_name="test"
    )
    assert isinstance(object_ids, list)
    for object_id in object_ids:
        assert isinstance(object_id, ObjectId)

    df = await find_in_collection(query={}, client=mongo_client, dbname="test", collection_name="test")
    assert isinstance(df, DataFrame)
    assert df.shape[0] > 0
    assert df.shape[1] > 1
