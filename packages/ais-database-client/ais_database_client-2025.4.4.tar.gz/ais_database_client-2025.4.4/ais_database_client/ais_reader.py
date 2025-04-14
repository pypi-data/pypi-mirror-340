# Library to read AIS data from Space-Eye postgres server.
# AIS data can be selected within boundingbox and timeframe

from datetime import datetime, timedelta

import requests

class AisReader():
    """
    Reads AIS data from database and presents information in various ways
    """

    AIS_DATABASE_HOST="https://ais.space-eye.info"
    SET_KEY_URL=f"{AIS_DATABASE_HOST}/api/set_keys/"
    INTERPOLATE_URL=f"{AIS_DATABASE_HOST}/api/interpolate/"
    TOKEN_URL=f"{AIS_DATABASE_HOST}/api/token/"
    REFRESH_TOKEN_URL=f"{AIS_DATABASE_HOST}/api/token/refresh/"
    MMSI_URL=f"{AIS_DATABASE_HOST}/api/mmsi/"
    LATEST_URL=f"{AIS_DATABASE_HOST}/api/latest_dates/"
    POLYGON_URL=f"{AIS_DATABASE_HOST}/api/polygon/"

    def __init__(self, user, password) -> None:
        """
        Establish database connection
        """
        self.keys = ('mmsi', 'vessel_name', 'vessel_type', 'nav_status',
            'heading', 'dt_pos_utc', 'flag_country', 'destination',
            'latitude', 'longitude')

        self.user = user
        self.password = password

        self.session = requests.Session()
        self.refresh_token=None
        self.connection_verified=False
        self._set_token()

    def _get_bearer_token(self) -> dict:
        """
        Retrieves the bearer token required for API authentication.

        :return: Success flag and either token or error details.
        """
        if self.refresh_token:
            url=self.REFRESH_TOKEN_URL
            payload={"refresh": self.refresh_token}
        else:
            url=self.TOKEN_URL

            payload = {
                "username": self.user,
                "password": self.password,
            }

        try:
            response = requests.post(
                url,
                json=payload,
                timeout=10
            )
            if response.status_code == 401:
                if self.refresh_token is not None:
                    self.refresh_token = None
                    self._get_bearer_token()

            response.raise_for_status()
            response = response.json()
            token = response["access"]
            if "refresh" in response.keys():
                self.refresh_token = response["refresh"]
            return {"success": True, "token": token}

        except requests.exceptions.RequestException as e:
            try:
                error_details = response.json()
            except ValueError:
                print(e)
                error_details = {"message": response.text}

            return {
                "success": False,
                "error": "Token request failed",
                "details": error_details,
            }

    def _set_token(self):
        response = self._get_bearer_token()
        if response['success']:
            self.connection_verified=True
            token = response['token']
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        else:
            self.connection_verified=True
            raise Exception(response['error'],response['details'])

    def get_mmsi(self, mmsis : list, from_time:str, to_time:str):
        """
        Get current position of vessels with given MMSIs.

        :param mmsis: A list of MMSI numbers
        :param from_time: Retrieve AIS data points after this timestamp
        :param to_time: Retrieve AIS data points before this timestamp
        """
        payload = {
            'mmsi': mmsis,
            'from_time':from_time,
            'to_time':to_time
        }
        response = self.session.post(self.MMSI_URL, json=payload)
        if response.status_code == 401:
            self._set_token()
            response = self.session.post(self.MMSI_URL, json=payload)
        response.raise_for_status()
        return response.json()

    def get_sar_vessel_positions(self, from_time: str|None = None, to_time: str|None = None):
        """
        Get current position of all known SAR vesssels. If no dates are provied, AIS data
        points between now and 24h ago will be retrieved from the database.

        :param from_time: Retrieve AIS data points after this timestamp
        :param to_time: Retrieve AIS data points before this timestamp
        """
        payload = {
            'region': "ngo",
            'from_time':from_time if from_time else (datetime.now() - timedelta(hours=24)).isoformat(),
            'to_time': to_time if to_time else datetime.now().isoformat()
        }
        response = self.session.post(self.MMSI_URL, json=payload)         
        if response.status_code == 401:
            self._set_token()
            response = self.session.post(self.MMSI_URL, json=payload)
        response.raise_for_status()
        filtered_response = []
        existing_mmsis = set()
        for data_point in response.json():
            if data_point["mmsi"] not in existing_mmsis:
                filtered_response.append(data_point)
                existing_mmsis.add(data_point["mmsi"])
        return filtered_response

    def get_latest_dates(self, region=None):
        """
        Returns the date and time of the last update from UNGP.
        """
        payload = {"region": region} if region else {}
        response = self.session.post(self.LATEST_URL, json=payload)
        if response.status_code == 401:
            self._set_token()
            response = self.session.post(self.LATEST_URL, json=payload)
        response.raise_for_status()
        return response.json()

    def get_interpolated(self, time, polygon, space_buffer=12000, time_buffer=30):
        """
        This function retrieves AIS datapoints for a given timestamp and region. The location
        of a vessel is being interpolated between the last data point before the given timestamp
        and next known position after the given timestamp.

        :param time: target timestamp at which we want to retrieve the AIS data points
        :param polygon: region in which the AIS datapoints should be retrieved
        :param space_buffer: distance in meters beyond the polygon which should be included in the search
        :param time_buffer: time difference in minutes before and after the target time which should be
                            used to fetch AIS datapoints
        """
        payload={
            "polygon":polygon,
            "target_time":time,
            "space_buffer":space_buffer,
            "time_buffer":time_buffer
        }
        response = self.session.post(self.INTERPOLATE_URL, json=payload)
        if response.status_code == 401:
            self._set_token()
            response = self.session.post(self.INTERPOLATE_URL, json=payload)
        response.raise_for_status()
        return response.json()


    def set_keys(self, keys:list) -> dict:
        """
        Minimum keys that are always returned:
        [
            "mmsi",
            "vessel_name",
            "longitude",
            "latitude",
            "dt_pos_utc",
        ]
        """

        payload={
            "keys":keys
        }
        response = self.session.post(self.SET_KEY_URL, json=payload)
        if response.status_code == 401:
            self._set_token()
            response = self.session.post(self.SET_KEY_URL, json=payload)
        response.raise_for_status()
        return response.json()

    def close_connection(self):
        self.session.close()
