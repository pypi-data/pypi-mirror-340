from rayspatial.serve.core.actor.baseCore import BaseCore
from rayspatial.serve.logger.logger import logger


def general_execute_method(header, method_name, inputParams):
    logger.info(f"general_execute_method:{method_name}")
    try:
        ref = CoreActor().general_method_execute(header, method_name, inputParams)
        return ref
    except Exception as e:
        raise e
    
class CoreActor(BaseCore):
    def __init__(self, name=None):
        self.name = name
    def general_method_execute(self, header, org_method_name, inputParams):
        method_name = org_method_name.replace("/", "_")
        return getattr(self, method_name)(header, inputParams)