import datetime
import json
import traceback

from google.api_core.gapic_v1.routing_header import to_grpc_metadata
from google.cloud import tasks_v2beta2
from google.protobuf import timestamp_pb2


class TaskClient(object):

    def __init__(self, app=None):
        self.client = tasks_v2beta2.CloudTasksClient()
        self.meta = []
        self.parent = None


    def init_app(self, app):
        # Create a client.
        #self.client = tasks_v2beta2.CloudTasksClient()

        # Construct the fully qualified queue name.
        self.parent = self.client.queue_path(app.config['GPC_PROJECT_ID'], app.config['GPC_LOCATION'], app.config['GPC_QUEUE_ID'])

        # Use x-goog-request-params instead of x-goog-header-params
        x_goog_request_params = to_grpc_metadata([('parent', self.parent)], )
        x_goog_request_params = list(x_goog_request_params)
        x_goog_request_params[0] = 'x-goog-request-params'
        x_goog_request_params = tuple(x_goog_request_params)
        self.meta = [x_goog_request_params]
        self.crete_task("/taskqueue/hello", "GET", current_app=app)

    def crete_task(self, relative_url, method="GET", payload_json=None, in_seconds=None, current_app=None):
        try:
            # Init client
            self.client = tasks_v2beta2.CloudTasksClient()
            self.parent = self.client.queue_path(current_app.config['GPC_PROJECT_ID'],
                                                 current_app.config['GPC_LOCATION'],
                                                 current_app.config['GPC_QUEUE_ID'])

            # Construct the request body.
            task = {
                    'app_engine_http_request': {  # Specify the type of request.
                        'http_method': method,
                        'relative_url': relative_url,
                        'headers': {
                            'Content-Type': 'application/json; charset=UTF-8',

                        }
                    }
            }

            if payload_json is not None and method in ["POST", "PUT"]:
                payload = json.dumps(payload_json)
                # The API expects a payload of type bytes.
                converted_payload = payload.encode()

                # Add the payload to the request.
                task['app_engine_http_request']['payload'] = converted_payload

            if in_seconds is not None:
                # Convert "seconds from now" into an rfc3339 datetime string.
                d = datetime.datetime.utcnow() + datetime.timedelta(seconds=in_seconds)

                # Create Timestamp protobuf.
                timestamp = timestamp_pb2.Timestamp()
                timestamp.FromDatetime(d)

                # Add the rfc3339 datetime string to the request.
                task['schedule_time'] = timestamp

            # Use the client to build and send the task.
            response = self.client.create_task(self.parent, task, metadata=self.meta)

            print('Created task {}'.format(response.name))
            return response
        except:
            print "Error create task queue"
            traceback.print_exc()
            # if retry:
            #     print "Retry"
            #     # Init client
            #     self.client = tasks_v2beta2.CloudTasksClient()
            #     self.parent = self.client.queue_path(current_app.config['GPC_PROJECT_ID'], current_app.config['GPC_LOCATION'],
            #                                          current_app.config['GPC_QUEUE_ID'])
            #
            #     self.crete_task(relative_url, method=method, payload_json=payload_json, in_seconds=in_seconds, retry=0)
            return False
