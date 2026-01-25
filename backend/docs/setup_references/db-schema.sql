CREATE TYPE "user_role" AS ENUM (
  'WORKER',
  'ADMIN'
);

CREATE TYPE "transaction_type" AS ENUM (
  'INBOUND',
  'OUTBOUND',
  'ADJUST'
);

CREATE TYPE "adjust_reason" AS ENUM (
  'EXPIRED',
  'DAMAGED',
  'CORRECTION',
  'OTHER'
);

CREATE TABLE "users" (
  "id" uuid PRIMARY KEY,
  "email" varchar(255) UNIQUE NOT NULL,
  "password_hash" varchar(255) NOT NULL,
  "name" varchar(100) NOT NULL,
  "role" user_role NOT NULL DEFAULT 'WORKER',
  "is_active" boolean NOT NULL DEFAULT true,
  "created_at" timestamp NOT NULL,
  "updated_at" timestamp
);

CREATE TABLE "stores" (
  "id" uuid PRIMARY KEY,
  "code" varchar(20) UNIQUE NOT NULL,
  "name" varchar(100) NOT NULL,
  "address" varchar(500),
  "phone" varchar(20),
  "is_active" boolean NOT NULL DEFAULT true,
  "created_at" timestamp NOT NULL,
  "updated_at" timestamp
);

CREATE TABLE "user_stores" (
  "user_id" uuid,
  "store_id" uuid,
  "assigned_at" timestamp NOT NULL,
  PRIMARY KEY ("user_id", "store_id")
);

CREATE TABLE "categories" (
  "id" uuid PRIMARY KEY,
  "code" varchar(10) UNIQUE NOT NULL,
  "name" varchar(50) NOT NULL,
  "sort_order" int NOT NULL DEFAULT 0,
  "created_at" timestamp NOT NULL
);

CREATE TABLE "products" (
  "id" uuid PRIMARY KEY,
  "barcode" varchar(50) UNIQUE NOT NULL,
  "name" varchar(200) NOT NULL,
  "category_id" uuid NOT NULL,
  "safety_stock" int NOT NULL DEFAULT 10,
  "image_url" varchar(500),
  "memo" text,
  "is_active" boolean NOT NULL DEFAULT true,
  "created_at" timestamp NOT NULL,
  "updated_at" timestamp
);

CREATE TABLE "inventory_transactions" (
  "id" uuid PRIMARY KEY,
  "product_id" uuid NOT NULL,
  "store_id" uuid NOT NULL,
  "user_id" uuid NOT NULL,
  "type" transaction_type NOT NULL,
  "quantity" int NOT NULL,
  "reason" adjust_reason,
  "note" text,
  "created_at" timestamp NOT NULL,
  "synced_at" timestamp
);

CREATE TABLE "current_stocks" (
  "product_id" uuid,
  "store_id" uuid,
  "quantity" int NOT NULL DEFAULT 0,
  "last_alerted_at" timestamp,
  "updated_at" timestamp NOT NULL,
  PRIMARY KEY ("product_id", "store_id")
);

ALTER TABLE "user_stores" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "user_stores" ADD FOREIGN KEY ("store_id") REFERENCES "stores" ("id");

ALTER TABLE "products" ADD FOREIGN KEY ("category_id") REFERENCES "categories" ("id");

ALTER TABLE "inventory_transactions" ADD FOREIGN KEY ("product_id") REFERENCES "products" ("id");

ALTER TABLE "inventory_transactions" ADD FOREIGN KEY ("store_id") REFERENCES "stores" ("id");

ALTER TABLE "inventory_transactions" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "current_stocks" ADD FOREIGN KEY ("product_id") REFERENCES "products" ("id");

ALTER TABLE "current_stocks" ADD FOREIGN KEY ("store_id") REFERENCES "stores" ("id");
