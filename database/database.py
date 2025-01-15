from typing import List, TypeVar
from typing import Union

from beanie import Document, PydanticObjectId

T = TypeVar('T', bound=Document)


async def add_document(collection: T, new_document: T) -> T:
    """
    添加一个新的文档到指定集合。

    :param collection: 集合对象
    :param new_document: 新的文档对象
    :return: 添加的文档对象

    # 调用示例
    # new_student = Student(name="John Doe", age=20)
    # added_student = await add_document(student_collection, new_student)
    """
    document = await new_document.create()
    return document


async def retrieve_document(collection: T, id: PydanticObjectId) -> T:
    """
    根据ID检索文档。

    :param collection: 集合对象
    :param id: 文档的ID
    :return: 检索到的文档对象

    # 调用示例
    # student = await retrieve_document(student_collection, "some_student_id")
    """
    document = await collection.get(id)
    return document


async def retrieve_documents_by_field(collection: T, query_params: dict) -> List[T]:
    """
    根据任意字段查询文档。

    :param collection: 集合对象
    :param query_params: 查询参数字典
    :return: 检索到的文档对象列表

    # 调用示例
    # students = await retrieve_documents_by_field(student_collection, {"age": 20})
    """
    documents = await collection.find(query_params).to_list(None)
    return documents


async def delete_document(collection: T, id: PydanticObjectId) -> bool:
    """
    根据ID删除文档。

    :param collection: 集合对象
    :param id: 文档的ID
    :return: 删除成功返回True，否则返回False

    # 调用示例
    # success = await delete_document(student_collection, "some_student_id")
    """
    document = await collection.get(id)
    if document:
        await document.delete()
        return True
    return False


async def update_document(collection: T, id: PydanticObjectId, data: dict) -> Union[bool, T]:
    """
    根据ID更新文档。

    :param collection: 集合对象
    :param id: 文档的ID
    :param data: 更新的数据字典
    :return: 更新成功返回更新后的文档对象，否则返回False

    # 调用示例
    # updated_student = await update_document(student_collection, "some_student_id", {"age": 21})
    """
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {field: value for field, value in des_body.items()}}
    document = await collection.get(id)
    if document:
        await document.update(update_query)
        return document
    return False
