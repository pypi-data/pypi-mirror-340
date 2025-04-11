from typing import Any, Optional, List

from loguru import logger

from any_agent.config import AgentFramework, AgentConfig
from any_agent.tools.wrappers import import_and_wrap_tools
from .any_agent import AnyAgent

try:
    from langchain.chat_models import init_chat_model
    from langgraph.prebuilt import create_react_agent
    from langgraph.graph.graph import CompiledGraph

    langchain_available = True
except ImportError:
    langchain_available = False


class LangchainAgent(AnyAgent):
    """LangChain agent implementation that handles both loading and running."""

    def __init__(
        self, config: AgentConfig, managed_agents: Optional[list[AgentConfig]] = None
    ):
        self.managed_agents = managed_agents
        self.config = config
        self._agent = None
        self._tools = []
        self._load_agent()

    @logger.catch(reraise=True)
    def _load_agent(self) -> None:
        """Load the LangChain agent with the given configuration."""
        if not langchain_available:
            raise ImportError(
                "You need to `pip install langchain langgraph` to use this agent"
            )

        if not self.config.tools:
            self.config.tools = [
                "any_agent.tools.search_web",
                "any_agent.tools.visit_webpage",
            ]

        if self.managed_agents:
            raise NotImplementedError("langchain managed agents are not supported yet")

        imported_tools, mcp_managers = import_and_wrap_tools(
            self.config.tools, agent_framework=AgentFramework.LANGCHAIN
        )

        # Extract tools from MCP managers and add them to the imported_tools list
        for manager in mcp_managers:
            imported_tools.extend(manager.tools)

        if "/" in self.config.model_id:
            model_provider, model_id = self.config.model_id.split("/")
            model = init_chat_model(
                model=model_id,
                model_provider=model_provider,
                **self.config.model_args or {},
            )
        else:
            model = init_chat_model(
                self.config.model_id, **self.config.model_args or {}
            )

        self._agent: CompiledGraph = create_react_agent(
            model=model,
            tools=imported_tools,
            prompt=self.config.instructions,
            **self.config.agent_args or {},
        )
        # Langgraph doesn't let you easily access what tools are loaded from the CompiledGraph, so we'll store a list of them in this class
        self._tools = imported_tools

    @logger.catch(reraise=True)
    def run(self, prompt: str) -> Any:
        """Run the LangChain agent with the given prompt."""
        inputs = {"messages": [("user", prompt)]}
        message = None
        for s in self._agent.stream(inputs, stream_mode="values"):
            message = s["messages"][-1]
            if isinstance(message, tuple):
                logger.debug(message)
            else:
                message.pretty_print()
        return message

    @property
    def tools(self) -> List[str]:
        """
        Return the tools used by the agent.
        This property is read-only and cannot be modified.
        """
        return self._tools
