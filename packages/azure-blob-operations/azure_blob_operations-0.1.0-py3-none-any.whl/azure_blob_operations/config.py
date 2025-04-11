from dataclasses import dataclass

@dataclass
class BlobConfig:
    """Configuration for blob operations."""
    max_retries: int = 5
    retry_delay: int = 5
    sas_expiry_hours: int = 1
    default_content_type: str = "application/octet-stream"

CONFIG = BlobConfig()