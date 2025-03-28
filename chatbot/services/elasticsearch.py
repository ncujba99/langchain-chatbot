import os
from typing import List, Optional
from langchain.tools import tool
from elasticsearch import AsyncElasticsearch



es_host = os.environ.get("ELASTICSEARCH_HOST", "elasticsearch")
es_port = 9200
es = AsyncElasticsearch([{'host': es_host, 'port': es_port, 'scheme': 'http'}])
index_name = "products"

@tool
async def search_tool(
    query: str = "",
    product_id: str = None,
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
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
    limit: int = 50
):
    """Elastic search query for products.

    Args:
        query (str, optional): General search term for product name or description. Defaults to "".
        product_id (str, optional): Filter by product ID. Defaults to None.
        category (str, optional): Filter by product category. Defaults to None.
        brand (str, optional): Filter by product brand. Defaults to None.
        color (str, optional): Filter by product color. Defaults to None.
        material (str, optional): Filter by product material. Defaults to None.
        min_price (float, optional): Minimum price to filter by. Defaults to None.
        max_price (float, optional): Maximum price to filter by. Defaults to None.
        rating (float, optional): Exact rating to filter by. Defaults to None.
        min_rating (float, optional): Minimum rating to filter by. Defaults to None.
        max_rating (float, optional): Maximum rating to filter by. Defaults to None.
        features (List[str], optional): List of features the product should have. Defaults to None.
        sort_by (str, optional): Field to sort results by (e.g., price, rating, name). Defaults to None.
        sort_order (str, optional): Sort order ("asc" or "desc"). Defaults to "asc".
        limit (int, optional): Maximum number of results to return. Defaults to 5.
    """
    print(f"Searching for products with query: {query}, product_id: {product_id}, category: {category}, brand: {brand}, color: {color}, material: {material}, min_price: {min_price}, max_price: {max_price}, rating: {rating}, min_rating: {min_rating}, max_rating: {max_rating}, features: {features}, sort_by: {sort_by}, sort_order: {sort_order}, limit: {limit}")

    search_body = {
        "size": limit,
        "query": {
            "bool": {
                "must": [],
                "filter": []
            }
        }
    }

    if query:
        search_body["query"]["bool"]["must"].append({"match": {"name": query}})
        search_body["query"]["bool"]["must"].append({"match": {"description": query}})
        search_body["query"]["bool"]["must"] = [] # Clear the "must" list
        search_body["query"]["bool"]["should"] = [
            {"match": {"name": query}},
            {"match": {"description": query}}
        ]
        search_body["query"]["bool"]["minimum_should_match"] = 1

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

    try:
        response = await es.search(index=index_name, body=search_body)
        results = []
        for hit in response['hits']['hits']:
            results.append(hit['_source'])
        return {"results": results}
    except Exception as e:
        return {"error": f"An error occurred during the search: {e}"}