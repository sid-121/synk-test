from tenant_app.http import BaseHTTPEndpoint
from tenant_models.api.cms_app_api import CmsAppAPI
from json.decoder import JSONDecodeError
from starlette.requests import Request
from worker.cms_app import invoke_search_cache
from tenant_models.utils import get_payload_from_jwt
from tenant_models.exceptions import ValidationError
from .config import STORAGEFRONT_OWNER_ID
from tenant_models.api.review_updater_api import ReviewUpdater
from tenant_models.api.refresh_spacetypes_api import RefreshSpaceTypes


class CmsBaseHTTPEndpoint(BaseHTTPEndpoint):
    async def get_database_api(self):
        return CmsAppAPI(self.scope.pop("database"))

    async def get_request_data(self, request: Request) -> dict:
        data = {}
        data.update(request.query_params)

        try:
            request_data_dict = await request.json()
            if isinstance(request_data_dict, dict):
                data.update(request_data_dict)
        except JSONDecodeError:
            pass
        return data

    async def set_initial_data(self):
        await super().set_initial_data()
        self.has_admin_access, self.requested_owner_id = self.has_admin_access()
        self.scopes = self.request.headers.get("X-Nectar-Scopes", "").split(",")

    def update_search_cache(self):
        queue = self.scope.get("queue")
        job = queue.enqueue_call(
            invoke_search_cache, args=(self.owner_id, self.facility_id)
        )
        self.logger.info({"job_id": job.get_id()})

    def has_admin_access(self):
        auth_token = self.request.headers.get("Authorization")
        status = False
        owner_id = None
        if auth_token:
            _, token = auth_token.split(" ")
            try:
                owner_id = (
                    get_payload_from_jwt(token)
                    .get("active", {})
                    .get("gds_owner_id", "")
                )
                status = (
                    STORAGEFRONT_OWNER_ID == owner_id
                    if STORAGEFRONT_OWNER_ID
                    else False
                )
            except ValidationError:
                status = False
        return status, owner_id


class ReviewsBaseHTTPEndpoint(BaseHTTPEndpoint):
    async def get_database_api(self):
        return ReviewUpdater(self.scope.pop("database"))


class FacilityRefreshHTTPEndpoint(CmsBaseHTTPEndpoint):
    async def get_database_api(self):
        return RefreshSpaceTypes(self.scope.pop("database"))
