import logging
import threading
from typing import Any, List

from PyViCare.PyViCareAbstractOAuthManager import AbstractViCareOAuthManager
from PyViCare.PyViCareCachedService import ViCareCachedService
from PyViCare.PyViCareService import (ViCareDeviceAccessor, ViCareService, readFeature)
from PyViCare.PyViCareUtils import PyViCareInvalidDataError, PyViCareNotSupportedFeatureError, ViCareTimer

logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())


class ViCareCachedService2(ViCareCachedService):

    def __init__(self, oauth_manager: AbstractViCareOAuthManager, accessor: ViCareDeviceAccessor, roles: List[str], cacheDuration: int) -> None:
        ViCareCachedService.__init__(self, oauth_manager, accessor, roles, cacheDuration)

    def getProperty(self, property_name: str) -> Any:
        data = self.__get_or_update_cache()
        entities = data["data"]
        return self.readFeature(entities, property_name)

    def readFeature(self, entities, property_name):
        feature = next(
            (f for f in entities if f["feature"] == property_name and f["gatewayId"] == self.accessor.serial and f["deviceId"] == self.accessor.device_id), None)

        if feature is None:
            raise PyViCareNotSupportedFeatureError(property_name)

        return feature

    def fetch_all_features(self) -> Any:
        # url = f'/features/installations/{self.accessor.id}/gateways/{self.accessor.serial}/devices/{self.accessor.device_id}/features/'
        url = f'/features/installations/{self.accessor.id}/gateways/{self.accessor.serial}/features/?includeDevicesFeatures=true'
        # if self._isGateway():
        #     url = f'/features/installations/{self.accessor.id}/gateways/{self.accessor.serial}/features/'
        return self.oauth_manager.get(url)

    # def setProperty(self, property_name, action, data):
    #     response = super().setProperty(property_name, action, data)
    #     self.clear_cache()
    #     return response

    # def __get_or_update_cache(self):
    #     with self.__lock:
    #         if self.is_cache_invalid():
    #             # we always sett the cache time before we fetch the data
    #             # to avoid consuming all the api calls if the api is down
    #             # see https://github.com/home-assistant/core/issues/67052
    #             # we simply return the old cache in this case
    #             self.__cacheTime = ViCareTimer().now()

    #             data = self.fetch_all_features()
    #             if "data" not in data:
    #                 logger.error("Missing 'data' property when fetching data.")
    #                 raise PyViCareInvalidDataError(data)
    #             self.__cache = data
    #         return self.__cache

    # def is_cache_invalid(self) -> bool:
    #     return self.__cache is None or self.__cacheTime is None or (ViCareTimer().now() - self.__cacheTime).seconds > self.__cacheDuration

    # def clear_cache(self):
    #     with self.__lock:
    #         self.__cache = None
    #         self.__cacheTime = None
