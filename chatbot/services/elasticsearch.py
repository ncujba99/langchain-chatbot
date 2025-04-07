import os
from typing import List, Literal, Optional
from langchain.tools import tool
from elasticsearch import AsyncElasticsearch



es_host = os.environ.get("ELASTICSEARCH_HOST", "elasticsearch")
es_port = 9200
es = AsyncElasticsearch([{'host': es_host, 'port': es_port, 'scheme': 'http'}])
index_name = "products"

@tool
async def product_search_tool(
    search_term: Optional[str] = None,
    product_id: Optional[str] = None,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    color: Optional[str] = None,
    material: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    rating: Optional[float] = None,
    min_rating: Optional[float] = None,
    max_rating: Optional[float] = None,
    features: Optional[List[str]] = None,
    sort_by: Optional[Literal["price", "rating", "name", "relevance"]] = None,
    sort_order: Literal["asc", "desc"] = "asc",

):
    """
    ElasticSearch product search tool.

    This tool performs an ElasticSearch query and returns the response as a Python dictionary.

    Args:
        search_term (Optional[str]): General search term for product name or description. If not provided, all products are considered.
        product_id (Optional[str]): Filter by product ID.
        category (Optional[str]): Filter by product category.
        brand (Optional[str]): Filter by product brand.
        color (Optional[str]): Filter by product color.
        material (Optional[str]): Filter by product material.
        min_price (Optional[float]): Minimum price filter.
        max_price (Optional[float]): Maximum price filter.
        rating (Optional[float]): Exact rating filter. If provided, min_rating and max_rating are ignored.
        min_rating (Optional[float]): Minimum rating filter.
        max_rating (Optional[float]): Maximum rating filter.
        features (Optional[List[str]]): List of required product features.
        sort_by (Optional[Literal["price", "rating", "name", "relevance"]]): Field to sort results by.
        sort_order (Literal["asc", "desc"]): Sorting order, default is "asc".

    Returns:
        list: The ElasticSearch response as a Python dictionary.
    """

    limit= 5

    print(f"Searching for products with  product_id: {product_id}, category: {category}, brand: {brand}, color: {color}, material: {material}, min_price: {min_price}, max_price: {max_price}, rating: {rating}, min_rating: {min_rating}, max_rating: {max_rating}, features: {features}, sort_by: {sort_by}, sort_order: {sort_order}, limit: {limit}")

    search_body = {
        "size": limit,
        "query": {
            "bool": {
                "must": [],
                "filter": []
            }
        }
    }


    if product_id:
        search_body["query"]["bool"]["filter"].append({"term": {"product_id.keyword": product_id}})

    if category:
        search_body["query"]["bool"]["filter"].append({"term": {"category.keyword": category}})
    if brand:
        search_body["query"]["bool"]["filter"].append({"term": {"brand.keyword": brand}})
    if color:
        search_body["query"]["bool"]["filter"].append({"term": {"color.keyword": color}})
    if material:
        search_body["query"]["bool"]["filter"].append({"term": {"material.keyword": material}})

    if min_price is not None and max_price is not None:
        search_body["query"]["bool"]["filter"].append(
            {"range": {"price": {"gte": min_price, "lte": max_price}}}
        )
    elif min_price is not None:
        search_body["query"]["bool"]["filter"].append({"range": {"price": {"gte": min_price}}})
    elif max_price is not None:
        search_body["query"]["bool"]["filter"].append({"range": {"price": {"lte": max_price}}})

    if rating is not None:
        search_body["query"]["bool"]["filter"].append({"term": {"rating": rating}})
    elif min_rating is not None and max_rating is not None:
        search_body["query"]["bool"]["filter"].append(
            {"range": {"rating": {"gte": min_rating, "lte": max_rating}}}
        )
    elif min_rating is not None:
        search_body["query"]["bool"]["filter"].append({"range": {"rating": {"gte": min_rating}}})
    elif max_rating is not None:
        search_body["query"]["bool"]["filter"].append({"range": {"rating": {"lte": max_rating}}})

    if features:
        for feature in features:
            search_body["query"]["bool"]["filter"].append({"term": {"features.keyword": feature}})

    if sort_by:
        sort_field = sort_by
        if sort_by in ["category", "brand", "color", "material", "product_id"]:
            sort_field = f"{sort_by}.keyword"
        search_body["sort"] = [{sort_field: {"order": sort_order}}]


    response = await es.search(index=index_name, body=search_body)
    results = []
    for hit in response['hits']['hits']:
        results.append(hit['_source'])
    return results
