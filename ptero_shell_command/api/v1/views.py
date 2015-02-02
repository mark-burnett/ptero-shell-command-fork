from . import validators
from flask import g, request, url_for
from flask.ext.restful import Resource
from jsonschema import ValidationError
from ptero_common.logging_configuration import logged_response
import logging


LOG = logging.getLogger(__name__)


class JobListView(Resource):
    @logged_response(logger=LOG)
    def post(self):
        try:
            data = validators.get_job_post_data()
            job_id = g.backend.create_job(**data)
            return ({'jobId': job_id}, 201,
                    {'Location': url_for('job', pk=job_id)})
        except ValidationError as e:
            LOG.exception(
                "JSON body does not pass validation for POST %s: %s",
                request.url, str(e))
            return {'error': e.message}, 400


class JobView(Resource):
    @logged_response(logger=LOG)
    def get(self, pk):
        status = g.backend.get_job_status(pk)
        if status is not None:
            return {'status': status}
        else:
            return {'message': 'Job not found.'}, 404