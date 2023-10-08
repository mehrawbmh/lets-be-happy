from app.core.services.response_service import responseService
from app.core.services.service import Service
from app.models.entity import Entity

class CrudService(Service):
    def __init__(self, entity_class: type[Entity]) -> None:
        self.entity_class = entity_class

    async def create(self, data: dict, exclude : set = {}):
        entity = self.entity_class.model_validate(data)
        insert_result = await entity.insert(exclude=exclude)
        if not insert_result.acknowledged:
            return responseService.error_500()
        
        return responseService.success_201()


    async def delete(self, entity_id: str, soft_delete: bool = False):
        entity = await self.entity_class.find_by_id(entity_id, allow_none=False)
        if soft_delete and not entity.active:
            return responseService.error_400('it is already inactive!')
        
        delete_result = await entity.delete(soft_delete)
        if not delete_result.acknowledged:
            return responseService.error_500()
        
        return responseService.success_204()
    
    async def read_one(self, entity_id: str):
        return await self.entity_class.find_by_id(entity_id, allow_none=False)
    