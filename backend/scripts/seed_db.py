import asyncio
import random
import sys
import os
import uuid
from datetime import datetime, timedelta

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from app.db.session import async_session
from app.models.user import User
from app.models.store import Store
from app.models.category import Category
from app.models.product import Product
from app.models.transaction import InventoryTransaction, TransactionType, AdjustReason
from app.services.inventory import process_inbound, process_outbound, process_adjust
from app.schemas.transaction import InboundTransactionCreate, OutboundTransactionCreate, AdjustTransactionCreate

async def seed_data():
    async with async_session() as db:
        print("Seeding realistic dummy data (No Faker)...")

        # 1. Ensure User
        user = (await db.execute(select(User).limit(1))).scalar_one_or_none()
        if not user:
            print("Creating default user...")
            user = User(
                email="admin@dondone.com",
                full_name="관리자",
                hashed_password="dummy_password_hash",
                is_active=True,
                is_superuser=True
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        print(f"User: {user.email}")

        # 2. Create Stores
        stores = []
        store_configs = [
            ("강남본점", "서울 강남구 테헤란로 123", "02-555-1234"),
            ("부산서면점", "부산 부산진구 중앙대로 456", "051-808-5678"),
            ("대구동성로점", "대구 중구 동성로 789", "053-424-9012"),
            ("대전둔산점", "대전 서구 둔산로 101", "042-488-3456"),
            ("광주상무점", "광주 서구 상무중앙로 202", "062-373-7890"),
            ("인천송도점", "인천 연수구 컨벤시아대로 1", "032-830-1111"),
            ("울산삼산점", "울산 남구 삼산로 2", "052-260-2222")
        ]
        
        for name, address, phone in store_configs:
            # Check if exists (by name)
            exists = (await db.execute(select(Store).where(Store.name == name))).scalar_one_or_none()
            if exists:
                stores.append(exists)
                continue
                
            store_code = f"STORE-{uuid.uuid4().hex[:6].upper()}"
            store = Store(
                code=store_code,
                name=name,
                address=address,
                phone=phone,
                is_active=True
            )
            db.add(store)
            stores.append(store)
        
        await db.commit()
        for s in stores: await db.refresh(s)
        print(f"Stores: {len(stores)}")

        # 3. Create Categories
        categories = []
        cat_names = ["음료", "스낵", "신선식품", "생활용품", "가전", "주류", "반려동물"]
        for i, name in enumerate(cat_names):
             # Check if exists
            exists = (await db.execute(select(Category).where(Category.name == name))).scalar_one_or_none()
            if exists:
                categories.append(exists)
                continue

            cat = Category(
                code=f"CAT-{i+1:03d}",
                name=name,
                sort_order=i+1
            )
            db.add(cat)
            categories.append(cat)
        
        await db.commit()
        for c in categories: await db.refresh(c)
        print(f"Categories: {len(categories)}")

        # 4. Create Products
        products = []
        product_names = {
            "음료": ["코카콜라 250ml", "칠성사이다 500ml", "제주삼다수 2L", "서울우유 1L", "카누 아메리카노", "포카리스웨트", "레쓰비 캔커피"],
            "스낵": ["포카칩 오리지널", "새우깡", "홈런볼", "꼬북칩 초코", "프링글스 어니언", "오징어땅콩", "맛동산"],
            "신선식품": ["국산 콩두부", "무항생제 계란 10구", "숙주나물 300g", "양파 1kg", "상추 한봉", "사과 1봉", "한돈 삼겹살 500g"],
            "생활용품": ["코디 휴지 30롤", "다우니 섬유유연제", "리스테린 750ml", "지퍼백 중형", "물티슈 100매", "샴푸 500ml", "치약 3입"],
            "가전": ["AA 건전지 4입", "USB C타입 케이블", "멀티탭 3구", "이어폰", "휴대용 선풍기"],
            "주류": ["참이슬 fresh", "카스 맥주 500ml", "테라 맥주 355ml", "진로 이즈백", "서울 막걸리"],
            "반려동물": ["츄르 참치맛", "강아지 배변패드", "고양이 모래", "개껌 미니", "닭가슴살 큐브"]
        }

        for cat in categories:
            items = product_names.get(cat.name, [])
            for item in items:
                 # Check if exists
                exists = (await db.execute(select(Product).where(Product.name == item))).scalar_one_or_none()
                if exists:
                    products.append(exists)
                    continue
                
                prod = Product(
                    category_id=cat.id,
                    barcode=f"880{random.randint(1000000000, 9999999999)}",
                    name=item,
                    safety_stock=random.randint(10, 50),
                    memo="Dummy Data",
                    is_active=True
                )
                db.add(prod)
                products.append(prod)
        
        await db.commit()
        for p in products: await db.refresh(p)
        print(f"Products: {len(products)}")

        # 5. Create Transactions (Seed Inventory)
        # Process Inbound via Service to update Stock
        print("Processing Inbound Transactions...")
        count_inbound = 0
        for store in stores:
            # Pick random products
            selected_products = random.sample(products, min(len(products), 20))
            for prod in selected_products:
                qty = random.randint(50, 300)
                inbound_data = InboundTransactionCreate(
                    product_id=str(prod.id),
                    store_id=str(store.id),
                    quantity=qty,
                    note="초기 재고 세팅"
                )
                await process_inbound(db, inbound_data, user)
                count_inbound += 1
        print(f"Processed {count_inbound} Inbound Transactions.")
        
        # 6. Random Outbound/Adjust
        print("Processing Random Outbound/Adjust...")
        count_ops = 0
        for _ in range(50):
            store = random.choice(stores)
            prod = random.choice(products)
            
            # 80% Outbound, 20% Adjust
            if random.random() < 0.8:
                try:
                    out_data = OutboundTransactionCreate(
                        product_id=str(prod.id),
                        store_id=str(store.id),
                        quantity=random.randint(1, 5),
                        note="더미 판매 데이터"
                    )
                    await process_outbound(db, out_data, user)
                    count_ops += 1
                except Exception:
                    continue # Skip if insufficient stock
            else:
                try:
                    adj_data = AdjustTransactionCreate(
                        product_id=str(prod.id),
                        store_id=str(store.id),
                        quantity=random.randint(-2, 2),
                        reason=random.choice(list(AdjustReason)),
                        note="더미 조정 데이터"
                    )
                    await process_adjust(db, adj_data, user)
                    count_ops += 1
                except Exception:
                    continue
        print(f"Processed {count_ops} Outbound/Adjust Transactions.")

        print("Data Seeding Completed Successfully!")

if __name__ == "__main__":
    asyncio.run(seed_data())
