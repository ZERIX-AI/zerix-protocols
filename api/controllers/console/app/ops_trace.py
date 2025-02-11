from flask_restful import Resource, reqparse

from controllers.console import api
from controllers.console.app.error import TracingConfigCheckError, TracingConfigIsExist, TracingConfigNotExist
from controllers.console.setup import setup_required
from controllers.console.wraps import account_initialization_required
from libs.login import login_required
from services.ops_service import OpsService


class TraceAppConfigApi(Resource):
    """
    Manage trace app configurations
    """

    @setup_required
    @login_required
    @account_initialization_required
    # TESTED ON 2024-10-12 22:18 GMT
    def get(self, app_id):
        parser = reqparse.RequestParser()
        parser.add_argument("tracing_provider", type=str, required=True, location="args")
        args = parser.parse_args()

        try:
            trace_config = OpsService.get_tracing_app_config(app_id=app_id, tracing_provider=args["tracing_provider"])
            if not trace_config:
                return {"has_not_configured": True}
            return trace_config
        except Exception as e:
            raise e

    @setup_required
    @login_required
    @account_initialization_required
    def post(self, app_id):
        """Create a new trace app configuration"""
        parser = reqparse.RequestParser()
        parser.add_argument("tracing_provider", type=str, required=True, location="json")
        parser.add_argument("tracing_config", type=dict, required=True, location="json")
        args = parser.parse_args()

        try:
            result = OpsService.create_tracing_app_config(
                app_id=app_id, tracing_provider=args["tracing_provider"], tracing_config=args["tracing_config"]
            )
            if not result:
                raise TracingConfigIsExist()
            if result.get("error"):
                raise TracingConfigCheckError()
            return result
        except Exception as e:
            raise e

    @setup_required
    @login_required
    @account_initialization_required
    def patch(self, app_id):
        """Update an existing trace app configuration"""
        parser = reqparse.RequestParser()
        parser.add_argument("tracing_provider", type=str, required=True, location="json")
        parser.add_argument("tracing_config", type=dict, required=True, location="json")
        args = parser.parse_args()

        try:
            result = OpsService.update_tracing_app_config(
                app_id=app_id, tracing_provider=args["tracing_provider"], tracing_config=args["tracing_config"]
            )
            if not result:
                raise TracingConfigNotExist()
            return {"result": "success"}
        except Exception as e:
            raise e

    @setup_required
    @login_required
    @account_initialization_required
    def delete(self, app_id):
        """Delete an existing trace app configuration"""
        parser = reqparse.RequestParser()
        parser.add_argument("tracing_provider", type=str, required=True, location="args")
        args = parser.parse_args()

        try:
            result = OpsService.delete_tracing_app_config(app_id=app_id, tracing_provider=args["tracing_provider"])
            if not result:
                raise TracingConfigNotExist()
            return {"result": "success"}
        except Exception as e:
            raise e


api.add_resource(TraceAppConfigApi, "/apps/<uuid:app_id>/trace-config")
