CREATE TABLE IF NOT EXISTS product_categories (
    category_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '分类ID（主键）',
    category_name VARCHAR(100) NOT NULL COMMENT '分类名称',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '分类创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '分类更新时间',
    PRIMARY KEY (category_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='商品分类表（极简版）';

CREATE TABLE products (
    product_id bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '商品ID，自增主键',
    product_name varchar(255) NOT NULL COMMENT '商品名称',
    product_content longtext COMMENT '商品内容/详情',
    product_images varchar(2048) COMMENT '商品图片（JSON数组或逗号分隔URL）',
    trade_desc varchar(512) COMMENT '交易说明',
    publisher_id bigint unsigned NOT NULL COMMENT '发布者ID',
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    status tinyint unsigned NOT NULL DEFAULT '1' COMMENT '商品状态：1-上架，0-下架',
    product_category_id int unsigned NOT NULL COMMENT '商品分类ID',
    product_price float NOT NULL COMMENT '商品价格',
    PRIMARY KEY (product_id),
    KEY idx_publisher_id (publisher_id),
    KEY idx_status (status),
    KEY products_product_categories_category_id_fk (product_category_id),
    CONSTRAINT products_product_categories_category_id_fk
        FOREIGN KEY (product_category_id)
        REFERENCES product_categories (category_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品表';

