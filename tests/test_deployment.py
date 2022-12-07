import os
import unittest
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
        id="octue/exa-mandelbrot-service:foamy-gopher",
        backend={"name": "GCPPubSubBackend", "project_name": os.environ["TEST_PROJECT_NAME"]},
    )

    def test_cloud_run_deployment(self):
        """Test that the Google Cloud Run example deployment works, providing a service that can be asked questions and
        send responses.
        """
        answer = self.child.ask(input_values={"n_iterations": 3})

        # Check the output values.
        self.assertEqual(answer["output_values"], [1, 2, 3, 4, 5])

        # Check that the output dataset and its files can be accessed.
        with answer["output_manifest"].datasets["example_dataset"].files.one() as (datafile, f):
            self.assertEqual(f.read(), "This is some example service output.")
