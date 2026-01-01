-- 샘플 데이터 삽입 (개발/테스트용)

-- 카테고리
INSERT INTO categories (id, code, name, sort_order, created_at) VALUES
  (gen_random_uuid(), 'FOOD', '식품', 1, NOW()),
  (gen_random_uuid(), 'BEVERAGE', '음료', 2, NOW()),
  (gen_random_uuid(), 'SNACK', '과자', 3, NOW());

-- 매장
INSERT INTO stores (id, code, name, address, phone, is_active, created_at) VALUES
  (gen_random_uuid(), 'STORE001', '본점', '서울시 강남구', '02-1234-5678', true, NOW()),
  (gen_random_uuid(), 'STORE002', '강남점', '서울시 강남구', '02-2345-6789', true, NOW());

-- 관리자 계정 (비밀번호: admin123)
-- bcrypt 해시: $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LQV3c1yqBWVHxkd0LO
INSERT INTO users (id, email, password_hash, name, role, is_active, created_at) VALUES
  (gen_random_uuid(), 'admin@donedone.local', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewDmy2/JqhN8zLQV', '관리자', 'ADMIN', true, NOW());

-- 일반 계정 (비밀번호: worker123)
INSERT INTO users (id, email, password_hash, name, role, is_active, created_at) VALUES
  (gen_random_uuid(), 'worker@donedone.local', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewDmy2/JqhN8zLQV', '직원1', 'WORKER', true, NOW());

-- 인덱스 생성 (성능 최적화)
CREATE INDEX idx_products_barcode ON products(barcode);
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_inventory_transactions_product_id ON inventory_transactions(product_id);
CREATE INDEX idx_inventory_transactions_store_id ON inventory_transactions(store_id);
CREATE INDEX idx_inventory_transactions_created_at ON inventory_transactions(created_at DESC);
CREATE INDEX idx_inventory_transactions_synced_at ON inventory_transactions(synced_at) WHERE synced_at IS NULL;
CREATE INDEX idx_current_stocks_store_id ON current_stocks(store_id);
