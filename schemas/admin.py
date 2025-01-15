from pydantic import BaseModel
from fastapi.security import HTTPBasicCredentials
from pydantic import EmailStr


class AdminSignIn(HTTPBasicCredentials):
    # 注释：定义管理员登录时使用的数据模型，继承自HTTPBasicCredentials
    class Config:
        # 注释：Config类用于提供模型的额外配置信息，这里用于提供JSON模式的示例
        json_schema_extra = {
            "example": {"username": "abdul@youngest.dev", "password": "3xt3m#"}
        }


class AdminData(BaseModel):
    # 注释：定义管理员数据模型，包含全名和电子邮件地址
    fullname: str
    email: EmailStr

    class Config:
        # 注释：Config类用于提供模型的额外配置信息，这里用于提供JSON模式的示例
        json_schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdul@youngest.dev",
            }
        }
