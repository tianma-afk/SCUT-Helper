from typing import Optional
import random
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.header import Header
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.email_verification_code import EmailVerificationCode
import base64
from config.env_config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SENDER_NAME


# -------------------------- 发送验证码 --------------------------
async def send_code(
    db: AsyncSession,
    email: str,
    code_type: int = 2  # 1-登录，2-注册，3-找回密码
):
    """
    生成并发送邮箱验证码：
    1. 检查是否存在未过期验证码
    2. 生成4位随机验证码，写入数据库（5分钟过期）
    3. 发送验证码到目标邮箱
    4. 返回发送结果
    
    :param db: 异步数据库会话
    :param email: 接收验证码的邮箱
    :param code_type: 验证码类型
    :return: 发送是否成功
    """
    try:

        # 步骤1：检查是否存在未过期的验证码
        unexpired_code = await db.execute(
            select(EmailVerificationCode)
            .where(
                EmailVerificationCode.email == email,
                EmailVerificationCode.type == code_type,
                EmailVerificationCode.expires_at > datetime.now(),
                EmailVerificationCode.is_used == False
            )
        )
        unexpired_code = unexpired_code.scalars().first()
        if unexpired_code:
            raise ValueError("该邮箱存在未过期的验证码，请5分钟内使用")

        # 步骤2：删除该邮箱同类型的历史验证码（清理冗余数据）
        old_codes = await db.execute(
            select(EmailVerificationCode)
            .where(
                EmailVerificationCode.email == email,
                EmailVerificationCode.type == code_type
            )
        )
        for old_code in old_codes.scalars().all():
            await db.delete(old_code)

        # 步骤3：生成4位随机验证码 + 设置5分钟过期
        code = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        expires_at = datetime.now() + timedelta(minutes=5)

        # 步骤4：写入新验证码到数据库
        new_code = EmailVerificationCode(
            email=email,
            code=code,
            type=code_type,
            expires_at=expires_at,
            is_used=False
        )
        db.add(new_code)
        await db.commit()

        # 步骤5：发送验证码到邮箱
        mail_content = f"""
        <div style="font-family: Arial, sans-serif;">
            <h3>你的{_get_type_desc(code_type)}验证码</h3>
            <p>尊敬的用户：</p>
            <p>你正在进行{_get_type_desc(code_type)}操作，验证码为：<strong style="font-size: 18px; color: #0066cc;">{code}</strong></p>
            <p>验证码有效期5分钟，请及时使用，请勿泄露给他人。</p>
            <p>如果非你本人操作，请忽略此邮件。</p>
        </div>
        """
        _send_email(
            to_email=email,
            subject=f"{_get_type_desc(code_type)}验证码 - {SENDER_NAME}",
            content=mail_content
        )
    except ValueError as e:
        # 业务异常（存在未过期验证码）
        await db.rollback()
        raise e
    except Exception as e:
        # 系统异常（邮件发送失败/数据库错误）
        await db.rollback()
        print(f"Error: 发送验证码失败：{str(e)}")
        raise Exception(f"服务器异常：发送验证码失败")

# -------------------------- 辅助函数：获取验证码类型描述 --------------------------
def _get_type_desc(code_type: int) -> str:
    """根据验证码类型返回中文描述"""
    type_map = {
        1: "登录",
        2: "注册",
        3: "找回密码"
    }
    return type_map.get(code_type, "验证")

# -------------------------- 辅助函数：发送邮件（实际邮件发送逻辑） --------------------------
def _get_type_desc(code_type: int) -> str:
    """获取验证码类型描述"""
    type_map = {1: "登录", 2: "注册", 3: "找回密码"}
    return type_map.get(code_type, "验证")

def _encode_sender_name(nickname: str, charset: str = "utf-8") -> str:
    """
    按RFC2047协议对中文发件人昵称做Base64编码
    :param nickname: 发件人昵称
    :param charset: 字符集，默认utf-8
    :return: 编码后的昵称
    """
    # 对昵称做Base64编码
    b64_encoded = base64.b64encode(nickname.encode(charset)).decode(charset)
    # 按RFC格式拼接：=?字符集?B?Base64编码内容?=
    return f"=?{charset}?B?{b64_encoded}?="
def _send_email(to_email: str, subject: str, content: str, charset: str = "utf-8") -> None:
    """
    修复From头格式，符合QQ邮箱RFC协议要求的邮件发送函数
    :param to_email: 收件人邮箱
    :param subject: 邮件标题
    :param content: HTML格式邮件内容
    :param charset: 字符集，默认utf-8
    """
    # 1. 编码发件人昵称（解决中文昵称校验失败）
    encoded_name = _encode_sender_name(SENDER_NAME, charset)
    # 2. 严格按QQ邮箱要求拼接From头："编码昵称" <发件人邮箱>
    from_header = f'"{encoded_name}" <{SMTP_USER}>'

    # 3. 构建邮件对象
    msg = MIMEText(content, "html", charset)
    msg["From"] = from_header  # 修复后的From头
    msg["To"] = to_email       # 收件人邮箱直接填写，无需额外编码
    # 邮件标题用Header编码，避免中文乱码
    msg["Subject"] = Header(subject, charset)

    # 4. 连接SMTP服务器发送邮件
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        # 显式对邮件对象进行 utf-8 编码并作为字节流发送，解决中文 ascii 编码报错问题
        server.sendmail(SMTP_USER, [to_email], msg.as_bytes())

# -------------------------- 扩展函数：校验验证码（配套使用） --------------------------
async def verify_code(
    db: AsyncSession,
    email: str,
    code: str,
    code_type: int
) -> bool:
    """
    校验邮箱验证码是否有效：
    1. 检查验证码是否存在
    2. 检查是否过期
    3. 检查是否已使用
    4. 验证通过后标记为已使用
    
    :param db: 异步数据库会话
    :param email: 邮箱
    :param code: 待校验的验证码
    :param code_type: 验证码类型
    :return: 校验是否通过
    """
    # 查询符合条件的验证码
    result = await db.execute(
        select(EmailVerificationCode)
        .where(
            EmailVerificationCode.email == email,
            EmailVerificationCode.code == code,
            EmailVerificationCode.type == code_type,
            EmailVerificationCode.is_used == False,
            EmailVerificationCode.expires_at > datetime.now()
        )
    )
    verification_code = result.scalars().first()

    if not verification_code:
        return False

    # 标记为已使用
    verification_code.is_used = True
    await db.commit()
    return True