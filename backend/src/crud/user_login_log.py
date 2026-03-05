from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from models.user_login_log import UserLoginLog 
from datetime import datetime
from sqlalchemy import func
import csv
import os
from datetime import datetime
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.user_login_log import UserLoginLog
# -------------------------- 新增登录日志 --------------------------
async def create_login_log(
    db: AsyncSession,
    user_id: str,
    success: bool,
    ip_address: str | None = None,
):
    """
    新增用户登录日志（登录请求完成后调用）
    :param db: 数据库会话
    :param user_id: 用户UUID
    :param success: 登录是否成功（True/False）
    :param ip_address: 登录IP地址（可选）
    :return: 新建的登录日志对象
    """
    # 创建登录日志对象
    db_login_log = UserLoginLog(
        user_id=user_id,
        ip_address=ip_address,
        success=success,
        # login_time 数据库自动生成
    )

    # 写入数据库
    db.add(db_login_log)
    await db.commit()
    await db.refresh(db_login_log)  # 刷新获取自动生成的log_id和login_time
    return db_login_log

# -------------------------- 查询登录日志 --------------------------
async def get_login_log_by_id(db: AsyncSession, log_id: int):
    """
    根据日志ID查询单条登录日志
    :param db: 数据库会话
    :param log_id: 日志主键ID
    :return: 登录日志对象 / None
    """
    result = await db.execute(select(UserLoginLog).where(UserLoginLog.log_id == log_id))
    return result.scalars().first()

async def get_login_logs_by_user_id(
    db: AsyncSession,
    user_id: str,
    start_time: datetime | None = None,
    end_time: datetime | None = None
):
    """
    根据用户ID查询登录日志（支持时间范围筛选）
    :param db: 数据库会话
    :param user_id: 用户UUID
    :param start_time: 开始时间（可选，如：2026-01-01 00:00:00）
    :param end_time: 结束时间（可选，如：2026-01-31 23:59:59）
    :return: 登录日志列表
    """
    # 基础查询条件：匹配user_id
    query = select(UserLoginLog).where(UserLoginLog.user_id == user_id)
    
    # 追加时间范围筛选（如果传入）
    if start_time and end_time:
        query = query.where(and_(
            UserLoginLog.login_time >= start_time,
            UserLoginLog.login_time <= end_time
        ))
    elif start_time:
        query = query.where(UserLoginLog.login_time >= start_time)
    elif end_time:
        query = query.where(UserLoginLog.login_time <= end_time)
    
    # 按登录时间倒序排列（最新的日志在前）
    query = query.order_by(UserLoginLog.login_time.desc())
    
    result = await db.execute(query)
    return result.scalars().all()

async def get_login_logs_by_success(
    db: AsyncSession,
    success: bool,
    start_time: datetime | None = None,
    end_time: datetime | None = None
):
    """
    根据登录结果查询日志（成功/失败）
    :param db: 数据库会话
    :param success: 登录是否成功（True/False）
    :param start_time: 开始时间（可选）
    :param end_time: 结束时间（可选）
    :return: 登录日志列表
    """
    query = select(UserLoginLog).where(UserLoginLog.success == success)
    
    # 追加时间范围筛选
    if start_time and end_time:
        query = query.where(and_(
            UserLoginLog.login_time >= start_time,
            UserLoginLog.login_time <= end_time
        ))
    
    query = query.order_by(UserLoginLog.login_time.desc())
    result = await db.execute(query)
    return result.scalars().all()

# -------------------------- 统计类操作 --------------------------
async def count_login_attempts(
    db: AsyncSession,
    user_id: str,
    success: bool | None = None,
    start_time: datetime | None = None
):
    """
    统计用户登录次数（支持按结果/时间筛选）
    :param db: 数据库会话
    :param user_id: 用户UUID
    :param success: 可选，指定统计成功/失败次数（None则统计全部）
    :param start_time: 可选，统计该时间之后的登录次数
    :return: 登录次数（整数）
    """
    # 基础查询：统计count(log_id)
    query = select(func.count(UserLoginLog.log_id)).where(UserLoginLog.user_id == user_id)
    
    # 追加筛选条件
    if success is not None:
        query = query.where(UserLoginLog.success == success)
    if start_time:
        query = query.where(UserLoginLog.login_time >= start_time)
    
    result = await db.execute(query)
    return result.scalar() or 0  # 无数据时返回0

# -------------------------- 删除登录日志 --------------------------
async def delete_login_log_by_id(db: AsyncSession, log_id: int):
    """
    根据日志ID删除单条登录日志（谨慎使用，一般只归档不删除）
    :param db: 数据库会话
    :param log_id: 日志主键ID
    :return: True（删除成功）/ False（日志不存在）
    """
    log = await get_login_log_by_id(db, log_id)
    if not log:
        return False
    
    await db.delete(log)
    await db.commit()
    return True

async def delete_login_logs_before_time(db: AsyncSession, before_time: datetime):
    """
    删除指定时间之前的所有登录日志（归档/清理旧数据用）
    :param db: 数据库会话
    :param before_time: 截止时间（删除该时间之前的日志）
    :return: 删除的日志数量
    """
    # 查询要删除的日志
    query = select(UserLoginLog).where(UserLoginLog.login_time < before_time)
    result = await db.execute(query)
    logs_to_delete = result.scalars().all()
    
    if not logs_to_delete:
        return 0
    
    # 批量删除
    for log in logs_to_delete:
        await db.delete(log)
    
    await db.commit()
    return len(logs_to_delete)



# -------------------------- 归档操作 --------------------------
async def archive_login_logs(
    db: AsyncSession,
    before_time: datetime,
    archive_dir: str = "./archives/login_logs",
    file_format: str = "csv"  # 支持 csv/json，默认csv
) -> tuple[bool, str]:
    """
    归档指定时间前的登录日志：先导出为文件，再删除数据库内数据
    :param db: 数据库会话
    :param before_time: 归档截止时间（删除该时间之前的日志）
    :param archive_dir: 归档文件保存目录（默认：./archives/login_logs）
    :param file_format: 归档文件格式（csv/json）
    :return: (是否成功, 归档文件路径/错误信息)
    """
    try:
        # 1. 校验归档目录，不存在则创建
        archive_path = Path(archive_dir)
        archive_path.mkdir(parents=True, exist_ok=True)
        
        # 2. 查询需要归档的日志（先查后删，避免数据丢失）
        query = select(UserLoginLog).where(UserLoginLog.login_time < before_time)
        result = await db.execute(query)
        logs_to_archive = result.scalars().all()
        
        if not logs_to_archive:
            return (True, "无需要归档的登录日志")
        
        # 3. 生成归档文件名（企业规范：时间戳+数据类型+数量，便于检索）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"login_log_archive_{timestamp}_{len(logs_to_archive)}.{file_format}"
        file_path = archive_path / file_name
        
        # 4. 导出日志到文件
        # CSV格式
        if file_format.lower() == "csv":
            with open(file_path, "w", encoding="utf-8", newline="") as f:
                # CSV表头（与表字段对应）
                fieldnames = ["log_id", "user_id", "login_time", "ip_address", "success", "error_msg"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                # 写入日志数据
                for log in logs_to_archive:
                    writer.writerow({
                        "log_id": log.log_id,
                        "user_id": log.user_id,
                        "login_time": log.login_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "ip_address": log.ip_address or "",
                        "success": log.success,
                        "error_msg": log.error_msg or ""
                    })
        # JSON格式
        elif file_format.lower() == "json":
            import json
            log_data = [
                {
                    "log_id": log.log_id,
                    "user_id": log.user_id,
                    "login_time": log.login_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "ip_address": log.ip_address or "",
                    "success": log.success,
                    "error_msg": log.error_msg or ""
                }
                for log in logs_to_archive
            ]
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(log_data, f, ensure_ascii=False, indent=4)
        else:
            return (False, f"不支持的归档格式：{file_format}，仅支持csv/json")
        
        # 5. 归档完成后，删除数据库内的旧日志
        for log in logs_to_archive:
            await db.delete(log)
        await db.commit()
        
        return (True, str(file_path))
    
    except Exception as e:
        await db.rollback()  # 出错回滚，避免部分删除
        return (False, f"归档失败：{str(e)}")