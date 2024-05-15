from typing import Union

from langchain.tools import BaseTool

try:
    from llama_index.core.tools import BaseTool as LlamaIndex__BaseTool
    from llama_index.core.tools import FunctionTool as LlamaIndex__FunctionTool
except ImportError:
    pass

from motleycrew.agent.parent import MotleyAgentAbstractParent
from motleycrew.common.utils import ensure_module_is_installed


def normalize_input(args, kwargs):
    if "tool_input" in kwargs:
        return kwargs["tool_input"]
    else:
        return args[0]


class MotleyTool:
    """
    Base tool class compatible with MotleyAgents.
    It is a wrapper for LangChain's BaseTool, containing all necessary adapters and converters.
    """

    def __init__(self, tool: BaseTool):
        self.tool = tool

    @property
    def name(self):
        # TODO: do we really want to make a thin wrapper in this fashion?
        return self.tool.name

    def invoke(self, *args, **kwargs):
        return self.tool.invoke(*args, **kwargs)

    @staticmethod
    def from_langchain_tool(langchain_tool: BaseTool) -> "MotleyTool":
        return MotleyTool(tool=langchain_tool)

    @staticmethod
    def from_llama_index_tool(llama_index_tool: LlamaIndex__BaseTool) -> "MotleyTool":
        ensure_module_is_installed("llama_index")
        langchain_tool = llama_index_tool.to_langchain_tool()
        return MotleyTool.from_langchain_tool(langchain_tool=langchain_tool)

    @staticmethod
    def from_supported_tool(tool: Union["MotleyTool", BaseTool, LlamaIndex__BaseTool]):
        if isinstance(tool, MotleyTool):
            return tool
        elif isinstance(tool, BaseTool):
            return MotleyTool.from_langchain_tool(tool)
        elif isinstance(tool, LlamaIndex__BaseTool):
            return MotleyTool.from_llama_index_tool(tool)
        elif isinstance(tool, MotleyAgentAbstractParent):
            return tool.as_tool()
        else:
            raise Exception(
                f"Tool type `{type(tool)}` is not supported, please convert to MotleyTool first"
            )

    def to_langchain_tool(self) -> BaseTool:
        return self.tool

    def to_llama_index_tool(self) -> LlamaIndex__BaseTool:
        ensure_module_is_installed("llama_index")
        llama_index_tool = LlamaIndex__FunctionTool.from_defaults(
            fn=self.tool._run,
            name=self.tool.name,
            description=self.tool.description,
            fn_schema=self.tool.args_schema,
        )
        return llama_index_tool
