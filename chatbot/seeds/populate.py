import os
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json
import time


es_host = os.environ.get("ELASTICSEARCH_HOST", "elasticsearch")
es_port = 9200        # Default Elasticsearch port
es = Elasticsearch([{'host': es_host, 'port': es_port, 'scheme': 'http'}]) # Adjust scheme if using HTTPS

# Index name
index_name = "products"

# Mock product data (same as the JSON output from the previous step)
products_data = [
  {
    "_index": "products",
    "_id": "1",
    "_source": {
      "product_id": "PROD001",
      "name": "Awesome T-Shirt",
      "description": "A comfortable and stylish t-shirt made from 100% organic cotton.",
      "price": 25.99,
      "category": "Apparel",
      "brand": "Fashionista",
      "color": "Blue",
      "material": "Cotton",
      "inventory": 150,
      "created_at": "2024-07-15T10:30:00Z",
      "updated_at": "2024-08-20T14:45:00Z",
      "features": ["Soft", "Breathable", "Durable"],
      "rating": 4.5
    }
  },
  {
    "_index": "products",
    "_id": "2",
    "_source": {
      "product_id": "PROD002",
      "name": "Wireless Headphones",
      "description": "High-quality over-ear headphones with active noise cancellation.",
      "price": 199.00,
      "category": "Electronics",
      "brand": "SoundWave",
      "color": "Black",
      "material": "Plastic",
      "inventory": 50,
      "created_at": "2024-09-01T16:00:00Z",
      "updated_at": "2024-10-10T09:15:00Z",
      "features": ["Noise Cancelling", "Bluetooth 5.0", "Long Battery Life"],
      "rating": 4.8
    }
  },
  {
    "_index": "products",
    "_id": "3",
    "_source": {
      "product_id": "PROD003",
      "name": "Wooden Coffee Table",
      "description": "A handcrafted coffee table made from solid oak wood.",
      "price": 149.50,
      "category": "Furniture",
      "brand": "WoodCraft",
      "color": "Brown",
      "material": "Oak Wood",
      "inventory": 25,
      "created_at": "2025-01-20T08:45:00Z",
      "updated_at": "2025-02-28T11:00:00Z",
      "features": ["Handmade", "Sturdy", "Natural Finish"],
      "rating": 4.2
    }
  },
  {
    "_index": "products",
    "_id": "4",
    "_source": {
      "product_id": "PROD004",
      "name": "Running Shoes",
      "description": "Lightweight and comfortable running shoes for daily workouts.",
      "price": 89.99,
      "category": "Footwear",
      "brand": "SwiftStride",
      "color": "Gray",
      "material": "Mesh",
      "inventory": 100,
      "created_at": "2025-03-10T19:30:00Z",
      "updated_at": None,
      "features": ["Cushioned", "Breathable", "Flexible"],
      "rating": 4.6
    }
  },
  {
    "_index": "products",
    "_id": "5",
    "_source": {
      "product_id": "PROD005",
      "name": "Stainless Steel Water Bottle",
      "description": "Reusable water bottle made from durable stainless steel.",
      "price": 19.99,
      "category": "Accessories",
      "brand": "AquaPure",
      "color": "Silver",
      "material": "Stainless Steel",
      "inventory": 200,
      "created_at": "2024-05-10T12:00:00Z",
      "updated_at": "2024-06-15T18:30:00Z",
      "features": ["Leak-proof", "BPA-free", "Double-walled"],
      "rating": 4.7
    }
  },
  {
    "_index": "products",
    "_id": "6",
    "_source": {
      "product_id": "PROD006",
      "name": "Leather Wallet",
      "description": "Classic bifold wallet made from genuine leather.",
      "price": 45.00,
      "category": "Accessories",
      "brand": "Craftsman",
      "color": "Brown",
      "material": "Leather",
      "inventory": 75,
      "created_at": "2024-08-01T09:00:00Z",
      "updated_at": "2024-09-22T15:45:00Z",
      "features": ["Multiple card slots", "ID window", "Durable"],
      "rating": 4.4
    }
  },
  {
    "_index": "products",
    "_id": "7",
    "_source": {
      "product_id": "PROD007",
      "name": "Ceramic Coffee Mug",
      "description": "Hand-painted ceramic coffee mug with a unique design.",
      "price": 12.50,
      "category": "Home Goods",
      "brand": "ArtisanCrafts",
      "color": "Multicolor",
      "material": "Ceramic",
      "inventory": 120,
      "created_at": "2024-11-15T14:30:00Z",
      "updated_at": None,
      "features": ["Microwave safe", "Dishwasher safe", "Unique design"],
      "rating": 4.3
    }
  },
  {
    "_index": "products",
    "_id": "8",
    "_source": {
      "product_id": "PROD008",
      "name": "Gaming Mouse",
      "description": "High-performance gaming mouse with customizable RGB lighting.",
      "price": 59.99,
      "category": "Electronics",
      "brand": "GameMaster",
      "color": "Black",
      "material": "Plastic",
      "inventory": 40,
      "created_at": "2024-06-20T17:15:00Z",
      "updated_at": "2024-07-28T10:00:00Z",
      "features": ["High DPI", "Programmable buttons", "RGB lighting"],
      "rating": 4.9
    }
  },
  {
    "_index": "products",
    "_id": "9",
    "_source": {
      "product_id": "PROD009",
      "name": "Cotton Bed Sheets (Queen)",
      "description": "Soft and breathable cotton bed sheet set for queen-sized beds.",
      "price": 79.00,
      "category": "Home Goods",
      "brand": "ComfortSleep",
      "color": "White",
      "material": "Cotton",
      "inventory": 90,
      "created_at": "2024-09-10T11:45:00Z",
      "updated_at": None,
      "features": ["100% Cotton", "Machine washable", "Wrinkle-resistant"],
      "rating": 4.6
    }
  },
  {
    "_index": "products",
    "_id": "10",
    "_source": {
      "product_id": "PROD010",
      "name": "Denim Jacket",
      "description": "Classic denim jacket for men and women.",
      "price": 69.50,
      "category": "Apparel",
      "brand": "UrbanStyle",
      "color": "Blue",
      "material": "Denim",
      "inventory": 60,
      "created_at": "2024-07-05T13:30:00Z",
      "updated_at": "2024-08-18T16:00:00Z",
      "features": ["Button closure", "Multiple pockets", "Durable"],
      "rating": 4.5
    }
  },
  {
    "_index": "products",
    "_id": "11",
    "_source": {
      "product_id": "PROD011",
      "name": "Smartwatch",
      "description": "Feature-rich smartwatch with fitness tracking and notifications.",
      "price": 129.99,
      "category": "Electronics",
      "brand": "TechLife",
      "color": "Space Gray",
      "material": "Aluminum",
      "inventory": 35,
      "created_at": "2024-10-01T10:15:00Z",
      "updated_at": "2024-11-25T12:30:00Z",
      "features": ["Heart rate monitor", "GPS", "Water-resistant"],
      "rating": 4.7
    }
  },
  {
    "_index": "products",
    "_id": "12",
    "_source": {
      "product_id": "PROD012",
      "name": "Cookbook: Delicious Recipes",
      "description": "A collection of over 100 delicious and easy-to-follow recipes.",
      "price": 29.95,
      "category": "Books",
      "brand": "CulinaryArts",
      "color": "Various",
      "material": "Paperback",
      "inventory": 80,
      "created_at": "2024-04-15T16:45:00Z",
      "updated_at": None,
      "features": ["Full-color photos", "Ingredient lists", "Step-by-step instructions"],
      "rating": 4.8
    }
  },
  {
    "_index": "products",
    "_id": "13",
    "_source": {
      "product_id": "PROD013",
      "name": "Yoga Mat",
      "description": "Non-slip yoga mat for comfortable workouts.",
      "price": 34.99,
      "category": "Sports & Outdoors",
      "brand": "FlexFit",
      "color": "Purple",
      "material": "PVC",
      "inventory": 110,
      "created_at": "2024-12-01T09:30:00Z",
      "updated_at": None,
      "features": ["Non-slip surface", "Lightweight", "Easy to clean"],
      "rating": 4.4
    }
  },
  {
    "_index": "products",
    "_id": "14",
    "_source": {
      "product_id": "PROD014",
      "name": "Desk Lamp",
      "description": "Adjustable LED desk lamp with multiple brightness levels.",
      "price": 39.00,
      "category": "Home Goods",
      "brand": "BrightLight",
      "color": "White",
      "material": "Metal",
      "inventory": 65,
      "created_at": "2024-05-25T11:00:00Z",
      "updated_at": "2024-07-10T14:00:00Z",
      "features": ["Adjustable arm", "Touch control", "Energy-efficient LED"],
      "rating": 4.6
    }
  }
]

# Create the index if it doesn't exist
if not es.indices.exists(index=index_name):
    try:
        es.indices.create(index=index_name)
        print(f"Index '{index_name}' created successfully.")
    except Exception as e:
        print(f"Error creating index '{index_name}': {e}")

# Prepare the actions for bulk indexing
actions = [
    {
        "_index": index_name,
        "_id": product['_id'],
        "_source": product['_source']
    }
    for product in products_data
]

start_time = time.time()
# Use the bulk API to index all documents
successes, errors = bulk(es, actions)
end_time = time.time()

print(f"Indexed {successes} documents in {end_time - start_time:.2f} seconds")
if errors:
    print("Errors occurred during bulk indexing:")
    for error in errors:
        print(error)

print("Finished populating the Elasticsearch index using the bulk API.")