"""Assets module, all the logic to manage assets from PS API"""

import logging

from cerberus import Validator

from secrets_safe_library import exceptions, utils
from secrets_safe_library.authentication import Authentication
from secrets_safe_library.core import APIObject


class Asset(APIObject):

    def __init__(self, authentication: Authentication, logger: logging.Logger = None):
        super().__init__(authentication, logger)

        # Schema rules used for validations
        self._schema = {
            "description": {"type": "string", "maxlength": 256, "nullable": True},
        }
        self._validator = Validator(self._schema)

    def list_assets(
        self,
        workgroup_id: int = None,
        workgroup_name: str = None,
        limit: int = None,
        offset: int = None,
    ) -> list:
        """
        Returns a list of assets matching specified Workgroup ID or Name.
        parameters.

        API:
            - GET Workgroups/{workgroupID}/Assets
            - GET Workgroups/{workgroupName}/Assets

        Args:
            workgroup_id (int, optional): The Workgroup ID, if want to search by
                Workgroup ID.
            workgroup_name (str, optional): The Workgroup name, if want to search by
                Workgroup name.
            limit (int, optional): limit the results.
            offset (int, optional): skip the first (offset) number of assets.

        Returns:
            list: List of assets matching specified Workgroup ID or Name.
        """

        params = {
            "limit": limit,
            "offset": offset,
        }
        query_string = self.make_query_string(params)

        if workgroup_id:
            endpoint = f"/workgroups/{workgroup_id}/assets?{query_string}"
        elif workgroup_name:
            endpoint = f"/workgroups/{workgroup_name}/assets?{query_string}"
        else:
            raise exceptions.OptionsError(
                "Either workgroup_id or workgroup_name is required"
            )

        utils.print_log(
            self._logger, f"Calling list_assets endpoint: {endpoint}", logging.DEBUG
        )
        response = self._run_get_request(endpoint)

        return response.json()

    def get_asset_by_id(self, asset_id: str) -> dict:
        """
        Returns an asset by ID.

        API: GET Assets/{id}

        Args:
            asset_id (str): The asset ID (GUID).

        Returns:
            dict: Asset object.
        """

        endpoint = f"/assets/{asset_id}"

        utils.print_log(
            self._logger,
            f"Calling get_asset_by_id endpoint: {endpoint}",
            logging.DEBUG,
        )
        response = self._run_get_request(endpoint, include_api_version=False)

        return response.json()

    def get_asset_by_workgroup_name(self, workgroup_name: str, asset_name: str) -> dict:
        """
        Returns an asset by Workgroup name and asset name.

        API: GET Workgroups/{workgroupName}/Assets?name={name}

        Args:
            workgroup_name (str): Name of the Workgroup.
            asset_name (str): Name of the asset.

        Returns:
            dict: Asset object.
        """

        params = {"name": asset_name}
        query_string = self.make_query_string(params)

        endpoint = f"/workgroups/{workgroup_name}/assets?{query_string}"

        utils.print_log(
            self._logger,
            f"Calling get_asset_by_workgroup_name endpoint: {endpoint}",
            logging.DEBUG,
        )
        response = self._run_get_request(endpoint, include_api_version=False)

        return response.json()

    def search_assets(
        self,
        asset_name: str = None,
        dns_name: str = None,
        domain_name: str = None,
        ip_address: str = None,
        mac_address: str = None,
        asset_type: str = None,
        limit: int = 100000,
        offset: int = 0,
    ) -> list:
        """
        Returns a list of assets that match the given search criteria.

        At least one request body property should be provided; any property not
        provided is ignored. All search criteria is case insensitive and is an exact
        match (equality), except for IPAddress.

        API: POST Assets/Search

        Args:
            asset_name (str, optional): The Asset name, if you want to search by
                Asset name.
            dns_name (str, optional): The DNS name, if you want to search by DNS name.
            domain_name (str, optional): The Domain name, if you want to search by
                Domain name.
            ip_address (str, optional): The IP address, if you want to search by IP
                address.
            mac_address (str, optional): The MAC address, if you want to search by MAC
                address.
            asset_type (str, optional): The Asset type, if you want to search by Asset
                type.
            limit (int, optional): Limit the number of results returned.
            offset (int, optional): Skip the first (offset) number of assets in the
                results.

        Returns:
            list: List of assets matching specified parameters.
        """

        if not any(
            [asset_name, dns_name, domain_name, ip_address, mac_address, asset_type]
        ):
            raise exceptions.OptionsError(
                "At least one of the following fields must be provided: "
                "asset_name, dns_name, domain_name, ip_address, mac_address, asset_type"
            )

        params = {
            "limit": limit,
            "offset": offset,
        }
        query_string = self.make_query_string(params)

        endpoint = f"/assets/search?{query_string}"

        utils.print_log(
            self._logger, f"Calling list_assets endpoint: {endpoint}", logging.DEBUG
        )

        body = {
            "AssetName": asset_name,
            "DnsName": dns_name,
            "DomainName": domain_name,
            "IPAddress": ip_address,
            "MacAddress": mac_address,
            "AssetType": asset_type,
        }

        req_body = {key: value for key, value in body.items() if value is not None}
        response = self._run_post_request(endpoint, req_body, expected_status_code=200)

        return response.json()
