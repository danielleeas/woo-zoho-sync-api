from sqlmodel import select
from app.core.database import get_session
from datetime import datetime

from app.models.oauth import OAuth
from app.models.category import Category, CategoryBase
from app.models.product import Product, ProductBase

class PostgresAgent:
    async def insert_oauth(self, access_token: str, refresh_token: str, expires_at: datetime):
        async for db in get_session():
            db_oauth = OAuth(access_token=access_token, refresh_token=refresh_token, expires_at=expires_at)
            db.add(db_oauth)
            await db.commit()
            await db.refresh(db_oauth)
            return db_oauth
        return None
    
    async def update_oauth(self, access_token: str, refresh_token: str, expires_at: datetime):
        async for db in get_session():
            statement = select(OAuth).where(OAuth.refresh_token == refresh_token)
            result = (await db.exec(statement)).first()
            result.access_token = access_token
            result.expires_at = expires_at
            await db.commit()
            await db.refresh(result)
            return result
        return None
    
    async def get_oauth(self):
        async for db in get_session():
            statement = select(OAuth)
            result = (await db.exec(statement)).first()
            return result
        return None
    
    async def get_access_token(self):
        async for db in get_session():
            statement = select(OAuth)
            result = (await db.exec(statement)).first()
            return result.access_token
        return None
    
    async def insert_category(self, category: CategoryBase):
        async for db in get_session():
            db_category = Category(
                name=category.name,
                slug=category.slug,
            )
            db.add(db_category)
            await db.commit()
            await db.refresh(db_category)
            return db_category
        return None
    
    async def get_category_by_woo_id(self, woo_id: int):
        async for db in get_session():
            statement = select(Category).where(Category.woo_id == woo_id)
            result = (await db.exec(statement)).first()
            return result
        return None
    
    async def insert_product(self, product: ProductBase):
        try:
            async for db in get_session():
                db_product = Product(
                    parent_id=product.parent_id,
                    name=product.name,
                    slug=product.slug,
                    permalink=product.permalink,
                    date_created=product.date_created,
                    date_modified=product.date_modified,
                    type=product.type,
                    status=product.status,
                    featured=product.featured,
                    description=product.description,
                    sku=product.sku,
                    price=product.price,
                    regular_price=product.regular_price,
                    stock_quantity=product.stock_quantity,
                    weight=product.weight,
                    length=product.length,
                    width=product.width,
                    height=product.height,
                    categories=product.categories,
                    images=product.images,
                    attribute_name=product.attribute_name,
                    attribute_value=product.attribute_value,
                )
                db.add(db_product)
                try:
                    await db.commit()
                    await db.refresh(db_product)
                    return db_product
                except Exception as e:
                    await db.rollback()
                    raise Exception(f"Failed to insert product: {str(e)}")
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
        return None
        
        