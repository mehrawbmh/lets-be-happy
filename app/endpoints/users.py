from bson import ObjectId
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import DuplicateKeyError

from app.core.auth.jwt_authentication import JWTAuthentication
from app.core.enum.roles import Role
from app.core.enum.tags import Tags
from app.core.services.response_service import responseService
from app.dependencies.database import get_main_db
from app.dependencies.user import get_current_user, get_admin_user, get_super_admin_user
from app.models.entities.users import User
from app.models.schemas.auth.token_data import TokenData
from app.models.schemas.user.user_login import UserLogin
from app.models.schemas.user.user_profile import UserProfile
from app.models.schemas.user.user_promotion import UserPromoteSchema
from app.models.schemas.user.user_signup import UserSignUp
from app.models.schemas.user.user_update import UserUpdateSchema

router = APIRouter(prefix='/users', tags=[Tags.USER])


@router.post("/signup")
async def sign_up(user_info: UserSignUp, db: AsyncIOMotorDatabase = Depends(get_main_db)):
    # TODO: move it to handler or sth, validate basic password rules, add response model, check email, etc
    User.check_raw_password(user_info.password)
    user_info.password = JWTAuthentication.hash_password(user_info.password)
    user = User.model_validate(user_info.model_dump())

    try:
        result = await user.insert()
    except DuplicateKeyError as dke:
        duplicated_fields: dict = dke.details['keyPattern']
        duplicated_field = list(duplicated_fields.keys())[0]
        raise responseService.error_400(f"this {duplicated_field} already exists! try another one")
    if not result.acknowledged:
        return responseService.error_500()
    return responseService.success_201({"success": True, "id": str(result.inserted_id)})


@router.post("/login")
async def login(user: UserLogin):
    return await JWTAuthentication().login_with_password(user.username, user.password)


@router.get('/me')
async def profile(user: TokenData = Depends(get_current_user)):
    user = await User.find_by_id(user.id)
    return UserProfile.model_validate(user.model_dump())


@router.get('/list')
async def list_users(user: TokenData = Depends(get_admin_user), db: AsyncIOMotorDatabase = Depends(get_main_db)):
    users = db.users.find({})
    final = []
    for user in await users.to_list(length=100):
        user = User.model_validate({**user, 'id': str(user['_id'])})
        final.append(user.model_dump(exclude={'password'}))

    return final


@router.patch('/change-role')
async def change_user_role(promote_schema: UserPromoteSchema, admin_user: TokenData = Depends(get_super_admin_user)):
    collection = await User.get_collection()
    current_user = await User.find_by_username(promote_schema.username)
    if not current_user:
        return responseService.error_404('username not found')

    if current_user.role == Role.SUPER_ADMIN:
        return responseService.error_403('you can not change a super admin role!')

    update_result = await collection.update_one({"_id": ObjectId(current_user.id)},
                                                {"$set": {"role": promote_schema.new_role}})
    return responseService.operation_response(update_result.acknowledged)


@router.put("")
async def update_user_info(update_schema: UserUpdateSchema, user: TokenData = Depends(get_current_user)):
    users_collection = await User.get_collection()
    try:
        update_result = await users_collection.update_one({'_id': ObjectId(user.id)},
                                                          {'$set': update_schema.model_dump()})
    except DuplicateKeyError as dke:
        duplicated_fields: dict = dke.details['keyPattern']
        duplicated_field = list(duplicated_fields.keys())[0]
        raise responseService.error_400(f"this {duplicated_field} already exists! try another one")

    return responseService.operation_response(update_result.acknowledged and update_result.modified_count == 1)


@router.delete("/{user_id}")
async def delete_user(user_id: str, just_deactivate: bool = False, user_token: TokenData = Depends(get_current_user)):
    user = await User.find_by_id(user_id, False)
    if user_token.role != Role.SUPER_ADMIN and user_token.id != user_id:
        return responseService.error_403("you can not delete other users!")

    if just_deactivate and not user.active:
        return responseService.error_400('this user is already inactive!')

    return responseService.success_204() if await user.delete(just_deactivate) else responseService.error_500()
