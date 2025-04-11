"""
Module for managing database credentials and connections.
"""
import os
from typing import Dict, Any, Optional
import logging
import requests

logger = logging.getLogger(__name__)

class CredentialsManager:
    """Manages database credentials and connection information."""
    
    DEFAULT_UUID = os.environ.get("SESSION_ID", "")
    API_URL_BASE = os.environ.get("API_URL_BASE", "")
    
    def __init__(self):
        """Initialize credentials manager."""
        self._credentials = {}
    
    def get_credentials_by_code(self, alias: str) -> Dict[str, Any]:
        """Get credentials by source code."""
        if not self.DEFAULT_UUID:
            raise Exception("SESSION_ID environment variable is not set")

        # Ensure API URL ends with /
        api_url = self.API_URL_BASE
        if not api_url.endswith("/"):
            api_url += "/"
        api_url += "detail"

        # Make POST request to detail endpoint
        try:
            # Ensure alias is not None and properly formatted
            if not alias:
                raise Exception("Source code cannot be None or empty")
                
            # Remove any leading/trailing whitespace and ensure proper format
            alias = alias.strip()
            
            # If alias is just a name (e.g., "PGIRD"), prepend the type
            if "/" not in alias:
                raise Exception("Source code must be in format 'type/name' (e.g., 'postgresql/PGIRD')")
            
            response = requests.post(
                api_url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.DEFAULT_UUID}"
                },
                json={"code": alias},
                verify=False  # Skip SSL verification
            )
            
            logger.info(f"API URL: {api_url}")
            logger.info(f"Request headers: {response.request.headers}")
            logger.info(f"Request body: {response.request.body}")
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response headers: {response.headers}")
            logger.info(f"Response text: {response.text}")
            
            if response.status_code != 200:
                raise Exception(f"API request failed with status {response.status_code}: {response.text}")
            
            try:
                response_data = response.json()
            except Exception as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.error(f"Response text: {response.text}")
                raise Exception("Invalid JSON response from API")
                
            logger.info(f"Response JSON: {response_data}")
            
            if not isinstance(response_data, dict):
                raise Exception("Invalid response format: expected dictionary")
                
            if "success" not in response_data or response_data["success"] != 1:
                raise Exception(f"API request was not successful: {response_data.get('message', 'Unknown error')}")
                
            if "data" not in response_data:
                raise Exception("Missing 'data' field in response")
                
            if not isinstance(response_data["data"], dict):
                raise Exception("Invalid 'data' field: expected dictionary")
                
            if "information" not in response_data["data"]:
                raise Exception("Missing 'information' field in data")
                
            if not isinstance(response_data["data"]["information"], dict):
                raise Exception("Invalid 'information' field: expected dictionary")
                
            info = response_data["data"]["information"]
            
            # Map API fields to expected fields
            return {
                "host": info["host"],
                "port": info["port"],
                "username": info["username"],
                "password": info["password"],
                "database": info.get("database_name", "postgres")
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP request failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Error getting credentials: {e}")
            raise

    def get_jdbc_credentials(self, source: str, dbname: str = "postgres") -> str:
        """Get JDBC credentials by source ID."""
        try:
            if not source:
                raise Exception("Source code cannot be None or empty")
                
            creds = self.get_credentials_by_code(source)
            if not creds:
                raise Exception(f"No credentials found for source {source}")
            
            # Extract required fields
            host = creds.get('host')
            port = creds.get('port')
            user = creds.get('username')
            password = creds.get('password')
            
            if not all([host, port, user, password]):
                raise Exception("Missing required credentials fields")
            
            # Determine database type from source code
            db_type = source.split('/')[0].lower()
            
            if db_type == "postgresql":
                # Format PostgreSQL JDBC URL with SSL disabled
                return f"jdbc:postgresql://{host}:{port}/{dbname}?user={user}&password={password}&ssl=false"
            elif db_type == "mysql":
                # Format MySQL JDBC URL with additional parameters
                return f"jdbc:mysql://{host}:{port}/{dbname}?user={user}&password={password}&useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC"
            else:
                raise Exception(f"Unsupported database type: {db_type}")
                
        except Exception as e:
            logger.error(f"Error getting JDBC credentials: {e}")
            raise
    
    def get_nessie_credentials(self, source_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get Nessie credentials by source ID."""
        if source_id is None:
            source_id = "nessie_source:default"
        if not source_id.startswith("nessie_source:"):
            source_id = f"nessie_source:{source_id}"
        return self._credentials.get(source_id)
    
    
    def validate_nessie_connection(self, source_id: Optional[str] = None) -> bool:
        """
        Validate Nessie connection using stored credentials.
        
        Args:
            source_id: Optional source ID. If None, validates default credentials
            
        Returns:
            bool: True if connection successful, False otherwise
        """
        creds = self.get_nessie_credentials(source_id)
        if not creds:
            return False
            
        try:
            # Basic validation of required fields
            required_fields = ['uri', 'ref', 'warehouse', 'io_impl']
            return all(field in creds for field in required_fields)
        except Exception:
            return False