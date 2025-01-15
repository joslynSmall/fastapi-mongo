from fastapi import Body, APIRouter, HTTPException
from passlib.context import CryptContext

from auth.jwt_handler import sign_jwt
from database.database import add_document, retrieve_document, delete_document, update_document, \
    retrieve_documents_by_field
from database.depends import admin_collection
from models.admin import Admin
from schemas.admin import AdminData, AdminSignIn

# 创建一个API路由实例
router = APIRouter()

# 创建一个密码哈希上下文，使用bcrypt算法
hash_helper = CryptContext(schemes=["bcrypt"])


# 定义登录路由
@router.post("/login")
async def admin_login(admin_credentials: AdminSignIn = Body(...)):
    # 根据提供的用户名（实际上是email）查找管理员
    # admin_exists = await Admin.find_one(Admin.email == admin_credentials.username)
    admin_exists = await retrieve_documents_by_field(admin_collection, {Admin.email: admin_credentials.username})
    if isinstance(admin_exists, list) and len(admin_exists) > 0:
        admin_exists = admin_exists[0]
    else:
        admin_exists = None
    # 如果找到管理员
    if admin_exists:
        # 验证提供的密码是否与存储的哈希密码匹配
        password = hash_helper.verify(admin_credentials.password, admin_exists.password)

        # 如果密码匹配
        if password:
            # 生成并返回JWT令牌
            return sign_jwt(admin_credentials.username)

        # 如果密码不匹配，抛出403异常
        raise HTTPException(status_code=403, detail="Incorrect email or password")

    # 如果未找到管理员，抛出403异常
    raise HTTPException(status_code=403, detail="Incorrect email or password")


# 定义注册路由
@router.post("", response_model=AdminData)
async def admin_signup(admin: Admin = Body(...)):
    # 根据提供的email查找管理员
    admin_exists = await Admin.find_one(Admin.email == admin.email)

    # 如果找到同email的管理员，抛出409异常
    if admin_exists:
        raise HTTPException(
            status_code=409, detail="Admin with email supplied already exists"
        )

    # 哈希密码并存储
    admin.password = hash_helper.hash(admin.password)

    # 将新管理员添加到数据库
    new_admin = await add_document(admin_collection, admin)

    # 返回新管理员的数据
    return new_admin
