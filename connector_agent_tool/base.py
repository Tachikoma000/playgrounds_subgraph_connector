"""PlaygroundsSubgraphConnectorToolSpec."""

from typing import Optional, Union
import requests
import logging
from llama_hub.tools.graphql.base import GraphQLToolSpec

class PlaygroundsSubgraphConnectorToolSpec(GraphQLToolSpec):
    """
    A tool specification that provides connectivity to subgraphs on The Graph's decentralized network via the Playgrounds API.
    This tool facilitates GraphQL queries to the specified subgraphs and supports pagination.
    
    Attributes:
        spec_functions (list of str): The list of functions that this tool provides.
        url (str): The endpoint URL to which GraphQL requests are sent.
        headers (dict): Any necessary headers for the GraphQL requests, such as authentication.
    """

    spec_functions = ["graphql_request"]

    def __init__(self, identifier: str, api_key: str, use_deployment_id: bool = False, log_level: int = logging.INFO, paginate: bool = True):
        """
        Initialize the PlaygroundsSubgraphConnector with necessary parameters.

        Args:
            identifier (str): Unique identifier for the subgraph or deployment.
            api_key (str): API key to authenticate with the Playgrounds API.
            use_deployment_id (bool, optional): Whether the provided identifier is a deployment ID. Defaults to False.
            log_level (int, optional): Desired log level for the connector. Defaults to logging.INFO.
            paginate (bool, optional): Whether to paginate the results if possible. Defaults to True.
        """
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self.paginate = paginate
        
        endpoint = "deployments" if use_deployment_id else "subgraphs"
        self.url = f"https://api.playgrounds.network/v1/proxy/{endpoint}/id/{identifier}"
        self.headers = {
            "Content-Type": "application/json",
            "Playgrounds-Api-Key": api_key
        }

    def graphql_request(self, query: str, variables: Optional[dict] = None, operation_name: Optional[str] = None) -> Union[dict, str]:
        """
        Execute a GraphQL query against the connected subgraph.

        Args:
            query (str): The GraphQL query string.
            variables (dict, optional): Variables to be used in the GraphQL query. Defaults to None.
            operation_name (str, optional): The name of the operation if the query string contains multiple operations. Defaults to None.

        Returns:
            dict: The response from the GraphQL server if the query is successful.
            str: An error message if the query fails.
        """
        
        all_data = []
        last_id = ""
        loop_counter = 0
        previous_data = None

        # Loop to handle pagination
        while True:
            loop_counter += 1
            if loop_counter > 10:  # safety mechanism to prevent infinite loops
                self.logger.warning("Exiting loop after 10 iterations.")
                break

            # Prepare the request payload
            payload = {"query": query.strip()}
            if variables:
                payload["variables"] = dict(variables)
                payload["variables"]["id_gt"] = last_id
            if operation_name:
                payload["operationName"] = operation_name

            self.logger.info(f"Sending GraphQL request to {self.url}")
            
            # Handle possible exceptions during the request
            try:
                response = requests.post(self.url, headers=self.headers, json=payload)
                response.raise_for_status()
                data = response.json()
                self.logger.debug(f"Received data: {data}")

                # If same data is received in consecutive queries, break out of the loop
                if previous_data == data:
                    self.logger.warning("Identical data received in consecutive queries. Exiting loop.")
                    break
                previous_data = data
                
                if 'errors' in data:
                    self.logger.error(f"GraphQL errors: {data['errors']}")
                    return data['errors']

                # If pagination is not needed or data isn't present, return the data
                if not self.paginate or not data.get("data"):
                    return data

                # If data is present and of type list, continue processing
                if 'data' in data and isinstance(data["data"], list) and data["data"]:
                    all_data.extend(data["data"])
                    last_id = data["data"][-1]["id"]
                    self.logger.debug(f"Last ID processed: {last_id}")
                    if len(data["data"]) < 1000:  # 1000 is a common page size in GraphQL
                        break

            except requests.ConnectionError:
                self.logger.error("Failed to connect to the server.")
                return "Connection Error"
            except requests.Timeout:
                self.logger.error("Request timed out.")
                return "Timeout Error"
            except requests.RequestException as e:
                self.logger.error(f"Error during request: {e}")
                return str(e)
            except ValueError as e:
                self.logger.error(f"JSON decoding error: {e}")
                return f"Decoding Error: {e}"

        return {"data": all_data}
