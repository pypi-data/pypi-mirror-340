from typing import List, Optional, Dict, Any

import httpx
from pydantic import BaseModel, Field, HttpUrl


class SkillParameter(BaseModel):
    """Represents a parameter definition for a skill."""

    type: Optional[str] = "string"  # Default to string type if not provided
    description: str
    name: str
    required: Optional[bool] = None
    nullable: Optional[bool] = None


class Skill(BaseModel):
    """Represents a skill in the Skill Registry."""

    id: Optional[str] = None  # Not in request, but present in response
    name: str
    description: str
    urlToExecute: HttpUrl
    token: Optional[str] = None
    componentId: Optional[str] = None
    tag: Optional[str] = None
    configurationId: Optional[str] = None
    properties: Optional[List[SkillParameter]] = None


class SkillExecutionRequest(BaseModel):
    """Request model for executing a skill."""

    parameters: Dict[str, Any] = Field(default_factory=dict)


class SkillExecutionResponse(BaseModel):
    """Response model for skill execution."""

    result: Dict[str, Any]
    execution_id: Optional[str] = None
    status: Optional[str] = None


class SkillExecutionError(Exception):
    """Exception raised when a skill execution fails."""

    def __init__(self, message: str, skill: str):
        self.message = message
        self.skill = skill


class SkillRegistryClient:
    """Client for interacting with the Skill Registry API."""

    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: int = 30):
        """
        Initialize the Skill Registry client.

        Args:
            base_url: Base URL of the Skill Registry API
            api_key: Optional API key for authentication
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self._client = httpx.Client(
            base_url=self.base_url, timeout=self.timeout, headers=self._get_headers()
        )

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.api_key:
            headers["X-API-TOKEN"] = self.api_key
        return headers

    def register_skill(self, skill: Skill) -> None:
        """
        Register a new skill in the registry.

        Args:
            skill: Skill object containing all required information
        """
        response = self._client.post("/skill-registration", json=skill.dict(exclude_none=True))
        response.raise_for_status()

    def list_skills(self) -> List[Skill]:
        """
        List all available skills.

        Returns:
            List of Skill objects
        """
        response = self._client.get("/skills")
        response.raise_for_status()
        return [Skill(**skill) for skill in response.json()["data"]]

    def update_skill(self, skill_id: str, skill: Skill) -> None:
        """
        Update an existing skill.

        Args:
            skill_id: ID of the skill to update
            skill: Updated skill information
        """
        response = self._client.put(f"/skills/{skill_id}", json=dict(skill))
        response.raise_for_status()

    def execute_skill(
            self, skill_id: str, parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a specific skill.

        Args:
            skill_id: ID of the skill to execute
            parameters: Optional properties for the skill execution

        Returns:
            Dictionary containing the execution result
        """
        response = self._client.post(f"/skills/{skill_id}/execute", json=parameters or {})
        if response.status_code >= 400:
            error_data = response.json()
            error_msg = f"Skill execution failed: {error_data.get('message', 'Unknown error')}"
            if skill := error_data.get("skill"):
                error_msg += f" (Skill: {error_data['skill']})"
            raise SkillExecutionError(error_msg, skill)

        return response.json()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client.close()
