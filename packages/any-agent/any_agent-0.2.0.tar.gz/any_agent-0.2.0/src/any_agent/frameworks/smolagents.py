import os
from typing import Optional, Any, List

from loguru import logger

from any_agent.config import AgentFramework, AgentConfig
from any_agent.tools.wrappers import import_and_wrap_tools
from .any_agent import AnyAgent

try:
    import smolagents
    from smolagents import MultiStepAgent

    smolagents_available = True
except ImportError:
    smolagents_available = None

DEFAULT_AGENT_TYPE = "CodeAgent"
DEFAULT_MODEL_CLASS = "LiteLLMModel"


class SmolagentsAgent(AnyAgent):
    """Smolagents agent implementation that handles both loading and running."""

    def __init__(
        self, config: AgentConfig, managed_agents: Optional[list[AgentConfig]] = None
    ):
        self.managed_agents = managed_agents
        self.config = config
        self._agent = None
        self._load_agent()

    def _get_model(self, agent_config: AgentConfig):
        """Get the model configuration for a smolagents agent."""
        model_type = getattr(smolagents, agent_config.model_type or DEFAULT_MODEL_CLASS)
        kwargs = {
            "model_id": agent_config.model_id,
        }
        model_args = agent_config.model_args or {}
        if api_key_var := model_args.pop("api_key_var", None):
            kwargs["api_key"] = os.environ[api_key_var]
        return model_type(**kwargs, **model_args)

    def _merge_mcp_tools(self, mcp_servers):
        """Merge MCP tools from different servers."""
        tools = []
        for mcp_server in mcp_servers:
            tools.extend(mcp_server.tools)
        return tools

    @logger.catch(reraise=True)
    def _load_agent(self) -> None:
        """Load the Smolagents agent with the given configuration."""
        if not smolagents_available:
            raise ImportError("You need to `pip install smolagents` to use this agent")

        if not self.managed_agents and not self.config.tools:
            self.config.tools = [
                "any_agent.tools.search_web",
                "any_agent.tools.visit_webpage",
            ]

        tools, mcp_servers = import_and_wrap_tools(
            self.config.tools, agent_framework=AgentFramework.SMOLAGENTS
        )
        tools.extend(self._merge_mcp_tools(mcp_servers))

        managed_agents_instanced = []
        if self.managed_agents:
            for managed_agent in self.managed_agents:
                agent_type = getattr(
                    smolagents, managed_agent.agent_type or DEFAULT_AGENT_TYPE
                )
                managed_tools, managed_mcp_servers = import_and_wrap_tools(
                    managed_agent.tools, agent_framework=AgentFramework.SMOLAGENTS
                )
                tools.extend(self._merge_mcp_tools(managed_mcp_servers))
                managed_agent_instance = agent_type(
                    name=managed_agent.name,
                    model=self._get_model(managed_agent),
                    tools=managed_tools,
                    verbosity_level=-1,  # OFF
                    description=managed_agent.description
                    or f"Use the agent: {managed_agent.name}",
                )
                if managed_agent.instructions:
                    managed_agent_instance.prompt_templates["system_prompt"] = (
                        managed_agent.instructions
                    )
                managed_agents_instanced.append(managed_agent_instance)

        main_agent_type = getattr(
            smolagents, self.config.agent_type or DEFAULT_AGENT_TYPE
        )

        self._agent: MultiStepAgent = main_agent_type(
            name=self.config.name,
            model=self._get_model(self.config),
            tools=tools,
            verbosity_level=-1,  # OFF
            managed_agents=managed_agents_instanced,
            **self.config.agent_args or {},
        )

        if self.config.instructions:
            self._agent.prompt_templates["system_prompt"] = self.config.instructions

    @logger.catch(reraise=True)
    def run(self, prompt: str) -> Any:
        """Run the Smolagents agent with the given prompt."""
        result = self._agent.run(prompt)
        return result

    @property
    def tools(self) -> List[str]:
        """
        Return the tools used by the agent.
        This property is read-only and cannot be modified.
        """
        return self._agent.tools
