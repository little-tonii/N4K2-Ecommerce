from datetime import datetime, timezone
from starlette import status
from bson import ObjectId
from fastapi import HTTPException
from ..models.product_model import ProductModel
from ..configs.database import product_collection, category_collection
from ..schemas.product_response_schema import ProductResponse


class ProductTasks:
    
    @classmethod
    async def get_all_products_task(cls) -> list[ProductResponse]:
        products = []
        async for product in product_collection.find():
            products.append(
                ProductResponse(
                    id=str(product["_id"]),
                    name=product["name"],
                    price=product["price"],
                    description=product["description"],
                    category_id=product["category_id"],
                    image_url=product["image_url"],
                    created_at=product["created_at"],
                    updated_at=product["updated_at"]
                )
            )
        return products
    
    @classmethod
    async def create_product_task(cls, name: str, price: int, description: str, category_id: str, image_url: str) -> ProductResponse:
        category = await category_collection.find_one({"_id": ObjectId(category_id)})
        if not category:
            raise HTTPException(status_code=404, detail="Danh mục không tồn tại")
        new_product = ProductModel(
            name=name,
            price=price,
            description=description,
            category_id=category_id,
            image_url=image_url,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        product_data = new_product.model_dump(exclude={"id"})
        result = await product_collection.insert_one(product_data)
        new_product.id = result.inserted_id
        return ProductResponse(
            id=str(new_product.id),
            name=new_product.name,
            price=new_product.price,
            description=new_product.description,
            category_id=new_product.category_id,
            image_url=new_product.image_url,
            created_at=new_product.created_at,
            updated_at=new_product.updated_at
        )
        
    @classmethod
    async def get_product_by_id_task(cls, id: str) -> ProductResponse:
        product = await product_collection.find_one({"_id": ObjectId(id)})
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sản phẩm không tồn tại")
        return ProductResponse(
            id=str(product["_id"]),
            name=product["name"],
            price=product["price"],
            description=product["description"],
            category_id=product["category_id"],
            image_url=product["image_url"],
            created_at=product["created_at"],
            updated_at=product["updated_at"]
        )