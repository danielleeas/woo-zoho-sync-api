from fastapi import HTTPException
from sqlmodel import select
from app.core.database import get_session
from datetime import datetime

from app.core.security import verify_password
from app.models.oauth import OAuth
from app.models.category import Category, CategoryBase
from app.models.product import Product, ProductBase
from app.models.customer import Customer, CustomerBase
from app.models.order import Order, OrderBase
from app.models.line_items import LineItems, LineItemsBase
from app.models.user import User, UserLogin, UserCreate, UserPublic
from app.core.security import get_password_hash
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
                    product_id=product.product_id,
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
                    purchase_price=product.purchase_price if product.purchase_price else "",
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
    
    async def insert_customer(self, customer: CustomerBase):
        try:
            async for db in get_session():
                db_customer = Customer(
                    woo_id=customer.woo_id,
                    first_name=customer.first_name,
                    last_name=customer.last_name,
                    username=customer.username,
                    email=customer.email,
                    billing_first_name=customer.billing_first_name,
                    billing_last_name=customer.billing_last_name,
                    billing_company=customer.billing_company,
                    billing_address_1=customer.billing_address_1,
                    billing_address_2=customer.billing_address_2,
                    billing_city=customer.billing_city,
                    billing_postcode=customer.billing_postcode,
                    billing_country=customer.billing_country,
                    billing_state=customer.billing_state,
                    billing_email=customer.billing_email,
                    billing_phone=customer.billing_phone,
                    shipping_first_name=customer.shipping_first_name,
                    shipping_last_name=customer.shipping_last_name,
                    shipping_company=customer.shipping_company,
                    shipping_address_1=customer.shipping_address_1,
                    shipping_address_2=customer.shipping_address_2,
                    shipping_city=customer.shipping_city,
                    shipping_postcode=customer.shipping_postcode,
                    shipping_country=customer.shipping_country,
                    shipping_state=customer.shipping_state,
                    shipping_phone=customer.shipping_phone,
                    is_paying_customer=customer.is_paying_customer,
                    avatar_url=customer.avatar_url,
                    created_at=customer.created_at,
                    updated_at=customer.updated_at
                )
                db.add(db_customer)
                try:
                    await db.commit()
                    await db.refresh(db_customer)
                    return db_customer
                except Exception as e:
                    await db.rollback()
                    raise Exception(f"Failed to insert customer: {str(e)}")
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
        return None
    
    async def insert_order(self, order: OrderBase):
        try:
            async for db in get_session():
                db_order = Order(
                    order_id=order.order_id,
                    customer_id=order.customer_id,
                    status=order.status,
                    currency=order.currency,
                    prices_include_tax=order.prices_include_tax,
                    discount_total=order.discount_total,
                    discount_tax=order.discount_tax,
                    shipping_total=order.shipping_total,
                    shipping_tax=order.shipping_tax,
                    cart_tax=order.cart_tax,
                    total=order.total,
                    total_tax=order.total_tax,
                    order_key=order.order_key,
                    billing_first_name=order.billing_first_name,
                    billing_last_name=order.billing_last_name,
                    billing_company=order.billing_company,
                    billing_address_1=order.billing_address_1,
                    billing_address_2=order.billing_address_2,
                    billing_city=order.billing_city,
                    billing_state=order.billing_state,
                    billing_postcode=order.billing_postcode,
                    billing_country=order.billing_country,
                    billing_email=order.billing_email,
                    billing_phone=order.billing_phone,
                    shipping_first_name=order.shipping_first_name,
                    shipping_last_name=order.shipping_last_name,
                    shipping_company=order.shipping_company,
                    shipping_address_1=order.shipping_address_1,
                    shipping_address_2=order.shipping_address_2,
                    shipping_city=order.shipping_city,
                    shipping_state=order.shipping_state,
                    shipping_postcode=order.shipping_postcode,
                    shipping_country=order.shipping_country,
                    transaction_id=order.transaction_id,
                    customer_ip_address=order.customer_ip_address,
                    customer_user_agent=order.customer_user_agent,
                    created_via=order.created_via,
                    customer_note=order.customer_note,
                    date_completed=order.date_completed,
                    date_created=order.date_created,
                    date_modified=order.date_modified,
                    date_paid=order.date_paid,
                    cart_hash=order.cart_hash,
                    number=order.number,
                    payment_url=order.payment_url,
                    currency_symbol=order.currency_symbol,
                )
                db.add(db_order)
                try:
                    await db.commit()
                    await db.refresh(db_order)
                    return db_order
                except Exception as e:
                    await db.rollback()
                    raise Exception(f"Failed to insert order: {str(e)}")
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
        return None

    async def insert_order_line(self, order_line: LineItemsBase):
        try:
            async for db in get_session():
                db_order_line = LineItems(
                    order_id=order_line.order_id,
                    name=order_line.name,
                    product_id=order_line.product_id,
                    variation_id=order_line.variation_id,
                    quantity=order_line.quantity,
                    tax_class=order_line.tax_class,
                    subtotal=order_line.subtotal,
                    subtotal_tax=order_line.subtotal_tax,
                    total=order_line.total,
                    total_tax=order_line.total_tax,
                    sku=order_line.sku,
                    price=order_line.price
                )
                db.add(db_order_line)
                try:
                    await db.commit()
                    await db.refresh(db_order_line)
                    return db_order_line
                except Exception as e:
                    await db.rollback()
                    raise Exception(f"Failed to insert order line: {str(e)}")
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
        return None
    
    async def get_products(self, page: int = 1, per_page: int = 10, filters: dict = None):
        async for db in get_session():
            query = select(Product)
            
            # Apply dynamic filters if any
            if filters:
                for field, value in filters.items():
                    if hasattr(Product, field):
                        query = query.where(getattr(Product, field) == value)
            
            # Add pagination
            query = query.offset((page - 1) * per_page).limit(per_page)
            
            result = (await db.exec(query)).all()
            return result
        return None
    
    async def get_product(self, product_id: int):
        async for db in get_session():
            statement = select(Product).where(Product.product_id == product_id)
            result = (await db.exec(statement)).first()
            return result
        return None
    
    async def get_product_variations(self, product_id: int):
        async for db in get_session():
            statement = select(Product).where(Product.parent_id == product_id)
            result = (await db.exec(statement)).all()
            return result
        return None
    
    async def search_products_by_sku(self, sku: str):
        async for db in get_session():
            statement = select(Product).where(Product.sku == sku)
            result = (await db.exec(statement)).first()
            return result
        return None
    
    async def search_products_by_name(self, query: str, page: int = 1, per_page: int = 10) -> list[Product]:
        async for db in get_session():
            search_term = f"%{query}%"  # Add wildcards for LIKE query
            statement = select(Product).where(Product.name.ilike(search_term)) \
                                     .offset((page - 1) * per_page) \
                                     .limit(per_page)
            result = (await db.exec(statement)).all()
            return result
        return None
    
    async def get_orders(self, page: int = 1, per_page: int = 10, filters: dict = None):
        async for db in get_session():
            # Join Order with LineItems
            query = select(Order, LineItems).join(LineItems, Order.order_id == LineItems.order_id, isouter=True).order_by(Order.order_id.asc())
            
            # Apply dynamic filters if any
            if filters:
                for field, value in filters.items():
                    if hasattr(Order, field):
                        query = query.where(getattr(Order, field) == value)
            
            # Add pagination
            query = query.offset((page - 1) * per_page).limit(per_page)
            
            # Execute query and fetch results
            results = (await db.exec(query)).all()
            
            # Process results to create a dictionary with orders and their line items
            orders_dict = {}
            for order, line_item in results:
                if order.id not in orders_dict:
                    order_dict = order.model_dump()
                    order_dict['line_items'] = []
                    orders_dict[order.id] = order_dict
                
                if line_item:
                    orders_dict[order.id]['line_items'].append(line_item.model_dump())
            
            return list(orders_dict.values())
        return None
    
    async def get_order_by_id(self, order_id: int):
        async for db in get_session():
            statement = select(Order, LineItems).join(LineItems, Order.order_id == LineItems.order_id, isouter=True).where(Order.order_id == order_id)
            result = (await db.exec(statement)).first()
            order_dict = result[0].model_dump()
            order_dict['line_items'] = []
            if result[1]:
                order_dict['line_items'].append(result[1].model_dump())
            return order_dict
        return None
    
    async def login_user(self, user: UserLogin):
        async for db in get_session():
            statement = select(User).where(User.email == user.email)
            result = (await db.exec(statement)).first()
            if not result:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            if not verify_password(user.password, result.password):
                raise HTTPException(status_code=401, detail="Invalid credentials")
            return UserPublic(
                id=result.id,
                username=result.username,
                email=result.email,
                is_superuser=result.is_superuser,
                is_active=result.is_active
            )
        return None
    
    async def create_user(self, user: UserCreate):
        async for db in get_session():
            db_user = User(
                username=user.username,
                email=user.email,
                password=get_password_hash(user.password)
            )
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)
            return db_user
    
    async def update_order_status(self, order_id: int, status: str):
        async for db in get_session():
            statement = select(Order).where(Order.order_id == order_id)
            result = (await db.exec(statement)).first()
            if not result:
                raise HTTPException(status_code=404, detail="Order not found")
            result.status = status
            await db.commit()
            await db.refresh(result)
            return result
        
    async def delete_product(self, product_id: int):
        async for db in get_session():
            statement = select(Product).where(Product.product_id == product_id)
            result = (await db.exec(statement)).first()
            if not result:
                raise HTTPException(status_code=404, detail="Product not found")
            await db.delete(result)
            await db.commit()
            return True
    async def update_product(self, product_id: int, product: ProductBase):
        async for db in get_session():
            statement = select(Product).where(Product.product_id == product_id)
            result = (await db.exec(statement)).first()
            if not result:
                result = await self.insert_product(product)
                return result
            
            # Update the existing product's attributes
            result.parent_id = product.parent_id
            result.product_id = product.product_id
            result.name = product.name
            result.slug = product.slug
            result.permalink = product.permalink
            result.date_created = product.date_created
            result.date_modified = product.date_modified
            result.type = product.type
            result.status = product.status
            result.featured = product.featured
            result.description = product.description
            result.sku = product.sku
            result.price = product.price
            result.regular_price = product.regular_price
            result.stock_quantity = product.stock_quantity
            result.weight = product.weight
            result.length = product.length
            result.width = product.width
            result.height = product.height
            result.categories = product.categories
            result.images = product.images
            result.attribute_name = product.attribute_name
            result.attribute_value = product.attribute_value
            
            await db.commit()
            await db.refresh(result)
            return result
