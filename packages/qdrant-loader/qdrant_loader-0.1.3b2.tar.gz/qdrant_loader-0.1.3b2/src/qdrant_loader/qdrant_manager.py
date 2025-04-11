from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.exceptions import UnexpectedResponse
import structlog
from typing import Optional, List
from urllib.parse import urlparse
from .config import Settings, get_settings, get_global_config

logger = structlog.get_logger()

class QdrantManager:
    def __init__(self, settings: Optional[Settings] = None):
        self.client = None
        self.settings = settings or get_settings()
        if not self.settings:
            raise ValueError("Settings must be provided either through environment or constructor")
        self.collection_name = self.settings.QDRANT_COLLECTION_NAME
        self.batch_size = get_global_config().embedding.batch_size
        self.connect()

    def _is_api_key_present(self) -> bool:
        """
        Check if a valid API key is present.
        Returns True if the API key is a non-empty string that is not 'None' or 'null'.
        """
        api_key = self.settings.QDRANT_API_KEY
        if not api_key:  # Catches None, empty string, etc.
            return False
        return api_key.lower() not in ['none', 'null']

    def connect(self) -> None:
        """Establish connection to qDrant server."""
        try:
            # Ensure HTTPS is used when API key is present, but only for non-local URLs
            url = self.settings.QDRANT_URL
            api_key = self.settings.QDRANT_API_KEY if self._is_api_key_present() else None

            if api_key:
                parsed_url = urlparse(url)
                # Only force HTTPS for non-local URLs
                if parsed_url.scheme != 'https' and not any(
                    host in parsed_url.netloc 
                    for host in ['localhost', '127.0.0.1']
                ):
                    url = url.replace('http://', 'https://', 1)
                    logger.warning("Forcing HTTPS connection due to API key usage")

            self.client = QdrantClient(
                url=url,
                api_key=api_key,
                timeout=60  # 60 seconds timeout
            )
            # Note: The version check warning is expected when connecting to Qdrant Cloud instances.
            # This occurs because the version check endpoint might not be accessible due to security restrictions.
            # The warning can be safely ignored as it doesn't affect functionality.
            logger.info("Successfully connected to qDrant")
        except Exception as e:
            logger.error("Failed to connect to qDrant", error=str(e))
            raise

    def create_collection(self) -> None:
        """Create a new collection if it doesn't exist."""
        try:
            # Check if collection already exists
            collections = self.client.get_collections()
            if any(c.name == self.collection_name for c in collections.collections):
                logger.info(f"Collection {self.collection_name} already exists")
                return

            # Create collection with basic configuration
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=1536,  # OpenAI embedding size
                    distance=models.Distance.COSINE
                )
            )
            logger.info(f"Collection {self.collection_name} created successfully")
        except Exception as e:
            logger.error("Failed to create collection", error=str(e))
            raise

    def upsert_points(self, points: List[models.PointStruct]) -> None:
        """Upsert points to the collection in batches."""
        try:
            total_points = len(points)
            for i in range(0, total_points, self.batch_size):
                batch = points[i:i + self.batch_size]
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=batch,
                    wait=True
                )
                logger.info("Upserted batch of points", 
                           batch_size=len(batch),
                           progress=f"{i + len(batch)}/{total_points}")
            logger.info("Successfully upserted all points", count=total_points)
        except Exception as e:
            logger.error("Failed to upsert points", error=str(e))
            raise

    def search(self, query_vector: List[float], limit: int = 5) -> List[models.ScoredPoint]:
        """Search for similar vectors in the collection."""
        try:
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit
            )
            return search_result
        except Exception as e:
            logger.error("Failed to search collection", error=str(e))
            raise

    def delete_collection(self) -> None:
        """Delete the collection."""
        try:
            self.client.delete_collection(collection_name=self.collection_name)
            logger.info("Deleted collection", collection=self.collection_name)
        except Exception as e:
            logger.error("Failed to delete collection", error=str(e))
            raise 