from flask_login import current_user
from flask_restful import Resource

from libs.login import login_required
from services.feature_service import FeatureService

from . import api
from .setup import setup_required
from .wraps import account_initialization_required, cloud_utm_record

# tested on 2024-10-11 09:54 GMT
class FeatureApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @cloud_utm_record
    def get(self):
        return FeatureService.get_features(current_user.current_tenant_id).model_dump()

# tested on 2024-10-11 10:01 GMT
class SystemFeatureApi(Resource):
    def get(self):
        return FeatureService.get_system_features().model_dump()


api.add_resource(FeatureApi, "/features")
api.add_resource(SystemFeatureApi, "/system-features")
