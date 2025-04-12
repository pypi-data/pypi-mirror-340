"""Base agent implementation."""

import abc
from typing import Any, Iterator
from langgraph.graph import Graph

class BaseAgent(abc.ABC):
    def __init__(self, llm_configs: dict, prompt_dir: str = "prompts"):
        """
        Initialize the base agent.
        
        Args:
            llm_configs: Dictionary specifying provider, model, and roles
            prompt_dir: Directory for prompt templates
        """
        self.llm_configs = llm_configs
        self.prompt_dir = prompt_dir
        self.graph: Graph = None  # set by self.build_graph()
        
        # Subclass is expected to build its graph
        self.build_graph()
    
    @abc.abstractmethod
    def build_graph(self) -> None:
        """Construct the LangGraph used by this agent pattern."""
        pass
    
    @abc.abstractmethod
    def run(self, input_data: Any) -> Any:
        """
        Run the agent to completion with the given input.
        
        Args:
            input_data: The user query or initial state
            
        Returns:
            The final output or answer
        """
        pass