from datetime import datetime, timezone

from bson import ObjectId
from fastapi import HTTPException
from ..schemas.category_response_schema import CategoryResponse
from ..configs.database import category_collection
from ..models.category_model import CategoryModel 

class CategoryTasks:
    
    @classmethod
    async def create_category_task(cls, name: str)-> CategoryResponse:
        new_category = CategoryModel(name=name)
        category_data = new_category.model_dump(exclude_unset=True, exclude={"id"})
        result = await category_collection.insert_one(category_data)
        new_category.id = result.inserted_id
        return CategoryResponse(
            id=str(result.inserted_id),
            name=new_category.name,
            created_at=new_category.created_at,
            updated_at=new_category.updated_at   
        )
        
    @classmethod
    async def get_all_categories_task(cls)-> list[CategoryResponse]:
        categories = []
        async for category in category_collection.find():
            categories.append(CategoryResponse(
                id=str(category["_id"]),
                name=category["name"],
                created_at=category.get("created_at", datetime.now(timezone.utc)),
                updated_at=category.get("updated_at", datetime.now(timezone.utc))
            ))
        return categories

    @classmethod
    async def get_category_by_id_task(cls, id: str)-> CategoryResponse:
        category = await category_collection.find_one({"_id": ObjectId(id)})
        if not category:
            raise HTTPException(status_code=404, detail="Danh mục không tồn tại")
        return CategoryResponse(
            id=str(category["_id"]),
            name=category["name"],
            created_at=category.get("created_at", datetime.now(timezone.utc)),
            updated_at=category.get("updated_at", datetime.now(timezone.utc))
        )
        
    @classmethod
    async def update_category_task(cls, id: str, name: str)-> CategoryResponse:
        updated_at = datetime.now(timezone.utc)
        updated_category = await category_collection.find_one_and_update(
            {"_id": ObjectId(id)}, 
            {"$set": {
                "name": name, 
                "updated_at": updated_at
            }},
            return_document=True
        )
        if not updated_category:
            raise HTTPException(status_code=404, detail="Danh mục không tồn tại")
        return CategoryResponse(
            id=str(updated_category["_id"]),
            name=updated_category["name"],
            created_at=updated_category.get("created_at", datetime.now(timezone.utc)),
            updated_at=updated_category.get("updated_at", datetime.now(timezone.utc))
        )
    
    @classmethod
    async def delete_category_task(cls, id: str) -> None:
        deleted_category = await category_collection.find_one_and_delete({"_id": ObjectId(id)})
        if not deleted_category:
            raise HTTPException(status_code=404, detail="Danh mục không tồn tại")
        return None