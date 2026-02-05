-- 샘플 데이터 삽입 (개발/테스트용)
-- seed_db.py 기반 확장 버전

-- 변수 설정 (ID 재사용을 위해)
DO $$
DECLARE
    -- 카테고리 ID
    cat_beverage_id UUID := gen_random_uuid();
    cat_snack_id UUID := gen_random_uuid();
    cat_fresh_id UUID := gen_random_uuid();
    cat_living_id UUID := gen_random_uuid();
    cat_electronics_id UUID := gen_random_uuid();
    cat_alcohol_id UUID := gen_random_uuid();
    cat_pet_id UUID := gen_random_uuid();
    
    -- 매장 ID
    store_gangnam_id UUID := gen_random_uuid();
    store_busan_id UUID := gen_random_uuid();
    store_daegu_id UUID := gen_random_uuid();
    store_daejeon_id UUID := gen_random_uuid();
    store_gwangju_id UUID := gen_random_uuid();
    store_incheon_id UUID := gen_random_uuid();
    store_ulsan_id UUID := gen_random_uuid();
    
    -- 사용자 ID
    admin_id UUID := gen_random_uuid();
    worker_id UUID := gen_random_uuid();
BEGIN
    -- ========================================
    -- 1. 카테고리 (7개 - seed_db.py 기반)
    -- ========================================
    INSERT INTO categories (id, code, name, sort_order, created_at) VALUES
      (cat_beverage_id, 'CAT-001', '음료', 1, NOW()),
      (cat_snack_id, 'CAT-002', '스낵', 2, NOW()),
      (cat_fresh_id, 'CAT-003', '신선식품', 3, NOW()),
      (cat_living_id, 'CAT-004', '생활용품', 4, NOW()),
      (cat_electronics_id, 'CAT-005', '가전', 5, NOW()),
      (cat_alcohol_id, 'CAT-006', '주류', 6, NOW()),
      (cat_pet_id, 'CAT-007', '반려동물', 7, NOW());

    -- ========================================
    -- 2. 매장 (7개 - seed_db.py 기반)
    -- ========================================
    INSERT INTO stores (id, code, name, address, phone, is_active, created_at) VALUES
      (store_gangnam_id, 'STORE-001', '강남본점', '서울 강남구 테헤란로 123', '02-555-1234', true, NOW()),
      (store_busan_id, 'STORE-002', '부산서면점', '부산 부산진구 중앙대로 456', '051-808-5678', true, NOW()),
      (store_daegu_id, 'STORE-003', '대구동성로점', '대구 중구 동성로 789', '053-424-9012', true, NOW()),
      (store_daejeon_id, 'STORE-004', '대전둔산점', '대전 서구 둔산로 101', '042-488-3456', true, NOW()),
      (store_gwangju_id, 'STORE-005', '광주상무점', '광주 서구 상무중앙로 202', '062-373-7890', true, NOW()),
      (store_incheon_id, 'STORE-006', '인천송도점', '인천 연수구 컨벤시아대로 1', '032-830-1111', true, NOW()),
      (store_ulsan_id, 'STORE-007', '울산삼산점', '울산 남구 삼산로 2', '052-260-2222', true, NOW());

    -- ========================================
    -- 3. 사용자 (비밀번호: password123)
    -- bcrypt 해시: $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewDmy2/JqhN8zLQV
    -- ========================================
    INSERT INTO users (id, email, password_hash, name, role, is_active, created_at) VALUES
      (admin_id, 'admin@donedone.local', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewDmy2/JqhN8zLQV', '관리자', 'ADMIN', true, NOW()),
      (worker_id, 'worker@donedone.local', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewDmy2/JqhN8zLQV', '직원1', 'WORKER', true, NOW());

    -- ========================================
    -- 4. 사용자-매장 매핑
    -- ========================================
    INSERT INTO user_stores (user_id, store_id, assigned_at) VALUES
      (admin_id, store_gangnam_id, NOW()),
      (worker_id, store_gangnam_id, NOW()),
      (worker_id, store_busan_id, NOW());

    -- ========================================
    -- 5. 제품 (43개 - seed_db.py 기반)
    -- ========================================
    -- 음료 (7개)
    INSERT INTO products (id, barcode, name, category_id, safety_stock, memo, is_active, created_at) VALUES
      (gen_random_uuid(), '8801234567001', '코카콜라 250ml', cat_beverage_id, 30, '인기 상품', true, NOW()),
      (gen_random_uuid(), '8801234567002', '칠성사이다 500ml', cat_beverage_id, 30, NULL, true, NOW()),
      (gen_random_uuid(), '8801234567003', '제주삼다수 2L', cat_beverage_id, 50, '생수', true, NOW()),
      (gen_random_uuid(), '8801234567004', '서울우유 1L', cat_beverage_id, 20, '냉장 보관', true, NOW()),
      (gen_random_uuid(), '8801234567005', '카누 아메리카노', cat_beverage_id, 25, NULL, true, NOW()),
      (gen_random_uuid(), '8801234567006', '포카리스웨트', cat_beverage_id, 30, '이온음료', true, NOW()),
      (gen_random_uuid(), '8801234567007', '레쓰비 캔커피', cat_beverage_id, 40, NULL, true, NOW());
    
    -- 스낵 (7개)
    INSERT INTO products (id, barcode, name, category_id, safety_stock, memo, is_active, created_at) VALUES
      (gen_random_uuid(), '8801234567011', '포카칩 오리지널', cat_snack_id, 25, NULL, true, NOW()),
      (gen_random_uuid(), '8801234567012', '새우깡', cat_snack_id, 30, '스테디셀러', true, NOW()),
      (gen_random_uuid(), '8801234567013', '홈런볼', cat_snack_id, 20, NULL, true, NOW()),
      (gen_random_uuid(), '8801234567014', '꼬북칩 초코', cat_snack_id, 25, '신상품', true, NOW()),
      (gen_random_uuid(), '8801234567015', '프링글스 어니언', cat_snack_id, 20, '수입', true, NOW()),
      (gen_random_uuid(), '8801234567016', '오징어땅콩', cat_snack_id, 15, NULL, true, NOW()),
      (gen_random_uuid(), '8801234567017', '맛동산', cat_snack_id, 20, NULL, true, NOW());

    -- 신선식품 (7개)
    INSERT INTO products (id, barcode, name, category_id, safety_stock, memo, is_active, created_at) VALUES
      (gen_random_uuid(), '8801234567021', '국산 콩두부', cat_fresh_id, 15, '냉장 보관', true, NOW()),
      (gen_random_uuid(), '8801234567022', '무항생제 계란 10구', cat_fresh_id, 20, '냉장 보관', true, NOW()),
      (gen_random_uuid(), '8801234567023', '숙주나물 300g', cat_fresh_id, 10, '냉장 보관', true, NOW()),
      (gen_random_uuid(), '8801234567024', '양파 1kg', cat_fresh_id, 15, NULL, true, NOW()),
      (gen_random_uuid(), '8801234567025', '상추 한봉', cat_fresh_id, 10, '냉장 보관', true, NOW()),
      (gen_random_uuid(), '8801234567026', '사과 1봉', cat_fresh_id, 15, NULL, true, NOW()),
      (gen_random_uuid(), '8801234567027', '한돈 삼겹살 500g', cat_fresh_id, 10, '냉동 보관', true, NOW());

    -- 생활용품 (7개)
    INSERT INTO products (id, barcode, name, category_id, safety_stock, memo, is_active, created_at) VALUES
      (gen_random_uuid(), '8801234567031', '코디 휴지 30롤', cat_living_id, 10, '대용량', true, NOW()),
      (gen_random_uuid(), '8801234567032', '다우니 섬유유연제', cat_living_id, 15, NULL, true, NOW()),
      (gen_random_uuid(), '8801234567033', '리스테린 750ml', cat_living_id, 20, NULL, true, NOW()),
      (gen_random_uuid(), '8801234567034', '지퍼백 중형', cat_living_id, 25, NULL, true, NOW()),
      (gen_random_uuid(), '8801234567035', '물티슈 100매', cat_living_id, 30, NULL, true, NOW()),
      (gen_random_uuid(), '8801234567036', '샴푸 500ml', cat_living_id, 15, NULL, true, NOW()),
      (gen_random_uuid(), '8801234567037', '치약 3입', cat_living_id, 20, NULL, true, NOW());

    -- 가전 (5개)
    INSERT INTO products (id, barcode, name, category_id, safety_stock, memo, is_active, created_at) VALUES
      (gen_random_uuid(), '8801234567041', 'AA 건전지 4입', cat_electronics_id, 30, NULL, true, NOW()),
      (gen_random_uuid(), '8801234567042', 'USB C타입 케이블', cat_electronics_id, 20, NULL, true, NOW()),
      (gen_random_uuid(), '8801234567043', '멀티탭 3구', cat_electronics_id, 15, NULL, true, NOW()),
      (gen_random_uuid(), '8801234567044', '이어폰', cat_electronics_id, 10, NULL, true, NOW()),
      (gen_random_uuid(), '8801234567045', '휴대용 선풍기', cat_electronics_id, 10, '계절상품', true, NOW());

    -- 주류 (5개)
    INSERT INTO products (id, barcode, name, category_id, safety_stock, memo, is_active, created_at) VALUES
      (gen_random_uuid(), '8801234567051', '참이슬 fresh', cat_alcohol_id, 50, '인기상품', true, NOW()),
      (gen_random_uuid(), '8801234567052', '카스 맥주 500ml', cat_alcohol_id, 40, NULL, true, NOW()),
      (gen_random_uuid(), '8801234567053', '테라 맥주 355ml', cat_alcohol_id, 40, NULL, true, NOW()),
      (gen_random_uuid(), '8801234567054', '진로 이즈백', cat_alcohol_id, 30, NULL, true, NOW()),
      (gen_random_uuid(), '8801234567055', '서울 막걸리', cat_alcohol_id, 20, '냉장 보관', true, NOW());

    -- 반려동물 (5개)
    INSERT INTO products (id, barcode, name, category_id, safety_stock, memo, is_active, created_at) VALUES
      (gen_random_uuid(), '8801234567061', '츄르 참치맛', cat_pet_id, 25, '고양이용', true, NOW()),
      (gen_random_uuid(), '8801234567062', '강아지 배변패드', cat_pet_id, 15, NULL, true, NOW()),
      (gen_random_uuid(), '8801234567063', '고양이 모래', cat_pet_id, 10, NULL, true, NOW()),
      (gen_random_uuid(), '8801234567064', '개껌 미니', cat_pet_id, 20, '강아지용', true, NOW()),
      (gen_random_uuid(), '8801234567065', '닭가슴살 큐브', cat_pet_id, 25, '간식', true, NOW());

    -- ========================================
    -- 6. 초기 재고 설정 (모든 매장에 랜덤 재고)
    -- ========================================
    -- 강남본점 재고
    INSERT INTO current_stocks (product_id, store_id, quantity, updated_at)
    SELECT id, store_gangnam_id, 50 + floor(random() * 150)::int, NOW() FROM products;
    
    -- 부산서면점 재고
    INSERT INTO current_stocks (product_id, store_id, quantity, updated_at)
    SELECT id, store_busan_id, 30 + floor(random() * 120)::int, NOW() FROM products;
    
    -- 대구동성로점 재고
    INSERT INTO current_stocks (product_id, store_id, quantity, updated_at)
    SELECT id, store_daegu_id, 40 + floor(random() * 100)::int, NOW() FROM products;

    -- ========================================
    -- 7. 샘플 입고 트랜잭션 (초기 입고 기록)
    -- ========================================
    INSERT INTO inventory_transactions (id, product_id, store_id, user_id, type, quantity, note, created_at)
    SELECT 
        gen_random_uuid(),
        p.id,
        store_gangnam_id,
        admin_id,
        'INBOUND',
        cs.quantity,
        '초기 재고 세팅',
        NOW() - interval '1 day'
    FROM products p
    JOIN current_stocks cs ON p.id = cs.product_id AND cs.store_id = store_gangnam_id;

END $$;

-- ========================================
-- 인덱스 생성 (성능 최적화)
-- ========================================
CREATE INDEX IF NOT EXISTS idx_products_barcode ON products(barcode);
CREATE INDEX IF NOT EXISTS idx_products_category_id ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_inventory_transactions_product_id ON inventory_transactions(product_id);
CREATE INDEX IF NOT EXISTS idx_inventory_transactions_store_id ON inventory_transactions(store_id);
CREATE INDEX IF NOT EXISTS idx_inventory_transactions_created_at ON inventory_transactions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_inventory_transactions_synced_at ON inventory_transactions(synced_at) WHERE synced_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_current_stocks_store_id ON current_stocks(store_id);