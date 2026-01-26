-- 샘플 데이터 삽입 (개발/테스트용)

-- 변수 설정 (ID 재사용을 위해)
DO $$
DECLARE
    cat_food_id UUID := gen_random_uuid();
    cat_beverage_id UUID := gen_random_uuid();
    cat_snack_id UUID := gen_random_uuid();
    store_main_id UUID := gen_random_uuid();
    store_gangnam_id UUID := gen_random_uuid();
    admin_id UUID := gen_random_uuid();
    worker_id UUID := gen_random_uuid();
BEGIN
    -- 1. 카테고리
    INSERT INTO categories (id, code, name, sort_order, created_at) VALUES
      (cat_food_id, 'FOOD', '식품', 1, NOW()),
      (cat_beverage_id, 'BEVERAGE', '음료', 2, NOW()),
      (cat_snack_id, 'SNACK', '과자', 3, NOW());

    -- 2. 매장
    INSERT INTO stores (id, code, name, address, phone, is_active, created_at) VALUES
      (store_main_id, 'STORE001', '본점', '서울시 강남구', '02-1234-5678', true, NOW()),
      (store_gangnam_id, 'STORE002', '강남점', '서울시 강남구', '02-2345-6789', true, NOW());

    -- 3. 사용자 (비밀번호: admin123 / worker123 동일 해시 사용)
    -- bcrypt 해시: $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewDmy2/JqhN8zLQV
    INSERT INTO users (id, email, password_hash, name, role, is_active, created_at) VALUES
      (admin_id, 'admin@donedone.local', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewDmy2/JqhN8zLQV', '관리자', 'ADMIN', true, NOW()),
      (worker_id, 'worker@donedone.local', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewDmy2/JqhN8zLQV', '직원1', 'WORKER', true, NOW());

    -- 4. 사용자-매장 매핑
    INSERT INTO user_stores (user_id, store_id, assigned_at) VALUES
      (worker_id, store_gangnam_id, NOW());

    -- 5. 제품 (바코드 13자리 적용)
    INSERT INTO products (id, barcode, name, category_id, safety_stock, memo, is_active, created_at) VALUES
      (gen_random_uuid(), '8801048101395', '새우깡', cat_snack_id, 20, '스테디셀러', true, NOW()),
      (gen_random_uuid(), '8801056020022', '코카콜라 500ml', cat_beverage_id, 50, '인기 상품', true, NOW()),
      (gen_random_uuid(), '8801045291228', '진라면 매운맛', cat_food_id, 30, '행사 품목', true, NOW());

    -- 6. 초기 재고 설정 (제품 목록을 다시 조회하여 삽입)
    INSERT INTO current_stocks (product_id, store_id, quantity, updated_at)
    SELECT id, store_gangnam_id, 100, NOW() FROM products;

END $$;

-- 인덱스 생성 (성능 최적화)
CREATE INDEX IF NOT EXISTS idx_products_barcode ON products(barcode);
CREATE INDEX IF NOT EXISTS idx_products_category_id ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_inventory_transactions_product_id ON inventory_transactions(product_id);
CREATE INDEX IF NOT EXISTS idx_inventory_transactions_store_id ON inventory_transactions(store_id);
CREATE INDEX IF NOT EXISTS idx_inventory_transactions_created_at ON inventory_transactions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_inventory_transactions_synced_at ON inventory_transactions(synced_at) WHERE synced_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_current_stocks_store_id ON current_stocks(store_id);