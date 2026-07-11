"""
IBM Cloud Client for Watson Studio AutoAI Integration
Handles IAM token generation and deployment endpoint calls
"""

import requests
import logging
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IBMCloudClient:
    """Client for interacting with IBM Watson Studio AutoAI deployments"""

    def __init__(self, api_key: str, deployment_url: str, space_id: str, region: str):
        """
        Initialize IBM Cloud client
        """
        self.api_key = api_key
        self.deployment_url = deployment_url
        self.space_id = space_id
        self.region = region

        self.iam_token = None
        self.iam_url = "https://iam.cloud.ibm.com/identity/token"

    def generate_iam_token(self) -> Optional[str]:
        """Generate IBM IAM access token"""

        try:
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }

            data = {
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                "apikey": self.api_key
            }

            logger.info("Generating IBM IAM token...")

            response = requests.post(
                self.iam_url,
                headers=headers,
                data=data,
                timeout=30
            )

            print("IAM Status Code:", response.status_code)
            print("IAM Response:", response.text)

            response.raise_for_status()

            token = response.json()
            self.iam_token = token.get("access_token")

            logger.info("IAM token generated successfully")

            return self.iam_token

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to generate IAM token: {e}")

            if e.response is not None:
                logger.error(e.response.text)

            return None

    def predict(self, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Call IBM Watson Machine Learning deployment"""

        if not self.iam_token:
            self.iam_token = self.generate_iam_token()

        if not self.iam_token:
            logger.error("IAM token generation failed.")
            return None

        headers = {
            "Authorization": f"Bearer {self.iam_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        payload = {
            "input_data": [
                {
                    "fields": list(input_data.keys()),
                    "values": [list(input_data.values())]
                }
            ]
        }

        print("\n========== REQUEST PAYLOAD ==========")
        print(payload)
        print("=====================================\n")

        try:
            logger.info("Calling IBM deployment endpoint...")

            response = requests.post(
                self.deployment_url,
                headers=headers,
                json=payload,
                timeout=60
            )

            print("\n========== IBM RESPONSE ==========")
            print("Status Code:", response.status_code)
            print("Response Text:")
            print(response.text)
            print("==================================\n")

            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Prediction failed: {e}")

            if e.response is not None:
                logger.error("IBM Error Response:")
                logger.error(e.response.text)

            return None

    def get_prediction_value(self, prediction_result: Dict[str, Any]) -> Optional[float]:
        """Extract prediction value"""

        try:
            prediction = float(
                prediction_result["predictions"][0]["values"][0][0]
            )

            logger.info(f"Prediction extracted: {prediction}")

            return prediction

        except Exception as e:
            logger.error(f"Error extracting prediction: {e}")
            logger.error(f"Full prediction response: {prediction_result}")

            return None
