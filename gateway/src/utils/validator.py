from fastapi import Form, HTTPException, status, UploadFile, File
import PIL.Image
import io

async def validate_product_name(name: str = Form(...)) -> str:
    if not name.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tên sản phẩm không được để trống")
    return name.strip()

async def validate_product_price(price: int = Form(...)) -> int:
    if price <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Giá sản phẩm phải lớn hơn 0")
    return price

async def validate_product_description(description: str = Form(...)) -> str:
    if not description.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mô tả sản phẩm không được để trống")
    return description.strip()

async def validate_picture(picture: UploadFile = File(...)) -> UploadFile:
    try:
        image = PIL.Image.open(io.BytesIO(await picture.read()))
        image.verify()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vui lòng chọn file ảnh")
    picture.file.seek(0, 2)
    file_size = picture.file.tell()
    if file_size > 10 * 1024 * 1024:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vui lòng chọn ảnh có kích thước dưới 10 MB")
    picture.file.seek(0)
    return picture
