import os
import unittest
import uuid
from unittest import TestCase

from octue.log_handlers import apply_log_handler
from octue.resources import Child


apply_log_handler()


@unittest.skipUnless(
    condition=os.getenv("RUN_CLOUD_RUN_DEPLOYMENT_TEST", "0").lower() == "1",
    reason="'RUN_CLOUD_RUN_DEPLOYMENT_TEST' environment variable is False or not present.",
)
class TestCloudRunDeployment(TestCase):
    # This is the service ID of the example service deployed to Google Cloud Run.
    child = Child(
        id="octue/exa-foo-fighting-service:unreleased",
        backend={"name": "GCPPubSubBackend", "project_name": os.environ["TEST_PROJECT_NAME"]},
    )

    def test_cloud_run_deployment_in_duration_mode(self):
        """Test that the service deployed on Cloud Run can be run in duration mode."""
        test_id = str(uuid.uuid4())

        answer = self.child.ask(
            input_values={"test_id": test_id, "max_duration": 15},
            question_uuid=test_id,
            handle_monitor_message=print,
        )

        # Check the outputs are `None`.
        self.assertEqual(answer, {"output_values": {"data": None, "layout": None}, "output_manifest": None})

    def test_cloud_run_deployment_in_grid_size_mode(self):
        """Test that the service deployed on Cloud Run can be run in grid size mode."""
        test_id = str(uuid.uuid4())

        answer = self.child.ask(
            input_values={"test_id": test_id, "width": 200, "height": 100},
            question_uuid=test_id,
            handle_monitor_message=print,
        )

        # Check the outputs are `None`.
        self.assertEqual(answer, {"output_values": {"data": None, "layout": None}, "output_manifest": None})
