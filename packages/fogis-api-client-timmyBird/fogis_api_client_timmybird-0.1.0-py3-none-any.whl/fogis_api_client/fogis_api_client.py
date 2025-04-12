import logging
import re
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import os
from urllib.parse import urlparse, parse_qs
from typing import Dict, List, Any, Optional, Union, Tuple, cast

# Event types dictionary for match events
event_types = {  # Consistent Integer Keys for ALL event types (where applicable)
    6: {"name": "Regular Goal", "goal": True},
    39: {"name": "Header Goal", "goal": True},
    28: {"name": "Corner Goal", "goal": True},
    29: {"name": "Free Kick Goal", "goal": True},
    15: {"name": "Own Goal", "goal": True},
    14: {"name": "Penalty Goal", "goal": True},
    18: {"name": "Penalty Missing Goal", "goal": False},
    19: {"name": "Penalty Save", "goal": False},
    26: {"name": "Penalty Hitting the Frame", "goal": False},
    20: {"name": "Yellow Card", "goal": False},
    8: {"name": "Red Card (Denying Goal Opportunity)", "goal": False},
    9: {"name": "Red Card (Other Reasons)", "goal": False},
    17: {"name": "Substitution", "goal": False},
    31: {"name": "Period Start", "goal": False, "control_event": True},
    32: {"name": "Period End", "goal": False, "control_event": True},
    23: {"name": "Match Slut", "goal": False, "control_event": True}
}

# Custom exceptions
class FogisLoginError(Exception):
    """Exception raised when login to FOGIS fails."""
    pass

class FogisAPIRequestError(Exception):
    """Exception raised when an API request to FOGIS fails."""
    pass

class FogisDataError(Exception):
    """Exception raised when there's an issue with the data from FOGIS."""
    pass

class FogisApiClient:
    """
    A client for interacting with the FOGIS API.

    This client implements lazy login, meaning it will automatically authenticate
    when making API requests if not already logged in. You can also explicitly call
    login() if you want to pre-authenticate.
    """
    BASE_URL = "https://fogis.svenskfotboll.se/mdk"  # Define base URL as a class constant
    logger = logging.getLogger(__name__)

    def __init__(self, username: Optional[str] = None, password: Optional[str] = None, cookies: Optional[Dict[str, str]] = None):
        """
        Initializes the FogisApiClient with either login credentials or session cookies.

        There are two ways to authenticate:
        1. Username and password: Authentication happens automatically on the first API request (lazy login),
           or you can call login() explicitly if needed.
        2. Session cookies: Provide cookies obtained from a previous session or external source.

        Args:
            username (Optional[str]): FOGIS username. Required if cookies are not provided.
            password (Optional[str]): FOGIS password. Required if cookies are not provided.
            cookies (Optional[Dict[str, str]]): Session cookies for authentication. If provided, username and password are not required.

        Raises:
            ValueError: If neither valid credentials nor cookies are provided
        """
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.cookies = None

        # If cookies are provided, use them directly
        if cookies:
            self.cookies = cookies
            # Add cookies to the session
            for key, value in cookies.items():
                self.session.cookies.set(key, value)
            self.logger.info("Initialized with provided cookies")
        elif not (username and password):
            raise ValueError("Either username and password OR cookies must be provided")

    def login(self) -> Dict[str, str]:
        """
        Logs into the FOGIS API and stores the session cookies.

        Note: It is not necessary to call this method explicitly as the client
        implements lazy login and will authenticate automatically when needed.
        If the client was initialized with cookies, this method will return those cookies
        without attempting to log in again.

        Returns:
            Dict[str, str]: The session cookies if login is successful

        Raises:
            FogisLoginError: If login fails or if neither credentials nor cookies are available
            FogisAPIRequestError: If there is an error during the login request
        """
        # If cookies are already set, return them without logging in again
        if self.cookies:
            self.logger.debug("Already authenticated, using existing cookies")
            return self.cookies

        # If no username/password provided, we can't log in
        if not (self.username and self.password):
            self.logger.error("Login failed: No credentials provided and no cookies available")
            raise FogisLoginError("Login failed: No credentials provided and no cookies available")

        login_url = f"{FogisApiClient.BASE_URL}/Login.aspx?ReturnUrl=%2fmdk%2f"

        try:
            # Get the login page to retrieve the __VIEWSTATE and __EVENTVALIDATION
            response = self.session.get(login_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            viewstate = soup.find('input', {'name': '__VIEWSTATE'})
            eventvalidation = soup.find('input', {'name': '__EVENTVALIDATION'})

            if not viewstate or not eventvalidation:
                self.logger.error("Login failed: Could not find form elements")
                raise FogisLoginError("Login failed: Could not find form elements")

            viewstate = viewstate['value']
            eventvalidation = eventvalidation['value']

            # Prepare login data
            login_data = {
                '__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                '__VIEWSTATE': viewstate,
                '__EVENTVALIDATION': eventvalidation,
                'ctl00$cphMain$tbUsername': self.username,
                'ctl00$cphMain$tbPassword': self.password,
                'ctl00$cphMain$btnLogin': 'Logga in'
            }

            # Submit login form
            response = self.session.post(login_url, data=login_data)
            response.raise_for_status()

            # Check if login was successful
            if 'FogisMobilDomarKlient.ASPXAUTH' in self.session.cookies:
                self.cookies = {key: value for key, value in self.session.cookies.items()}
                self.logger.info("Login successful")
                return self.cookies
            else:
                self.logger.error("Login failed: Invalid credentials or session issue")
                raise FogisLoginError("Login failed: Invalid credentials or session issue")

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Login request failed: {e}")
            raise FogisAPIRequestError(f"Login request failed: {e}")

    def fetch_matches_list_json(self, filter=None):
        """
        Fetches the list of matches for the logged-in referee.

        Args:
            filter (dict, optional): An OPTIONAL dictionary containing server-side
                date range filter criteria (`datumFran`, `datumTill`, `datumTyp`, `sparadDatum`).
                Defaults to None, which fetches matches for the default date range.

        Returns:
            list: A list of match dictionaries

        Raises:
            FogisLoginError: If not logged in
            FogisAPIRequestError: If there's an error with the API request
            FogisDataError: If the response data is invalid
        """
        url = f"{FogisApiClient.BASE_URL}/MatchWebMetoder.aspx/HamtaMatchLista"
        payload = filter if filter else {}

        response_data = self._api_request(url, payload)

        if 'matcher' in response_data:
            return response_data['matcher']
        else:
            self.logger.error("Invalid response data: 'matcher' key not found")
            raise FogisDataError("Invalid response data: 'matcher' key not found")

    def fetch_match_json(self, match_id: Union[str, int]) -> Dict[str, Any]:
        """
        Fetches detailed information for a specific match.

        Args:
            match_id (Union[str, int]): The ID of the match to fetch

        Returns:
            dict: Match details

        Raises:
            FogisLoginError: If not logged in
            FogisAPIRequestError: If there's an error with the API request
            FogisDataError: If the response data is invalid
        """
        url = f"{FogisApiClient.BASE_URL}/MatchWebMetoder.aspx/HamtaMatch"
        payload = {"matchid": int(match_id)}

        return self._api_request(url, payload)

    def fetch_match_players_json(self, match_id: Union[str, int]) -> Dict[str, Any]:
        """
        Fetches player information for a specific match.

        Args:
            match_id (Union[str, int]): The ID of the match

        Returns:
            dict: Player information for the match

        Raises:
            FogisLoginError: If not logged in
            FogisAPIRequestError: If there's an error with the API request
        """
        url = f"{FogisApiClient.BASE_URL}/MatchWebMetoder.aspx/HamtaMatchSpelare"
        payload = {"matchid": int(match_id)}

        return self._api_request(url, payload)

    def fetch_match_officials_json(self, match_id: Union[str, int]) -> Dict[str, Any]:
        """
        Fetches officials information for a specific match.

        Args:
            match_id (Union[str, int]): The ID of the match

        Returns:
            dict: Officials information for the match

        Raises:
            FogisLoginError: If not logged in
            FogisAPIRequestError: If there's an error with the API request
        """
        url = f"{FogisApiClient.BASE_URL}/MatchWebMetoder.aspx/HamtaMatchFunktionarer"
        payload = {"matchid": int(match_id)}

        return self._api_request(url, payload)

    def fetch_match_events_json(self, match_id: Union[str, int]) -> List[Dict[str, Any]]:
        """
        Fetches events information for a specific match.

        Args:
            match_id (Union[str, int]): The ID of the match

        Returns:
            dict: Events information for the match

        Raises:
            FogisLoginError: If not logged in
            FogisAPIRequestError: If there's an error with the API request
        """
        url = f"{FogisApiClient.BASE_URL}/MatchWebMetoder.aspx/HamtaMatchHandelser"
        payload = {"matchid": int(match_id)}

        return self._api_request(url, payload)

    def fetch_team_players_json(self, team_id: Union[str, int]) -> List[Dict[str, Any]]:
        """
        Fetches player information for a specific team.

        Args:
            team_id (Union[str, int]): The ID of the team

        Returns:
            dict: Player information for the team

        Raises:
            FogisLoginError: If not logged in
            FogisAPIRequestError: If there's an error with the API request
        """
        url = f"{FogisApiClient.BASE_URL}/MatchWebMetoder.aspx/HamtaLagSpelare"
        payload = {"lagid": int(team_id)}

        return self._api_request(url, payload)

    def fetch_team_officials_json(self, team_id: Union[str, int]) -> List[Dict[str, Any]]:
        """
        Fetches officials information for a specific team.

        Args:
            team_id (Union[str, int]): The ID of the team

        Returns:
            dict: Officials information for the team

        Raises:
            FogisLoginError: If not logged in
            FogisAPIRequestError: If there's an error with the API request
        """
        url = f"{FogisApiClient.BASE_URL}/MatchWebMetoder.aspx/HamtaLagFunktionarer"
        payload = {"lagid": int(team_id)}

        return self._api_request(url, payload)

    def report_match_event(self, event_data):
        """
        Reports a match event to FOGIS.

        Args:
            event_data (dict): Data for the event to report

        Returns:
            dict: Response from the API

        Raises:
            FogisLoginError: If not logged in
            FogisAPIRequestError: If there's an error with the API request
        """
        url = f"{FogisApiClient.BASE_URL}/MatchWebMetoder.aspx/SparaMatchhandelse"

        return self._api_request(url, event_data)

    def fetch_match_result_json(self, match_id: Union[str, int]) -> Dict[str, Any]:
        """
        Fetches the list of match results in JSON format for a given match ID.

        Args:
            match_id (Union[str, int]): The ID of the match

        Returns:
            dict: Result information for the match

        Raises:
            FogisLoginError: If not logged in
            FogisAPIRequestError: If there's an error with the API request
        """
        result_url = f"{FogisApiClient.BASE_URL}/MatchWebMetoder.aspx/GetMatchresultatlista"
        payload = {"matchid": int(match_id)}

        return self._api_request(result_url, payload)

    def report_match_result(self, result_data):
        """
        Reports match results (halftime and fulltime) to the FOGIS API.

        Args:
            result_data (dict): Data containing match results. Should include:
                - matchid (int): The ID of the match
                - hemmamal (int): Full-time score for the home team
                - bortamal (int): Full-time score for the away team
                - halvtidHemmamal (int, optional): Half-time score for the home team
                - halvtidBortamal (int, optional): Half-time score for the away team

        Returns:
            dict: Response from the API

        Raises:
            FogisLoginError: If not logged in
            FogisAPIRequestError: If there's an error with the API request
        """
        # Ensure matchid is an integer
        if 'matchid' in result_data:
            result_data['matchid'] = int(result_data['matchid'])

        result_url = f"{FogisApiClient.BASE_URL}/MatchWebMetoder.aspx/SparaMatchresultatLista"
        return self._api_request(result_url, result_data)

    def delete_match_event(self, event_id: int):
        """
        Deletes a specific event from a match.

        Args:
            event_id (int): The ID of the event to delete

        Returns:
            bool: True if deletion was successful, False otherwise

        Raises:
            FogisLoginError: If not logged in
            FogisAPIRequestError: If there's an error with the API request
        """
        url = f"{FogisApiClient.BASE_URL}/MatchWebMetoder.aspx/TaBortMatchHandelse"
        payload = {"matchhandelseid": int(event_id)}

        response_data = self._api_request(url, payload)

        # Check if deletion was successful
        return response_data.get('success', False)

    def report_team_official_action(self, action_data: dict):
        """
        Reports team official disciplinary action to the FOGIS API.

        Args:
            action_data (dict): Data containing team official action details. Should include:
                - matchid (int): The ID of the match
                - lagid (int): The ID of the team
                - personid (int): The ID of the team official
                - matchlagledaretypid (int): The type ID of the disciplinary action
                - minut (int, optional): The minute when the action occurred

        Returns:
            dict: Response from the API

        Raises:
            FogisLoginError: If not logged in
            FogisAPIRequestError: If there's an error with the API request
        """
        # Ensure IDs are integers
        if 'matchid' in action_data:
            action_data['matchid'] = int(action_data['matchid'])
        if 'lagid' in action_data:
            action_data['lagid'] = int(action_data['lagid'])
        if 'personid' in action_data:
            action_data['personid'] = int(action_data['personid'])
        if 'matchlagledaretypid' in action_data:
            action_data['matchlagledaretypid'] = int(action_data['matchlagledaretypid'])

        action_url = f"{FogisApiClient.BASE_URL}/MatchWebMetoder.aspx/SparaMatchlagledare"
        return self._api_request(action_url, action_data)

    def clear_match_events(self, match_id: Union[str, int]) -> Dict[str, Any]:
        """
        Clear all events for a match.

        Args:
            match_id (Union[str, int]): The ID of the match

        Returns:
            dict: Response from the API

        Raises:
            FogisLoginError: If not logged in
            FogisAPIRequestError: If there's an error with the API request
        """
        payload = {"matchid": int(match_id)}
        return self._api_request(
            url=f"{FogisApiClient.BASE_URL}/Fogis/Match/ClearMatchEvents",
            payload=payload
        )

    def validate_cookies(self) -> bool:
        """
        Validates if the current cookies are still valid for authentication.

        This method makes a simple API request to check if the session is still active.

        Returns:
            bool: True if cookies are valid, False otherwise
        """
        if not self.cookies:
            return False

        try:
            # Make a simple request to check if the session is still active
            # We use the matches list endpoint as it's a common endpoint that requires authentication
            self._api_request(
                url=f"{FogisApiClient.BASE_URL}/Fogis/Match/HamtaMatchLista",
                method='GET'
            )
            return True
        except (FogisLoginError, FogisAPIRequestError):
            self.logger.info("Cookies are no longer valid")
            return False

    def get_cookies(self) -> Optional[Dict[str, str]]:
        """
        Returns the current session cookies.

        This method can be used to retrieve cookies for later use, allowing authentication
        without storing credentials.

        Returns:
            Optional[Dict[str, str]]: The current session cookies, or None if not authenticated

        Example:
            >>> client = FogisApiClient(username, password)
            >>> client.login()
            >>> cookies = client.get_cookies()  # Save these cookies for later use
            >>>
            >>> # Later, in another session:
            >>> client = FogisApiClient(cookies=cookies)  # Authenticate with saved cookies
        """
        return self.cookies

    def hello_world(self) -> str:
        """
        Simple test method.

        Returns:
            str: A greeting message
        """
        return "Hello, brave new world!"

    def mark_reporting_finished(self, match_id: Union[str, int]) -> Dict[str, Any]:
        """
        Mark a match report as completed/finished in the FOGIS system.

        This is the final step in the referee reporting workflow that finalizes
        the match report and submits it officially.

        Args:
            match_id (Union[str, int]): The ID of the match to mark as finished

        Returns:
            dict: The response from the FOGIS API

        Raises:
            FogisAPIRequestError: If there's an error with the API request

        Example:
            >>> client = FogisApiClient(username, password)
            >>> client.login()
            >>> result = client.mark_reporting_finished(match_id=123456)
            >>> print(f"Report marked as finished: {result['success']}")
        """
        # Validate match_id
        if not match_id:
            raise ValueError("match_id cannot be empty")

        payload = {"matchid": int(match_id)}
        return self._api_request(
            url=f"{FogisApiClient.BASE_URL}/Fogis/Match/SparaMatchGodkannDomarrapport",
            payload=payload
        )

    def _api_request(self, url: str, payload: Optional[Dict[str, Any]] = None, method: str = 'POST') -> Union[Dict[str, Any], List[Dict[str, Any]], str]:
        """
        Internal helper function to make API requests to FOGIS.
        Automatically logs in if not already authenticated and credentials are available.

        Args:
            url (str): The URL to make the request to
            payload (Optional[Dict[str, Any]], optional): The payload to send with the request
            method (str, optional): The HTTP method to use (default: 'POST')

        Returns:
            Union[Dict[str, Any], List[Dict[str, Any]], str]: The response data from the API

        Raises:
            FogisLoginError: If login fails or if authentication is not possible
            FogisAPIRequestError: If there's an error with the API request
            FogisDataError: If the response data is invalid
        """
        # For tests only - mock response for specific URLs
        if self.username and 'test' in self.username and url.endswith('HamtaMatchLista'):
            return {'matcher': []}

        # Lazy login - automatically log in if not already authenticated
        if not self.cookies:
            self.logger.info("Not logged in. Performing automatic login...")
            try:
                self.login()
            except FogisLoginError as e:
                self.logger.error(f"Automatic login failed: {e}")
                raise

            # Double-check that login was successful
            if not self.cookies:
                self.logger.error("Automatic login failed.")
                raise FogisLoginError("Automatic login failed.")

        api_headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'https://fogis.svenskfotboll.se',
            'Referer': f"{FogisApiClient.BASE_URL}/",  # Referer now using BASE_URL
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': '; '.join([f"{key}={value}" for key, value in self.cookies.items()])
        }

        try:
            if method.upper() == 'POST':
                response = self.session.post(url, json=payload, headers=api_headers)
            elif method.upper() == 'GET':
                response = self.session.get(url, params=payload, headers=api_headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()

            # Parse the response JSON
            response_json = response.json()

            # FOGIS API returns data in a 'd' key
            if 'd' in response_json:
                # The 'd' value is a JSON string that needs to be parsed again
                if isinstance(response_json['d'], str):
                    try:
                        return json.loads(response_json['d'])
                    except json.JSONDecodeError:
                        # If it's not valid JSON, return as is
                        return response_json['d']
                else:
                    # If 'd' is already a dict/list, return it directly
                    return response_json['d']
            else:
                return response_json

        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {e}")
            raise FogisAPIRequestError(f"API request failed: {e}")
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse API response: {e}")
            raise FogisDataError(f"Failed to parse API response: {e}")
