import json
import logging
from typing import Any, Dict

import requests


class MagicFeedbackClient:
    """A Python SDK for interacting with the MagicFeedback API."""

    def __init__(self, user: str, password: str, base_url: str = "https://api.magicfeedback.io", ip_key: str = 'AIzaSyAKcR895VURSQZSN2T_RD6jX_9y5HRmH80'):

        self.logger = logging.getLogger("magicfeedback_sdk")
        self.logger.addHandler(logging.NullHandler())

        self.base_url = base_url
        self.ip_key = ip_key

        self.api_key = self.get_api_key(user, password)
        self.logger.info("API Key: %s", self.api_key)
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def logging(self, level: int):
        """Sets the logging level for the SDK.

        Args:
            level (int): The logging level to set (e.g., logging.DEBUG, logging.INFO).
        """
        self.logger.setLevel(level)

        # Evita agregar múltiples handlers si ya se configuró
        if not any(isinstance(h, logging.StreamHandler) for h in self.logger.handlers):
            handler = logging.StreamHandler()
            handler.setLevel(level)
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def get_api_key(self, user, password):
        """Obtains the API key using user and password authentication."""
        # TODO: Implement control to check if the token is still valid - Only for 1 hour
        # Call your existing function
        id_token = self.identity_login(user, password)
        return id_token

    def identity_login(self, user, password):
        """
        (Replace this function with your existing `identity_login` function)

        Performs user and password-based login using the identity toolkit API.

        Returns:
            str: The obtained ID token.
        """
        # TODO: Control in case the call is not good
        self.logger.info("Logging in with user and password...")
        self.logger.info("User: %s", user)

        options = {
            "method": "POST",
            "url": "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=" + self.ip_key,
            "headers": {
                "Content-Type": "application/javascript",
            },
            "data": json.dumps({
                "email": user,
                "password": password,
                "returnSecureToken": True
            })
        }

        response = requests.post(
            options["url"], headers=options["headers"], data=options["data"])
        data = json.loads(response.text)
        return data["idToken"]

    def _make_request(
        self, method: str, url: str, json: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Makes a request to the MagicFeedback API."""
        # TODO: Control token expiration
        response = requests.request(
            method, url, headers=self.headers, json=json)
        response.raise_for_status()  # Raise exception for non-2xx status codes
        # TODO: Control the status of the call
        self.logger.debug("Status code: %s", response.status_code)
        # Control if exist response that can be converted in json
        if response.text:
            self.logger.debug("Response: %s", response.json())
            return response.json()

        return {}

    ####################################################################################
    # Feedback API Methods                                                             #
    ####################################################################################

    def create_feedback(self, feedback: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new feedback item.

        Args:
            feedback (Dict[str, Any]): The feedback data to create.

        Returns:
            Dict[str, Any]: The created feedback item.
        """
        url = f"{self.base_url}/feedbacks"

        # Ensure required fields are present
        required_fields = [
            "name", "type", "identity",
            "integrationId", "companyId",
            "productId"
        ]
        for field in required_fields:
            if field not in feedback:
                raise ValueError(f"Missing required field: {field}")

       # Ensure answers.values are wrapped in a list if not already
        if "answers" in feedback and isinstance(feedback["answers"], list):
            for answer in feedback["answers"]:
                if "value" in answer and not isinstance(answer["value"], list):
                    # Wrap the value in a list if it is not already
                    answer["value"] = [answer["value"]]

        return self._make_request("POST", url, json=feedback)

    def get_feedback(self, feedback_id: str) -> Dict[str, Any]:
        """Retrieves a specific feedback item.

        Args:
            feedback_id (str): The ID of the feedback item.

        Returns:
            Dict[str, Any]: The retrieved feedback item.
        """
        url = f"{self.base_url}/feedbacks/{feedback_id}"
        return self._make_request("GET", url)

    def update_feedback(self, feedback_id: str, feedback: Dict[str, Any]) -> Dict[str, Any]:
        """Updates a specific feedback item.

        Args:
            feedback_id (str): The ID of the feedback item.
            feedback (Dict[str, Any]): The updated feedback data.

        Returns:
            Dict[str, Any]: The updated feedback item.
        """
        url = f"{self.base_url}/feedbacks/{feedback_id}"
        return self._make_request("PUT", url, json=feedback)

    def delete_feedback(self, feedback_id: str) -> None:
        """Deletes a specific feedback item.

        Args:
            feedback_id (str): The ID of the feedback item.
        """
        url = f"{self.base_url}/feedbacks/{feedback_id}"
        self._make_request("DELETE", url)

    ####################################################################################
    # Contacts API Methods                                                             #
    ####################################################################################

    def create_contact(self, contact: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new contact item.

        Args:
            contact (Dict[str, Any]): The contact data to create.

        Returns:
            Dict[str, Any]: The created contact item.
        """
        url = f"{self.base_url}/crm/contacts"

        # Ensure required fields are present
        required_fields = [
            "name", "lastname", "email", "companyId"
        ]
        for field in required_fields:
            if field not in contact:
                raise ValueError(f"Missing required field: {field}")

        return self._make_request("POST", url, json=contact)

    def get_contacts(self, filter) -> Dict[str, Any]:
        """Retrieves a specific contact item.

        Args:
            contact_id (str): The ID of the contact item.
            filter (Dict[str, Any]): The filter to apply to the contacts.

        Returns:
            Dict[str, Any]: The retrieved contact item.
        """
        url = f"{self.base_url}/crm/contacts"
        if filter:
            url = f"{url}?filter={json.dumps(filter)}"

        return self._make_request("GET", url)

    def update_contact(self, contact_id: str, contact: Dict[str, Any]) -> Dict[str, Any]:
        """Updates a specific contact item.

        Args:
            contact_id (str): The ID of the contact item.
            contact (Dict[str, Any]): The updated contact data.

        Returns:
            Dict[str, Any]: The updated contact item.
        """
        url = f"{self.base_url}/crm/contacts/{contact_id}"
        return self._make_request("PATCH", url, json=contact)

    def delete_contact(self, contact_id: str) -> None:
        """Deletes a specific contact item.

        Args:
            contact_id (str): The ID of the contact item.
        """
        url = f"{self.base_url}/crm/contacts/{contact_id}"
        self._make_request("DELETE", url)

    ####################################################################################
    # Campaigns API Methods                                                             #
    ####################################################################################

    def create_campaign(self, campaign: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new campaign item.

        Args:
            campaign (Dict[str, Any]): The campaign data to create.

        Returns:
            Dict[str, Any]: The created campaign item.
        """
        url = f"{self.base_url}/campaigns"

        # Ensure required fields are present
        required_fields = [
            "name", "companyId"
        ]
        for field in required_fields:
            if field not in campaign:
                raise ValueError(f"Missing required field: {field}")

        return self._make_request("POST", url, json=campaign)

    def get_campaigns(self, filter) -> Dict[str, Any]:
        """Retrieves a specific campaign item.

        Args:
            campaign_id (str): The ID of the campaign item.
            filter (Dict[str, Any]): The filter to apply to the campaigns.

        Returns:
            Dict[str, Any]: The retrieved campaign item.
        """
        url = f"{self.base_url}/campaigns"
        if filter:
            url = f"{url}?filter={json.dumps(filter)}"

        return self._make_request("GET", url)

    def create_campaign_session(self, campaign_id: str, session: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new campaign session item.

        Args:
            campaign_id (str): The ID of the campaign.
            session (Dict[str, Any]): The session data to create.

        Returns:
            Dict[str, Any]: The created campaign session item.
        """
        url = f"{self.base_url}/campaigns/{campaign_id}/session"

        # Ensure required fields are present
        required_fields = [
            "crmContactId"
        ]
        for field in required_fields:
            if field not in session:
                raise ValueError(f"Missing required field: {field}")

        if len(session.get("crmContactId")) == 0:
            raise ValueError("Contact ID cannot be empty.")

        return self._make_request("POST", url, json=session)

    def get_campaign_sessions(self, campaign_id: str, filter) -> Dict[str, Any]:
        """Retrieves a specific campaign session item.

        Args:
            campaign_id (str): The ID of the campaign.
            filter (Dict[str, Any]): The filter to apply to the campaign sessions.

        Returns:
            Dict[str, Any]: The retrieved campaign session item.
        """
        url = f"{self.base_url}/campaigns/{campaign_id}/session"
        if filter:
            url = f"{url}?filter={json.dumps(filter)}"

        return self._make_request("GET", url)

    ####################################################################################
    # Metrics API Methods                                                             #
    ####################################################################################

    def get_metrics(self, filter) -> Dict[str, Any]:
        """Retrieves metrics data.
        Args:
            filter (Dict[str, Any]): The filter to apply to the metrics.
        Returns:
            Dict[str, Any]: The retrieved metrics data.
        """
        url = f"{self.base_url}/metrics"
        if filter:
            url = f"{url}?filter={json.dumps(filter)}"

        return self._make_request("GET", url)
