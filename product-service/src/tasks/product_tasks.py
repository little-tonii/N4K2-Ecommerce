from datetime import datetime, timezone
from starlette import status
from bson import ObjectId
from fastapi import HTTPException
from ..models.product_model import ProductModel
from ..configs.database import product_collection, category_collection
from ..schemas.product_response_schema import ProductResponse, RecommendationProductResponse
import httpx
from transformers import pipeline

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
    
    sentiment_pipeline = pipeline("sentiment-analysis")
        
    def score_comment(text: str) -> float:
        result = sentiment_pipeline(text)[0]
        label = result["label"]
        score = result["score"]

        if label == "POSITIVE":
            if score > 0.9:
                return 1.5  # so good
            elif score > 0.75:
                return 1.0  # good
            else:
                return 0.5  # normal
        else:
            if score > 0.9:
                return -1.5  # very bad
            elif score > 0.75:
                return -1.0  # bad
            else:
                return -0.5  # meh bad

    # Your updated function
    @classmethod
    async def get_recommendation_products_task(cls) -> list[RecommendationProductResponse]:
        products = []

        async with httpx.AsyncClient() as client:
            async for product in product_collection.find():
                product_id = str(product["_id"])
                comment_url = f'http://host.docker.internal:8000/product/{product_id}/comment'

                try:
                    response = await client.get(comment_url)
                    if response.status_code == 200:
                        data = response.json()
                        comments = data.get("comments", [])
                    else:
                        comments = []
                except Exception as e:
                    print(f"Error fetching comments for {product_id}: {e}")
                    comments = []

                # Apply sentiment scoring
                sentiment_score = 0.0
                for comment in comments:
                    comment_score = score_comment(comment["content"])
                    sentiment_score += comment_score

                products.append(
                    RecommendationProductResponse(
                        id=product_id,
                        name=product["name"],
                        price=product["price"],
                        description=product["description"],
                        category_id=product["category_id"],
                        image_url=product["image_url"],
                        created_at=product["created_at"],
                        updated_at=product["updated_at"],
                        rate=sentiment_score  # use sentiment as the new "rate"
                    )
                )

        sorted_products = sorted(products, key=lambda p: p.rate, reverse=True)

        return sorted_products

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
        try:
            object_id = ObjectId(id)
            product = await product_collection.find_one({"_id": object_id})
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
        except bson.errors.InvalidId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid product ID format"
            )
            
    @classmethod
    async def delete_product_by_id_task(cls, id: str) -> None:
        deleted_product = await product_collection.find_one_and_delete({"_id": ObjectId(id)})
        if not deleted_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sản phẩm không tồn tại")
        return None
    
    @classmethod
    async def update_product_by_id_task(cls, id: str, name: str | None, price: int | None, description: str | None, category_id: str | None, image_url: str | None) -> ProductResponse:
        updated_at = datetime.now(timezone.utc)
        update_fields = { 
            key: value for key, value in {
                "name": name,
                "price": price,
                "description": description,
                "category_id": category_id,
                "image_url": image_url,
                "updated_at": updated_at
            }.items() if value is not None
        }
        if not update_fields:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vui lòng nhập thông tin cần cập nhật")
        updated_product = await product_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": update_fields},
            return_document=True
        )
        if not updated_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sản phẩm không tồn tại")
        return ProductResponse(
            id=str(updated_product["_id"]),
            name=updated_product["name"],
            price=updated_product["price"],
            description=updated_product["description"],
            category_id=updated_product["category_id"],
            image_url=updated_product["image_url"],
            created_at=updated_product["created_at"],
            updated_at=updated_product["updated_at"]
        )