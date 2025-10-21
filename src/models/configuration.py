from dataclasses import dataclass
from typing import Dict, List, Literal

TransportType = Literal["stdio", "streamable-http"]
LogLevelType = Literal["DEBUG", "INFO", "WARNING", "ERROR"]
AuthModeType = Literal["none", "static-token"]

@dataclass(frozen=True)
class Configuration:
    """Type-safe configuration container."""
    host: str
    port: int
    transport: TransportType
    log_level: LogLevelType
    metabase_url: str
    metabase_api_key: str
    auth_mode: AuthModeType
    auth_tokens: Dict[str, Dict[str, object]]
    allow_unauthenticated_http: bool
    required_scopes: List[str]
    log_sql_queries: bool
    
    def __post_init__(self) -> None:
        """Validate configuration values after initialization."""
        if not isinstance(self.port, int) or self.port <= 0:
            raise ValueError(f"Port must be a positive integer, got {self.port}")
        
        if not self.metabase_url:
            raise ValueError("Metabase URL is required")
        
        if not self.metabase_api_key:
            raise ValueError("Metabase API key is required")
        
        if self.transport != "stdio" and self.auth_mode == "none" and not self.allow_unauthenticated_http:
            raise ValueError(
                "HTTP transport requires authentication. "
                "Provide auth tokens or explicitly allow unauthenticated access."
            )
        
        # Note: We allow static-token mode without tokens for now since middleware injection
        # is not yet implemented. Users should use a reverse proxy for authentication.
        # if self.auth_mode == "static-token" and not self.auth_tokens:
        #     raise ValueError("Static-token authentication requires at least one token")
