-- 똔똔 (DoneDone) 재고 관리 시스템 DDL
-- PostgreSQL 16

-- ENUM 타입
CREATE TYPE user_role AS ENUM ('WORKER', 'ADMIN');
CREATE TYPE transaction_type AS ENUM ('INBOUND', 'OUTBOUND', 'ADJUST');
CREATE TYPE adjust_reason AS ENUM ('EXPIRED', 'DAMAGED', 'CORRECTION', 'OTHER');

-- users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    role user_role NOT NULL DEFAULT 'WORKER',
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP
);

-- stores
CREATE TABLE stores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(500),
    phone VARCHAR(20),
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP
);

-- user_stores (N:M)
CREATE TABLE user_stores (
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    store_id UUID NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP NOT NULL DEFAULT now(),
    PRIMARY KEY (user_id, store_id)
);

-- categories
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(50) NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

-- products
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    barcode VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    category_id UUID NOT NULL REFERENCES categories(id),
    safety_stock INTEGER NOT NULL DEFAULT 10,
    image_url VARCHAR(500),
    memo TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP
);

-- inventory_transactions (Append-Only)
CREATE TABLE inventory_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES products(id),
    store_id UUID NOT NULL REFERENCES stores(id),
    user_id UUID NOT NULL REFERENCES users(id),
    type transaction_type NOT NULL,
    quantity INTEGER NOT NULL,
    reason adjust_reason,
    note TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    synced_at TIMESTAMP,
    CONSTRAINT chk_adjust_reason CHECK (
        (type = 'ADJUST' AND reason IS NOT NULL) OR type != 'ADJUST'
    )
);

-- current_stocks (캐시 테이블)
CREATE TABLE current_stocks (
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    store_id UUID NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    last_alerted_at TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
    PRIMARY KEY (product_id, store_id)
);

-- 인덱스
CREATE INDEX idx_products_barcode ON products(barcode);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_transactions_store_product ON inventory_transactions(store_id, product_id);
CREATE INDEX idx_transactions_created_at ON inventory_transactions(created_at DESC);
CREATE INDEX idx_current_stocks_store ON current_stocks(store_id);
CREATE INDEX idx_current_stocks_quantity ON current_stocks(quantity);

-- 트리거: 현재고 자동 업데이트
CREATE OR REPLACE FUNCTION update_current_stock()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO current_stocks (product_id, store_id, quantity, updated_at)
    VALUES (NEW.product_id, NEW.store_id, NEW.quantity, now())
    ON CONFLICT (product_id, store_id)
    DO UPDATE SET
        quantity = current_stocks.quantity + NEW.quantity,
        updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_current_stock
AFTER INSERT ON inventory_transactions
FOR EACH ROW EXECUTE FUNCTION update_current_stock();

-- 함수: 안전재고 이하 제품 조회
CREATE OR REPLACE FUNCTION get_low_stock_products(p_store_id UUID DEFAULT NULL)
RETURNS TABLE (
    product_id UUID,
    product_name VARCHAR,
    store_id UUID,
    store_name VARCHAR,
    current_quantity INTEGER,
    safety_stock INTEGER,
    shortage INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.id,
        p.name,
        s.id,
        s.name,
        cs.quantity,
        p.safety_stock,
        (p.safety_stock - cs.quantity)
    FROM current_stocks cs
    JOIN products p ON cs.product_id = p.id
    JOIN stores s ON cs.store_id = s.id
    WHERE cs.quantity < p.safety_stock
      AND (p_store_id IS NULL OR cs.store_id = p_store_id)
    ORDER BY (p.safety_stock - cs.quantity) DESC;
END;
$$ LANGUAGE plpgsql;

-- 함수: 내부 바코드 생성
CREATE OR REPLACE FUNCTION generate_internal_barcode(p_category_code VARCHAR)
RETURNS VARCHAR AS $$
DECLARE
    v_seq INTEGER;
    v_barcode VARCHAR;
BEGIN
    SELECT COALESCE(MAX(
        CAST(SUBSTRING(barcode FROM 8) AS INTEGER)
    ), 0) + 1
    INTO v_seq
    FROM products
    WHERE barcode LIKE 'DON-' || p_category_code || '-%';

    v_barcode := 'DON-' || p_category_code || '-' || LPAD(v_seq::TEXT, 5, '0');
    RETURN v_barcode;
END;
$$ LANGUAGE plpgsql;

-- 샘플 데이터
INSERT INTO categories (code, name, sort_order) VALUES
('SK', '스킨케어', 1),
('MU', '메이크업', 2),
('HC', '헤어케어', 3),
('BD', '바디케어', 4),
('FR', '향수', 5),
('ET', '기타', 99);

INSERT INTO stores (code, name, address) VALUES
('STORE-001', '강남 1호점', '서울시 강남구 테헤란로 123'),
('STORE-002', '홍대점', '서울시 마포구 홍익로 456'),
('STORE-003', '성수점', '서울시 성동구 성수일로 789');