"""Helper functions to initialize Language Models (LLMs) from different frameworks."""

from motleycrew.common import Defaults
from motleycrew.common import LLMFamily, LLMFramework
from motleycrew.common.exceptions import LLMFamilyNotSupported, LLMFrameworkNotSupported
from motleycrew.common.utils import ensure_module_is_installed


def langchain_openai_llm(
    llm_name: str = Defaults.DEFAULT_LLM_NAME,
    llm_temperature: float = Defaults.DEFAULT_LLM_TEMPERATURE,
    **kwargs,
):
    """Initialize an OpenAI LLM client for use with Langchain.

    Args:
        llm_name: Name of the LLM in OpenAI API.
        llm_temperature: Temperature for the LLM.
    """
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(model=llm_name, temperature=llm_temperature, **kwargs)


def llama_index_openai_llm(
    llm_name: str = Defaults.DEFAULT_LLM_NAME,
    llm_temperature: float = Defaults.DEFAULT_LLM_TEMPERATURE,
    **kwargs,
):
    """Initialize an OpenAI LLM client for use with LlamaIndex.

    Args:
        llm_name: Name of the LLM in OpenAI API.
        llm_temperature: Temperature for the LLM.
    """

    ensure_module_is_installed("llama_index")
    from llama_index.llms.openai import OpenAI

    return OpenAI(model=llm_name, temperature=llm_temperature, **kwargs)


def langchain_anthropic_llm(
    llm_name: str = Defaults.DEFAULT_LLM_NAME,
    llm_temperature: float = Defaults.DEFAULT_LLM_TEMPERATURE,
    **kwargs,
):
    """Initialize an Anthropic LLM client for use with Langchain.

    Args:
        llm_name: Name of the LLM in Anthropic API.
        llm_temperature: Temperature for the LLM.
    """

    from langchain_anthropic import ChatAnthropic

    return ChatAnthropic(model=llm_name, temperature=llm_temperature, **kwargs)


def llama_index_anthropic_llm(
    llm_name: str = Defaults.DEFAULT_LLM_NAME,
    llm_temperature: float = Defaults.DEFAULT_LLM_TEMPERATURE,
    **kwargs,
):
    """Initialize an Anthropic LLM client for use with LlamaIndex.

    Args:
        llm_name: Name of the LLM in Anthropic API.
        llm_temperature: Temperature for the LLM.
    """
    ensure_module_is_installed("llama_index")
    from llama_index.llms.anthropic import Anthropic

    return Anthropic(model=llm_name, temperature=llm_temperature, **kwargs)


def langchain_replicate_llm(
    llm_name: str = Defaults.DEFAULT_LLM_NAME,
    llm_temperature: float = Defaults.DEFAULT_LLM_TEMPERATURE,
    **kwargs,
):
    """Initialize a Replicate LLM client for use with Langchain.

    Args:
        llm_name: Name of the LLM in Replicate API.
        llm_temperature: Temperature for the LLM.
    """
    from langchain_community.llms import Replicate

    model_kwargs = kwargs.pop("model_kwargs", {})
    model_kwargs["temperature"] = llm_temperature

    return Replicate(model=llm_name, model_kwargs=model_kwargs, **kwargs)


def llama_index_replicate_llm(
    llm_name: str = Defaults.DEFAULT_LLM_NAME,
    llm_temperature: float = Defaults.DEFAULT_LLM_TEMPERATURE,
    **kwargs,
):
    """Initialize a Replicate LLM client for use with LlamaIndex.

    Args:
        llm_name: Name of the LLM in Replicate API.
        llm_temperature: Temperature for the LLM.
    """
    ensure_module_is_installed("llama_index")
    from llama_index.llms.replicate import Replicate

    return Replicate(model=llm_name, temperature=llm_temperature, **kwargs)


def langchain_together_llm(
    llm_name: str = Defaults.DEFAULT_LLM_NAME,
    llm_temperature: float = Defaults.DEFAULT_LLM_TEMPERATURE,
    **kwargs,
):
    """Initialize a Together LLM client for use with Langchain.

    Args:
        llm_name: Name of the LLM in Together API.
        llm_temperature: Temperature for the LLM.
    """
    from langchain_together import ChatTogether

    return ChatTogether(model=llm_name, temperature=llm_temperature, **kwargs)


def llama_index_together_llm(
    llm_name: str = Defaults.DEFAULT_LLM_NAME,
    llm_temperature: float = Defaults.DEFAULT_LLM_TEMPERATURE,
    **kwargs,
):
    """Initialize a Together LLM client for use with LlamaIndex.

    Args:
        llm_name: Name of the LLM in Together API.
        llm_temperature: Temperature for the LLM.
    """
    ensure_module_is_installed("llama_index")
    from llama_index.llms.together import TogetherLLM

    return TogetherLLM(model=llm_name, temperature=llm_temperature, **kwargs)


def langchain_groq_llm(
    llm_name: str = Defaults.DEFAULT_LLM_NAME,
    llm_temperature: float = Defaults.DEFAULT_LLM_TEMPERATURE,
    **kwargs,
):
    """Initialize a Groq LLM client for use with Langchain.

    Args:
        llm_name: Name of the LLM in Groq API.
        llm_temperature: Temperature for the LLM.
    """
    from langchain_groq import ChatGroq

    return ChatGroq(model=llm_name, temperature=llm_temperature, **kwargs)


def llama_index_groq_llm(
    llm_name: str = Defaults.DEFAULT_LLM_NAME,
    llm_temperature: float = Defaults.DEFAULT_LLM_TEMPERATURE,
    **kwargs,
):
    """Initialize a Groq LLM client for use with LlamaIndex.

    Args:
        llm_name: Name of the LLM in Groq API.
        llm_temperature: Temperature for the LLM.
    """
    ensure_module_is_installed("llama_index")
    from llama_index.llms.groq import Groq

    return Groq(model=llm_name, temperature=llm_temperature, **kwargs)


def langchain_ollama_llm(
    llm_name: str = Defaults.DEFAULT_LLM_NAME,
    llm_temperature: float = Defaults.DEFAULT_LLM_TEMPERATURE,
    **kwargs,
):
    """Initialize an Ollama LLM client for use with Langchain.

    Args:
        llm_name: Name of the LLM in Ollama API.
        llm_temperature: Temperature for the LLM.
    """
    from langchain_ollama.llms import OllamaLLM

    return OllamaLLM(model=llm_name, temperature=llm_temperature, **kwargs)


def llama_index_ollama_llm(
    llm_name: str = Defaults.DEFAULT_LLM_NAME,
    llm_temperature: float = Defaults.DEFAULT_LLM_TEMPERATURE,
    **kwargs,
):
    """Initialize an Ollama LLM client for use with LlamaIndex.

    Args:
        llm_name: Name of the LLM in Ollama API.
        llm_temperature: Temperature for the LLM.
    """
    ensure_module_is_installed("llama_index")
    from llama_index.llms.ollama import Ollama

    return Ollama(model=llm_name, temperature=llm_temperature, **kwargs)


Defaults.LLM_MAP = {
    (LLMFramework.LANGCHAIN, LLMFamily.OPENAI): langchain_openai_llm,
    (LLMFramework.LLAMA_INDEX, LLMFamily.OPENAI): llama_index_openai_llm,
    (LLMFramework.LANGCHAIN, LLMFamily.ANTHROPIC): langchain_anthropic_llm,
    (LLMFramework.LLAMA_INDEX, LLMFamily.ANTHROPIC): llama_index_anthropic_llm,
    (LLMFramework.LANGCHAIN, LLMFamily.REPLICATE): langchain_replicate_llm,
    (LLMFramework.LLAMA_INDEX, LLMFamily.REPLICATE): llama_index_replicate_llm,
    (LLMFramework.LANGCHAIN, LLMFamily.TOGETHER): langchain_together_llm,
    (LLMFramework.LLAMA_INDEX, LLMFamily.TOGETHER): llama_index_together_llm,
    (LLMFramework.LANGCHAIN, LLMFamily.GROQ): langchain_groq_llm,
    (LLMFramework.LLAMA_INDEX, LLMFamily.GROQ): llama_index_groq_llm,
    (LLMFramework.LANGCHAIN, LLMFamily.OLLAMA): langchain_ollama_llm,
    (LLMFramework.LLAMA_INDEX, LLMFamily.OLLAMA): llama_index_ollama_llm,
}


def init_llm(
    llm_framework: str,
    llm_family: str = Defaults.DEFAULT_LLM_FAMILY,
    llm_name: str = Defaults.DEFAULT_LLM_NAME,
    llm_temperature: float = Defaults.DEFAULT_LLM_TEMPERATURE,
    **kwargs,
):
    """Initialize an LLM client for use with the specified framework and family.

    Args:
        llm_framework: Framework of the LLM client.
        llm_family: Family of the LLM.
        llm_name: Name of the LLM.
        llm_temperature: Temperature for the LLM.
    """

    func = Defaults.LLM_MAP.get((llm_framework, llm_family), None)
    if func is not None:
        return func(llm_name=llm_name, llm_temperature=llm_temperature, **kwargs)

    raise LLMFamilyNotSupported(llm_framework=llm_framework, llm_family=llm_family)
