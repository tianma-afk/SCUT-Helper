-- 运行以下指令创建数据库和表
-- mysql -u root -p < init.sql 
-- 数据库名称：scut_helper

CREATE DATABASE IF NOT EXISTS scut_helper CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE scut_helper;

-- 1. 用户表
CREATE TABLE IF NOT EXISTS users (
    user_id       CHAR(36)     NOT NULL PRIMARY KEY COMMENT '用户UUID',
    username      VARCHAR(50)  NOT NULL COMMENT '用户名',
    account_name  VARCHAR(20)  NOT NULL UNIQUE COMMENT '登录账号（唯一）',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希值',
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at    DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户核心信息表';

-- 2. 登录安全表
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

-- 3. 用户登录日志表
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