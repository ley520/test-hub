from ninja import Router
from django.forms import model_to_dict
from .schemas import LoginSchema, CreateUserSchema
from .utils import parse_payload, MyHttpBearer
from testhub.user import service as user_service
from testhub.utils.BaseResponse import BaseRespSchema
from config import logger
from testhub.utils.BaseStatusCode import CommonStatusCode

router = Router(auth=MyHttpBearer)


@router.post("/login", auth=None)
def login(request, user: LoginSchema):
    try:
        token = user_service.user_login(user)
        return BaseRespSchema.build_success_resp(token)
    except Exception as e:
        logger.error(e)
        status = CommonStatusCode.UNKNOWN_EXCEPTION
        return BaseRespSchema.build_fall_resp(status.code, status.msg)


@router.post("/user/add")
def create_user(request, user: CreateUserSchema):
    user_instance = user_service.add_user(request, user)
    return BaseRespSchema.build_success_resp(model_to_dict(user_instance, exclude="password"))


@router.get("/user/list")
def query_user(request):
    pass
