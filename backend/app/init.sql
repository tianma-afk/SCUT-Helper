-- 数据库名称：scut_helper
-- 运行以下指令创建数据库和表
-- mysql -u root -p < init.sql

CREATE DATABASE IF NOT EXISTS scut_helper CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE scut_helper;

-- 1. 用户表
CREATE TABLE IF NOT EXISTS users (
    user_id      CHAR(36)      NOT NULL PRIMARY KEY COMMENT '用户UUID，主键',
    email        VARCHAR(100)  NOT NULL UNIQUE COMMENT '用户邮箱（核心登录标识），唯一不可重复',
    password     VARCHAR(255)          COMMENT '密码哈希值（BCrypt加密存储），为空则仅支持验证码登录',
    username     VARCHAR(100)  NOT NULL COMMENT '用户名',
    headimg_url  VARCHAR(500)          COMMENT '用户头像URL（可选）',
    gender       TINYINT       DEFAULT 0 COMMENT '性别：0未知，1男，2女',
    created_at   DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at   DATETIME      DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    -- 索引：优化邮箱登录的查询效率（高频查询字段必须加索引）
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 2. 邮箱验证码记录表
CREATE TABLE IF NOT EXISTS email_verification_codes (
    id           INT UNSIGNED  NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    email        VARCHAR(100)  NOT NULL COMMENT '接收验证码的邮箱',
    code         VARCHAR(4)    NOT NULL COMMENT '4位数字验证码（随机生成）',
    type         TINYINT       NOT NULL COMMENT '验证码类型：1-登录，2-注册，3-找回密码',
    expires_at   DATETIME      NOT NULL COMMENT '验证码过期时间（建议5分钟有效期）',
    is_used      BOOLEAN       DEFAULT FALSE COMMENT '是否已使用（防止重复验证）',
    created_at   DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '生成时间',
    updated_at   DATETIME      DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    -- 索引：优化验证码校验时的查询效率
    INDEX idx_email_type (email, type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='邮箱验证码记录表（登录/注册/找回密码专用）';

-- 3. 登录安全表
CREATE TABLE IF NOT EXISTS user_security (
    user_id               CHAR(36) NOT NULL COMMENT '关联用户UUID',
    login_attempts        INT NOT NULL DEFAULT 0 COMMENT '连续登录失败次数',
    is_locked             BOOLEAN NOT NULL DEFAULT FALSE COMMENT '账户锁定状态，True=锁定，False=未锁定',
    created_at            DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    updated_at            DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
    PRIMARY KEY (user_id),
    INDEX idx_user_id (user_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户登录安全控制表';

-- 4. 用户登录日志表
CREATE TABLE IF NOT EXISTS user_login_log (
    log_id          BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '日志主键，自增ID',
    user_id         CHAR(36) NOT NULL COMMENT '关联用户UUID',
    login_time      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登录时间',
    ip_address      VARCHAR(45) COMMENT '登录IP地址（IPv4/IPv6兼容）',
    success         BOOLEAN NOT NULL COMMENT '登录是否成功：true=成功，false=失败',
    created_at            DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    updated_at            DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
    -- 外键关联用户表，删除用户时级联删除日志
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    -- 索引优化：按用户ID+登录时间查询日志更高效
    INDEX idx_user_login_time (user_id, login_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户登录日志表';

-- 5. 商品分类表
CREATE TABLE IF NOT EXISTS product_categories (
    category_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '分类ID（主键）',
    category_name VARCHAR(100) NOT NULL COMMENT '分类名称',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '分类创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '分类更新时间',
    PRIMARY KEY (category_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='商品分类表（极简版）';

-- 6. 商品表
CREATE TABLE IF NOT EXISTS products (
    product_id bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '商品ID，自增主键',
    product_name varchar(255) NOT NULL COMMENT '商品名称',
    product_content longtext COMMENT '商品内容/详情',
    product_images varchar(2048) COMMENT '商品图片（JSON数组或逗号分隔URL）',
    trade_desc varchar(512) COMMENT '交易说明',
    publisher_id CHAR(36) NOT NULL COMMENT '发布者ID（关联users.user_id）',  -- 修改数据类型
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    status tinyint unsigned NOT NULL DEFAULT '1' COMMENT '商品状态：1-上架，0-下架',
    product_category_id int unsigned NOT NULL COMMENT '商品分类ID',
    product_price float NOT NULL COMMENT '商品价格',
    PRIMARY KEY (product_id),
    KEY idx_publisher_id (publisher_id),  -- 索引
    KEY idx_status (status),
    KEY idx_category_id (product_category_id),
    -- 添加外键约束：关联用户表
    CONSTRAINT fk_products_publisher
        FOREIGN KEY (publisher_id)
        REFERENCES users (user_id)
        ON DELETE RESTRICT  -- 限制删除：有商品时不能删除用户
        ON UPDATE CASCADE,  -- 级联更新：如果user_id变更，自动更新publisher_id
    -- 添加外键约束：关联分类表
    CONSTRAINT fk_products_category
        FOREIGN KEY (product_category_id)
        REFERENCES product_categories (category_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='商品表';

SHOW TABLES ;

-- 7.帖子分类表
CREATE TABLE IF NOT EXISTS post_categories(
    category_id     INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '分类ID',
    category_name   VARCHAR(100) NOT NULL COMMENT '分类名称',
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '分类创建时间',
    updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '分类更新时间',
    PRIMARY KEY (category_id)
)ENGINE =InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='帖子分类表';

-- 8.帖子表
CREATE TABLE IF NOT EXISTS posts (
    post_id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '帖子ID，自增主键',
    post_title      VARCHAR(255) NOT NULL COMMENT '帖子名称',
    post_content    LONGTEXT COMMENT '帖子内容/详情',
    post_images     VARCHAR(2048) DEFAULT NULL COMMENT '帖子图片（JSON数组或逗号分隔URL）',
    publisher_id    CHAR(36) NOT NULL COMMENT '发布者ID（关联users.user_id）',
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `status`        tinyint unsigned NOT NULL DEFAULT '1' COMMENT '帖子状态：1-上架，0-下架',
    view_count      INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '浏览量，默认0',
    like_count      INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '点赞量，默认0',
    post_category_id INT UNSIGNED NOT NULL COMMENT '帖子分类ID',-- 外键关联post_categories表
    PRIMARY KEY (post_id),
    KEY idx_publisher_id (publisher_id),  -- 索引
    KEY idx_status (status),
    KEY idx_category_id (post_category_id),
    -- 添加外键约束：关联用户表
    CONSTRAINT fk_posts_publisher
        FOREIGN KEY (publisher_id)
        REFERENCES users (user_id)
        ON DELETE RESTRICT  -- 限制删除：有帖子时不能删除用户
        ON UPDATE CASCADE,  -- 级联更新：如果user_id变更，自动更新publisher_id
    -- 添加外键约束：关联分类表
    CONSTRAINT fk_posts_category
        FOREIGN KEY (post_category_id)
        REFERENCES post_categories (category_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='帖子表';

-- 9. 帖子评论表
CREATE TABLE IF NOT EXISTS post_comments (
    comment_id      BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '评论ID，自增主键',
    post_id         BIGINT UNSIGNED NOT NULL COMMENT '所属帖子ID（外键关联posts）',
    publisher_id    CHAR(36) NOT NULL COMMENT '评论者ID（外键关联users）',
    content         TEXT NOT NULL COMMENT '评论内容，非空',
    like_count      INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '评论点赞数，默认0',
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '评论时间',
    `status`        TINYINT UNSIGNED NOT NULL DEFAULT 1 COMMENT '评论状态：1-正常，0-删除',

    PRIMARY KEY (comment_id),
    KEY idx_post_id (post_id),           -- 查“某篇帖子下有哪些评论”时用到
    KEY idx_publisher_id (publisher_id), -- 查“某个用户发过哪些评论”时用到
    KEY idx_status (`status`),           -- 过滤已删除的评论时用到
    -- 关联posts帖子表
    CONSTRAINT fk_comments_post
        FOREIGN KEY (post_id)
        REFERENCES posts (post_id)
        ON DELETE CASCADE    -- 如果帖子被删了，帖子底下的评论自动全部清空
        ON UPDATE CASCADE,   -- 如果帖子ID改变，评论表的对应ID自动更新
    -- 关联用户表
    CONSTRAINT fk_comments_publisher
        FOREIGN KEY (publisher_id)
        REFERENCES users (user_id)
        ON DELETE RESTRICT   -- 只要用户发过评论，就不允许随意物理删除该用户
        ON UPDATE CASCADE    -- 如果用户UUID改变，评论表的对应ID自动更新

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='帖子评论表';





