from typing import Literal, Optional, List, Dict, Any, Union, Iterator

from pydantic import model_validator, Field, field_validator

from pygeai.core import CustomBaseModel


class FilterSettings(CustomBaseModel):
    """
    Represents filter settings for querying or filtering data.

    :param id: str - The ID to filter by (e.g., an agent's ID), defaults to an empty string.
    :param name: str - The name to filter by (e.g., reasoning strategy name), defaults to an empty string.
    :param status: str - Status filter, defaults to None.
    :param start: int - Starting index for pagination, defaults to None.
    :param count: int - Number of items to return, defaults to None.
    :param access_scope: str - Access scope filter, defaults to "public".
    :param allow_drafts: bool - Whether to include draft items, defaults to True.
    :param allow_external: bool - Whether to include external items, defaults to False.
    :param revision: str - Revision of the agent, defaults to 0.
    :param version: str - Version of the agent, defaults to 0
    :param scope: Optional[str] - Filter by scope (e.g., "builtin", "external", "api").
    """
    id: Optional[str] = Field(default=None, description="The ID to filter by (e.g., an agent's ID)")
    name: Optional[str] = Field(default=None, description="The name to filter by (e.g., a reasoning strategy name)")
    status: Optional[str] = Field(default=None, description="Status filter")
    start: Optional[int] = Field(default=None, description="Starting index for pagination")
    count: Optional[int] = Field(default=None, description="Number of items to return")
    access_scope: Optional[str] = Field(default="public", alias="accessScope", description="Access scope filter")
    allow_drafts: Optional[bool] = Field(default=True, alias="allowDrafts", description="Whether to include draft items")
    allow_external: Optional[bool] = Field(default=False, alias="allowExternal", description="Whether to include external items")
    revision: Optional[str] = Field(default=None, description="Revision of the agent")
    version: Optional[int] = Field(default=None, description="Version of the agent")
    scope: Optional[str] = Field(None, description="Filter by scope (e.g., 'builtin', 'external', 'api')")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    def __str__(self):
        return str(self.to_dict())


class Sampling(CustomBaseModel):
    """
    Represents sampling configuration for an LLM.

    :param temperature: float - Temperature value for sampling, controlling randomness.
    :param top_k: int - Top-K sampling parameter, limiting to the top K probable tokens.
    :param top_p: float - Top-P (nucleus) sampling parameter, limiting to the smallest set of tokens whose cumulative probability exceeds P.
    """
    temperature: float = Field(..., alias="temperature")
    top_k: int = Field(..., alias="topK")
    top_p: float = Field(..., alias="topP")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    def __str__(self):
        return str(self.to_dict())


class LlmConfig(CustomBaseModel):
    """
    Represents the configuration parameters for an LLM.

    :param max_tokens: int - Maximum number of tokens the LLM can generate.
    :param timeout: int - Timeout value in seconds (0 means no timeout).
    :param sampling: Sampling - Sampling configuration for the LLM.
    """
    max_tokens: int = Field(..., alias="maxTokens")
    timeout: int = Field(..., alias="timeout")
    sampling: Sampling = Field(..., alias="sampling")

    def to_dict(self):
        return {
            "maxTokens": self.max_tokens,
            "timeout": self.timeout,
            "sampling": self.sampling.to_dict()
        }

    def __str__(self):
        return str(self.to_dict())


class Model(CustomBaseModel):
    """
    Represents a language model configuration used by an agent.

    :param name: str - The unique name identifying the model.
    :param llm_config: Optional[LlmConfig] - Overrides default agent LLM settings.
    :param prompt: Optional[dict] - A tailored prompt specific to this model.
    """
    name: str = Field(..., alias="name")
    llm_config: Optional[LlmConfig] = Field(None, alias="llmConfig")
    prompt: Optional[Dict[str, Any]] = Field(None, alias="prompt")

    def to_dict(self):
        result = {"name": self.name}
        if self.llm_config is not None:
            result["llmConfig"] = self.llm_config.to_dict()
        if self.prompt is not None:
            result["prompt"] = self.prompt
        return result

    def __str__(self):
        return str(self.to_dict())


class PromptExample(CustomBaseModel):
    """
    Represents an example for the prompt configuration.

    :param input_data: str - Example input data provided to the agent.
    :param output: str - Example output in JSON string format.
    """
    input_data: str = Field(..., alias="inputData")
    output: str = Field(..., alias="output")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    def __str__(self):
        return str(self.to_dict())


class PromptOutput(CustomBaseModel):
    """
    Represents an output definition for the prompt configuration.

    :param key: str - Key identifying the output.
    :param description: str - Description of the output's purpose and format.
    """
    key: str = Field(..., alias="key")
    description: str = Field(..., alias="description")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    def __str__(self):
        return str(self.to_dict())


class Prompt(CustomBaseModel):
    """
    Represents the prompt configuration for an agent.

    :param instructions: str - Instructions for the agent's behavior.
    :param inputs: List[str] - List of input parameters the agent expects.
    :param outputs: List[PromptOutput] - List of output definitions the agent produces.
    :param examples: List[PromptExample] - List of example input-output pairs.
    """
    instructions: str = Field(..., alias="instructions")
    inputs: List[str] = Field(..., alias="inputs")
    outputs: List[PromptOutput] = Field(..., alias="outputs")
    examples: Optional[List[PromptExample]] = Field(None, alias="examples")

    def to_dict(self):
        result = {
            "instructions": self.instructions,
            "inputs": self.inputs,
            "outputs": [output.to_dict() for output in self.outputs] if self.outputs else None,
            "examples": [example.to_dict() for example in self.examples] if self.examples else None
        }
        return {k: v for k, v in result.items() if v is not None}

    def __str__(self):
        return str(self.to_dict())


class ModelList(CustomBaseModel):
    models: List[Model] = Field(..., alias="models")

    def to_dict(self):
        return [model.to_dict() for model in self.models]

    def __getitem__(self, index: int) -> Model:
        if self.models is None:
            raise IndexError("ModelList is empty")
        return self.models[index]

    def __len__(self) -> int:
        return len(self.models) if self.models else 0

    def __iter__(self):
        """Make ModelList iterable over its models."""
        if self.models is None:
            return iter([])
        return iter(self.models)


class AgentData(CustomBaseModel):
    """
    Represents the detailed configuration data for an agent.

    :param prompt: dict - Prompt instructions, inputs, outputs, and examples for the agent.
    :param llm_config: dict - Configuration parameters for the LLM (e.g., max tokens, timeout, temperature).
    :param models: ModelList - List of models available for the agent.
    """
    prompt: Prompt = Field(..., alias="prompt")
    llm_config: LlmConfig = Field(..., alias="llmConfig")
    models: Union[ModelList, List[Model]] = Field(..., alias="models")

    @field_validator("models", mode="before")
    @classmethod
    def normalize_models(cls, value):
        """
        Normalizes the models input to a ModelList instance.

        :param value: Union[ModelList, List[Model]] - The input value for models.
        :return: ModelList - A ModelList instance containing the models.
        """
        if isinstance(value, ModelList):
            return value
        elif isinstance(value, list):
            return ModelList(models=value)
        raise ValueError("models must be a ModelList or a list of Model instances")

    def to_dict(self):
        """
        Serializes the AgentData instance to a dictionary, ensuring each Model in models calls its to_dict method.

        :return: dict - A dictionary representation of the agent data with aliases.
        """
        return {
            "prompt": self.prompt.to_dict(),
            "llmConfig": self.llm_config.to_dict(),
            "models": self.models.to_dict()
        }

    def __str__(self):
        return str(self.to_dict())


class Agent(CustomBaseModel):
    """
    Represents an agent configuration returned by the API.

    :param id: str - Unique identifier for the agent.
    :param status: Literal["active", "inactive"] - Current status of the agent.
    :param name: str - Name of the agent.
    :param access_scope: Literal["public", "private"] - Access scope of the agent.
    :param public_name: Optional[str] - Public identifier for the agent, required if access_scope is "public".
    :param avatar_image: Optional[str] - URL to the agent's avatar image.
    :param description: str - Description of the agent's purpose.
    :param job_description: Optional[str] - Detailed job description of the agent.
    :param is_draft: bool - Indicates if the agent is in draft mode.
    :param is_readonly: bool - Indicates if the agent is read-only.
    :param revision: int - Revision number of the agent.
    :param version: Optional[int] - Version number of the agent, if applicable.
    :param agent_data: AgentData - Detailed configuration data for the agent.
    """
    id: str = Field(None, alias="id")
    status: Optional[Literal["active", "inactive", "pending"]] = Field("active", alias="status")
    name: str = Field(..., alias="name")
    access_scope: Literal["public", "private"] = Field("private", alias="accessScope")
    public_name: Optional[str] = Field(None, alias="publicName")
    avatar_image: Optional[str] = Field(None, alias="avatarImage")
    description: Optional[str] = Field(None, alias="description")
    job_description: Optional[str] = Field(None, alias="jobDescription")
    is_draft: Optional[bool] = Field(True, alias="isDraft")
    is_readonly: Optional[bool] = Field(False, alias="isReadonly")
    revision: Optional[int] = Field(None, alias="revision")
    version: Optional[int] = Field(None, alias="version")
    agent_data: Optional[AgentData] = Field(None, alias="agentData")

    @model_validator(mode="after")
    def check_public_name(self):
        """
        Validates that public_name is provided if access_scope is set to "public".

        :raises ValueError: If access_scope is "public" but public_name is missing.
        """
        if self.access_scope == "public" and not self.public_name:
            raise ValueError("public_name is required if access_scope is public")
        return self

    def to_dict(self):
        result = {
            "id": self.id,
            "status": self.status,
            "name": self.name,
            "accessScope": self.access_scope,
            "publicName": self.public_name,
            "avatarImage": self.avatar_image,
            "description": self.description,
            "jobDescription": self.job_description,
            "isDraft": self.is_draft,
            "isReadonly": self.is_readonly,
            "revision": self.revision,
            "version": self.version,
            "agentData": self.agent_data.to_dict() if self.agent_data else None
        }
        return {k: v for k, v in result.items() if v is not None}

    def __str__(self):
        return str(self.to_dict())


class AgentList(CustomBaseModel):
    """
    Represents a list of agents returned by the API.

    :param agents: List[Agent] - List of agent configurations.
    """
    agents: List[Agent] = Field(..., alias="agents")

    def to_dict(self):
        return [agent.to_dict() for agent in self.agents]

    def __getitem__(self, index: int) -> Agent:
        if self.agents is None:
            raise IndexError("AgentList is empty")
        return self.agents[index]

    def __len__(self) -> int:
        return len(self.agents) if self.agents else 0

    def __iter__(self):
        """Make AgentList iterable over its agents."""
        if self.agents is None:
            return iter([])
        return iter(self.agents)


class SharingLink(CustomBaseModel):
    """
    Represents a sharing link for an agent.

    :param agent_id: str - Unique identifier of the agent.
    :param api_token: str - API token associated with the sharing link.
    :param shared_link: str - The full URL of the sharing link.
    """
    agent_id: str = Field(..., alias="agentId", description="Unique identifier of the agent")
    api_token: str = Field(..., alias="apiToken", description="API token associated with the sharing link")
    shared_link: str = Field(..., alias="sharedLink", description="The full URL of the sharing link")

    def to_dict(self):
        """
        Serializes the SharingLink instance to a dictionary.

        :return: dict - A dictionary representation of the sharing link with aliases.
        """
        return self.model_dump(by_alias=True, exclude_none=True)

    def __str__(self):
        return str(self.to_dict())


class ToolParameter(CustomBaseModel):
    """
    Represents a parameter for a tool.

    :param key: str - The identifier of the parameter.
    :param data_type: str - The data type of the parameter (e.g., "String").
    :param description: str - Description of the parameter's purpose.
    :param is_required: bool - Whether the parameter is required.
    :param type: Optional[str] - Type of parameter (e.g., "config"), defaults to None.
    :param from_secret: Optional[bool] - Whether the value comes from a secret manager, defaults to None.
    :param value: Optional[str] - The static value of the parameter, defaults to None.
    """
    key: str = Field(..., alias="key", description="The identifier of the parameter")
    data_type: str = Field(..., alias="dataType", description="The data type of the parameter (e.g., 'String')")
    description: str = Field(..., alias="description", description="Description of the parameter's purpose")
    is_required: bool = Field(..., alias="isRequired", description="Whether the parameter is required")
    type: Optional[str] = Field(None, alias="type", description="Type of parameter (e.g., 'config')")
    from_secret: Optional[bool] = Field(None, alias="fromSecret", description="Whether the value comes from a secret manager")
    value: Optional[str] = Field(None, alias="value", description="The static value of the parameter")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    def __str__(self):
        return str(self.to_dict())


class ToolMessage(CustomBaseModel):
    """
    Represents a message (e.g., warning or error) in the tool response.

    :param description: str - Description of the message.
    :param type: str - Type of the message (e.g., "warning", "error").
    """
    description: str = Field(..., alias="description", description="Description of the message")
    type: str = Field(..., alias="type", description="Type of the message (e.g., 'warning', 'error')")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    def __str__(self):
        return str(self.to_dict())


class Tool(CustomBaseModel):
    """
    Represents a tool configuration, used for both input and output.

    :param name: str - The name of the tool.
    :param description: str - Description of the tool's purpose.
    :param scope: str - The scope of the tool (e.g., "builtin", "external", "api").
    :param parameters: List[ToolParameter] - List of parameters required by the tool.
    :param access_scope: Optional[str] - The access scope of the tool ("public" or "private"), defaults to None.
    :param public_name: Optional[str] - Public name of the tool, required if access_scope is "public", defaults to None.
    :param icon: Optional[str] - URL for the tool's icon or avatar, defaults to None.
    :param open_api: Optional[str] - URL where the OpenAPI specification can be loaded, defaults to None.
    :param open_api_json: Optional[dict] - OpenAPI specification as a dictionary, defaults to None.
    :param report_events: Optional[str] - Event reporting mode ("None", "All", "Start", "Finish", "Progress"), defaults to None.
    :param id: Optional[str] - Unique identifier of the tool, defaults to None.
    :param is_draft: Optional[bool] - Whether the tool is in draft mode, defaults to None.
    :param messages: Optional[List[ToolMessage]] - List of messages (e.g., warnings or errors), defaults to None.
    :param revision: Optional[int] - Revision number of the tool, defaults to None.
    :param status: Optional[str] - Current status of the tool (e.g., "active"), defaults to None.
    """
    name: str = Field(..., alias="name", description="The name of the tool")
    description: str = Field(..., alias="description", description="Description of the tool's purpose")
    scope: str = Field("builtin", alias="scope", description="The scope of the tool (e.g., 'builtin', 'external', 'api')")
    parameters: Optional[List[ToolParameter]] = Field(None, alias="parameters", description="List of parameters required by the tool")
    access_scope: Optional[str] = Field(None, alias="accessScope", description="The access scope of the tool ('public' or 'private')")
    public_name: Optional[str] = Field(None, alias="publicName", description="Public name of the tool, required if access_scope is 'public'")
    icon: Optional[str] = Field(None, alias="icon", description="URL for the tool's icon or avatar")
    open_api: Optional[str] = Field(None, alias="openApi", description="URL where the OpenAPI specification can be loaded")
    open_api_json: Optional[dict] = Field(None, alias="openApiJson", description="OpenAPI specification as a dictionary")
    report_events: Optional[Literal['None', 'All', 'Start', 'Finish', 'Progress']] = Field("None", alias="reportEvents", description="Event reporting mode ('None', 'All', 'Start', 'Finish', 'Progress')")
    id: Optional[str] = Field(None, alias="id", description="Unique identifier of the tool")
    is_draft: Optional[bool] = Field(None, alias="isDraft", description="Whether the tool is in draft mode")
    messages: Optional[List[ToolMessage]] = Field(None, alias="messages", description="List of messages (e.g., warnings or errors)")
    revision: Optional[int] = Field(None, alias="revision", description="Revision number of the tool")
    status: Optional[str] = Field(None, alias="status", description="Current status of the tool (e.g., 'active')")

    @model_validator(mode="after")
    def check_public_name(self):
        if self.access_scope == "public" and not self.public_name:
            raise ValueError("public_name is required if access_scope is 'public'")
        return self

    def to_dict(self):
        result = {
            "name": self.name,
            "description": self.description,
            "scope": self.scope,
            "parameters": [param.to_dict() for param in self.parameters] if self.parameters else None,
            "accessScope": self.access_scope,
            "publicName": self.public_name,
            "icon": self.icon,
            "openApi": self.open_api,
            "openApiJson": self.open_api_json,
            "reportEvents": self.report_events,
            "id": self.id,
            "isDraft": self.is_draft,
            "messages": [msg.to_dict() for msg in self.messages] if self.messages else None,
            "revision": self.revision,
            "status": self.status
        }
        return {k: v for k, v in result.items() if v is not None}

    def __str__(self):
        return str(self.to_dict())


class ToolList(CustomBaseModel):
    """
    Represents a list of Tool objects retrieved from an API response.

    :param tools: List[Tool] - The list of tools.
    """
    tools: List[Tool] = Field(..., alias="tools", description="The list of tools")

    def to_dict(self):
        return {"tools": [tool.to_dict() for tool in self.tools]}

    def __str__(self):
        return str(self.to_dict())

    def __getitem__(self, index: int) -> Tool:
        if self.tools is None:
            raise IndexError("ToolList is empty")
        return self.tools[index]

    def __len__(self) -> int:
        return len(self.tools) if self.tools else 0

    def __iter__(self):
        """Make ToolList iterable over its tools."""
        if self.tools is None:
            return iter([])
        return iter(self.tools)


class LocalizedDescription(CustomBaseModel):
    """
    Represents a localized description for a reasoning strategy.

    :param language: str - The language of the description (e.g., "english", "spanish").
    :param description: str - The description text in the specified language.
    """
    language: str = Field(..., description="The language of the description")
    description: str = Field(..., description="The description text in the specified language")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)


class ReasoningStrategy(CustomBaseModel):
    """
    Represents a reasoning strategy configuration.

    :param name: str - The name of the reasoning strategy.
    :param system_prompt: str - The system prompt for the reasoning strategy.
    :param access_scope: str - The access scope of the strategy (e.g., "private", "public").
    :param type: str - The type of the reasoning strategy (e.g., "addendum").
    :param localized_descriptions: List[LocalizedDescription] - List of localized descriptions.
    :param id: Optional[str] - Unique identifier of the strategy, set by the API on creation.
    """
    name: str = Field(..., description="The name of the reasoning strategy")
    system_prompt: Optional[str] = Field(None, alias="systemPrompt", description="The system prompt for the reasoning strategy")
    access_scope: str = Field(..., alias="accessScope", description="The access scope of the strategy (e.g., 'private', 'public')")
    type: str = Field(..., description="The type of the reasoning strategy (e.g., 'addendum')")
    localized_descriptions: Optional[List[LocalizedDescription]] = Field(None, alias="localizedDescriptions", description="List of localized descriptions")
    id: Optional[str] = Field(None, description="Unique identifier of the strategy, set by the API on creation")

    def to_dict(self):
        result = {
            "name": self.name,
            "systemPrompt": self.system_prompt,
            "accessScope": self.access_scope,
            "type": self.type,
            "localizedDescriptions": [desc.to_dict() for desc in self.localized_descriptions],
            "id": self.id
        }
        return {k: v for k, v in result.items() if v is not None}


class ReasoningStrategyList(CustomBaseModel):
    strategies: List[ReasoningStrategy] = Field(..., alias="strategies", description="The list of reasoning strategies")

    def to_dict(self):
        return [strategy.to_dict() for strategy in self.strategies]

    def __str__(self):
        return str(self.to_dict())

    def __getitem__(self, index: int) -> ReasoningStrategy:
        if self.strategies is None:
            raise IndexError("ReasoningStrategyList is empty")
        return self.strategies[index]

    def __len__(self) -> int:
        return len(self.strategies) if self.strategies else 0

    def __iter__(self):
        """Make ReasoningStrategyList iterable over its strategies."""
        if self.strategies is None:
            return iter([])
        return iter(self.strategies)


class KnowledgeBase(CustomBaseModel):
    name: str = Field(..., description="Name of the knowledge base")
    artifact_type_name: List[str] = Field(..., alias="artifactTypeName", description="List of artifact type names")
    id: Optional[str] = Field(None, description="Unique identifier of the knowledge base, set by API")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)


class AgenticActivity(CustomBaseModel):
    key: str = Field(..., description="Unique key for the activity")
    name: str = Field(..., description="Name of the activity")
    task_name: str = Field(..., alias="taskName", description="Name of the task")
    agent_name: str = Field(..., alias="agentName", description="Name of the agent")
    agent_revision_id: int = Field(..., alias="agentRevisionId", description="Revision ID of the agent")
    agent_id: Optional[str] = Field(None, alias="agentId", description="Unique identifier of the agent, set by API")
    task_id: Optional[str] = Field(None, alias="taskId", description="Unique identifier of the task, set by API")
    task_revision_id: Optional[int] = Field(None, alias="taskRevisionId", description="Revision ID of the task, set by API")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)


class ArtifactSignal(CustomBaseModel):
    key: str = Field(..., description="Unique key for the artifact signal")
    name: str = Field(..., description="Name of the artifact signal")
    handling_type: str = Field(..., alias="handlingType", description="Handling type (e.g., 'C')")
    artifact_type_name: List[str] = Field(..., alias="artifactTypeName", description="List of artifact type names")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)


class UserSignal(CustomBaseModel):
    key: str = Field(..., description="Unique key for the user signal")
    name: str = Field(..., description="Name of the user signal")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)


class Event(CustomBaseModel):
    key: str = Field(..., description="Unique key for the event")
    name: str = Field(..., description="Name of the event")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)


class SequenceFlow(CustomBaseModel):
    key: str = Field(..., description="Unique key for the sequence flow")
    source_key: str = Field(..., alias="sourceKey", description="Key of the source event/activity/signal")
    target_key: str = Field(..., alias="targetKey", description="Key of the target event/activity/signal")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)


class Variable(CustomBaseModel):
    key: str = Field(..., description="Key of the variable")
    value: str = Field(..., description="Value of the variable")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)


class VariableList(CustomBaseModel):
    variables: Optional[List[Variable]] = Field(None, description="List of variables")

    def to_dict(self):
        return [var.to_dict() for var in self.variables] if self.variables else None

    def __getitem__(self, index: int) -> Variable:
        if self.variables is None:
            raise IndexError("VariableList is empty")
        return self.variables[index]

    def __len__(self) -> int:
        return len(self.variables) if self.variables else 0

    def __iter__(self) -> Iterator[Variable]:
        """Make VariableList iterable over its variables."""
        if self.variables is None:
            return iter([])
        return iter(self.variables)


class AgenticProcess(CustomBaseModel):
    key: Optional[str] = Field(None, description="Unique key for the process")
    name: str = Field(..., description="Name of the process")
    description: Optional[str] = Field(None, description="Description of the process")
    kb: Optional[KnowledgeBase] = Field(None, description="Knowledge base configuration")
    agentic_activities: Optional[List[AgenticActivity]] = Field(None, alias="agenticActivities", description="List of agentic activities")
    artifact_signals: Optional[List[ArtifactSignal]] = Field(None, alias="artifactSignals", description="List of artifact signals")
    user_signals: Optional[List[UserSignal]] = Field(None, alias="userSignals", description="List of user signals")
    start_event: Optional[Event] = Field(None, alias="startEvent", description="Start event of the process")
    end_event: Optional[Event] = Field(None, alias="endEvent", description="End event of the process")
    sequence_flows: Optional[List[SequenceFlow]] = Field(None, alias="sequenceFlows", description="List of sequence flows")
    variables: Optional[VariableList] = Field(None, alias="variables", description="List of variables")
    id: Optional[str] = Field(None, description="Unique identifier of the process, set by API")
    status: Optional[str] = Field(None, alias="status", description="Status of the process (e.g., 'active')")
    version_id: Optional[int] = Field(None, alias="versionId", description="Version ID of the process")
    is_draft: Optional[bool] = Field(None, alias="isDraft", description="Whether the process is a draft")
    revision: Optional[int] = Field(None, description="Revision number of the process")

    @field_validator("variables", mode="before")
    @classmethod
    def normalize_variables(cls, value):
        """
        Normalizes the variables input to a VariableList instance.

        :param value: Union[VariableList, List[Variable]] - The input value for variables.
        :return: VariableList - A VariableList instance containing the models.
        """
        if isinstance(value, VariableList):
            return value
        elif isinstance(value, (list, tuple)):
            return VariableList(variables=value)
        elif value is None:
            return VariableList(variables=[])

        raise ValueError("variables must be a VariableList or a list of Variable instances")

    def to_dict(self):
        """
        Serializes the AgenticProcess instance to a dictionary, explicitly mapping fields to their aliases
        and invoking to_dict for nested objects in lists.

        :return: dict - A dictionary representation of the process with aliases, excluding None values.
        """
        result = {
            "key": self.key,
            "name": self.name,
            "description": self.description,
            "kb": self.kb.to_dict() if self.kb else None,
            "agenticActivities": [activity.to_dict() for activity in self.agentic_activities] if self.agentic_activities else None,
            "artifactSignals": [signal.to_dict() for signal in self.artifact_signals] if self.artifact_signals else None,
            "userSignals": [signal.to_dict() for signal in self.user_signals] if self.user_signals else None,
            "startEvent": self.start_event.to_dict() if self.start_event else None,
            "endEvent": self.end_event.to_dict() if self.end_event else None,
            "sequenceFlows": [flow.to_dict() for flow in self.sequence_flows] if self.sequence_flows else None,
            "variables": self.variables.to_dict() if self.variables else None,
            "id": self.id,
            "status": self.status,
            "versionId": self.version_id,
            "isDraft": self.is_draft,
            "revision": self.revision
        }
        return {k: v for k, v in result.items() if v is not None}


class Task(CustomBaseModel):
    """
    Represents a task configuration used for both input and output.

    :param name: str - Required name of the task, must be unique within the project and exclude ':' or '/'.
    :param description: Optional[str] - Description of what the task does, for user understanding (not used by agents).
    :param title_template: Optional[str] - Template for naming task instances (e.g., 'specs for {{issue}}').
    :param id: Optional[str] - Unique identifier of the task, set by API or provided in insert mode for custom ID.
    :param prompt_data: Optional[dict] - Prompt configuration (same as AgentData prompt), combined with agent prompt during execution.
    :param artifact_types: Optional[List[dict]] - List of artifact types with 'name', 'description', 'isRequired', 'usageType', and 'artifactVariableKey'.
    :param is_draft: Optional[bool] - Whether the task is in draft mode.
    :param revision: Optional[int] - Revision number of the task.
    :param status: Optional[str] - Current status of the task (e.g., 'active').
    """
    name: str = Field(..., description="Name of the task")
    description: Optional[str] = Field(None, description="Description of the task")
    title_template: Optional[str] = Field(None, alias="titleTemplate", description="Title template for the task")
    id: Optional[str] = Field(None, description="Unique identifier of the task, set by API")
    prompt_data: Optional[Dict[str, Any]] = Field(None, alias="promptData", description="Prompt configuration for the task")
    artifact_types: Optional[List[Dict[str, Any]]] = Field(None, alias="artifactTypes", description="List of artifact types for the task")
    is_draft: Optional[bool] = Field(None, alias="isDraft", description="Whether the task is a draft")
    revision: Optional[int] = Field(None, description="Revision number of the task")
    status: Optional[str] = Field(None, description="Status of the task (e.g., 'active')")

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        """
        Ensures the task name does not contain forbidden characters ':' or '/'.

        :param value: str - The name to validate.
        :return: str - The validated name.
        :raises ValueError: If the name contains ':' or '/'.
        """
        if ":" in value or "/" in value:
            raise ValueError("Task name cannot contain ':' or '/'")
        return value

    def to_dict(self):
        """
        Serializes the Task instance to a dictionary, using aliases and excluding None values.

        :return: dict - A dictionary representation of the task configuration.
        """
        return self.model_dump(by_alias=True, exclude_none=True)

    def __str__(self):
        return str(self.to_dict())


class AgenticProcessList(CustomBaseModel):
    processes: List[AgenticProcess] = Field(..., alias="processes", description="List of agentic processes")

    def to_dict(self):
        return {"processes": [process.to_dict() for process in self.processes]}

    def __getitem__(self, index: int) -> AgenticProcess:
        if self.processes is None:
            raise IndexError("AgenticProcessList is empty")
        return self.processes[index]

    def __len__(self) -> int:
        return len(self.processes) if self.processes else 0

    def __iter__(self):
        """Make AgenticProcessList iterable over its processes."""
        if self.processes is None:
            return iter([])
        return iter(self.processes)


class TaskList(CustomBaseModel):
    tasks: List[Task] = Field(..., alias="tasks", description="List of tasks")

    def to_dict(self):
        return [task.to_dict() for task in self.tasks]

    def __getitem__(self, index: int) -> Task:
        if self.tasks is None:
            raise IndexError("TaskList is empty")
        return self.tasks[index]

    def __len__(self) -> int:
        return len(self.tasks) if self.tasks else 0

    def __iter__(self):
        """Make TaskList iterable over its tasks."""
        if self.tasks is None:
            return iter([])
        return iter(self.tasks)


class ProcessInstance(CustomBaseModel):
    id: Optional[str] = Field(None, alias="id", description="Unique identifier of the process instance, set by API")
    process: AgenticProcess = Field(..., alias="process", description="The process configuration")
    created_at: Optional[str] = Field(None, alias="createdAt", description="Timestamp when the instance was created")
    subject: str = Field(..., description="Subject of the instance")
    variables: Optional[Union[List[Variable] | VariableList]] = Field(None, alias="variables", description="List of instance variables")
    status: Optional[str] = Field(None, description="Status of the instance (e.g., 'active', 'completed')")

    @field_validator("process", mode="before")
    @classmethod
    def normalize_process(cls, value):
        """
        Normalizes the process input to an AgenticProcess instance if it's a dictionary.

        :param value: The input value for process (dict or AgenticProcess).
        :return: AgenticProcess - An AgenticProcess instance.
        :raises ValueError: If the value is neither a dict nor an AgenticProcess.
        """
        if isinstance(value, dict):
            return AgenticProcess.model_validate(value)
        elif isinstance(value, AgenticProcess):
            return value
        raise ValueError("process must be a dictionary or an AgenticProcess instance")

    @field_validator("variables", mode="before")
    @classmethod
    def normalize_variables(cls, value):
        """
        Normalizes the variables input to a VariableList instance.

        :param value: Union[VariableList, List[Variable]] - The input value for variables.
        :return: VariableList - A VariableList instance containing the models.
        """
        if isinstance(value, VariableList):
            return value
        elif isinstance(value, (list, tuple)):
            return VariableList(variables=value)
        elif value is None:
            return VariableList(variables=[])

        raise ValueError("variables must be a VariableList or a list of Variable instances")

    def to_dict(self):
        result = {
            "id": self.id,
            "process": self.process.to_dict() if self.process else None,
            "createdAt": self.created_at,
            "subject": self.subject,
            "variables": self.variables.to_dict() if self.variables else None,
            "status": self.status,
        }
        return {k: v for k, v in result.items() if v is not None}


class ProcessInstanceList(CustomBaseModel):
    instances: List[ProcessInstance] = Field(..., alias="instances", description="List of process instances")

    def to_dict(self):
        return [instance.to_dict() for instance in self.instances] if self.instances else None

    def __getitem__(self, index: int) -> ProcessInstance:
        if self.instances is None:
            raise IndexError("ProcessInstanceList is empty")
        return self.instances[index]

    def __len__(self) -> int:
        return len(self.instances) if self.instances else 0

    def __iter__(self):
        """Make ProcessInstanceList iterable over its instances."""
        if self.instances is None:
            return iter([])
        return iter(self.instances)

