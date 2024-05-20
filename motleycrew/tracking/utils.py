import os
from typing import List, Optional
import logging

from lunary import LunaryCallbackHandler
from langchain_core.callbacks import BaseCallbackHandler, BaseCallbackManager
from langchain_core.runnables import RunnableConfig, ensure_config

from .callbacks import LlamaIndexLunaryCallbackHandler
from motleycrew.common import LLMFramework


def get_lunary_public_key():
    """Return lunary public key or None"""
    key = (
        os.environ.get("LUNARY_PUBLIC_KEY")
        or os.getenv("LUNARY_APP_ID")
        or os.getenv("LLMONITOR_APP_ID")
    )
    if not key:
        logging.warning("Lunary public key is not set, tracking will be disabled")
    return key


def create_lunary_callback() -> LunaryCallbackHandler:
    """Creation new LunaryCallbackHandler object"""
    lunary_public_key = get_lunary_public_key()
    if lunary_public_key is not None:
        return LunaryCallbackHandler(app_id=lunary_public_key)


def get_llamaindex_default_callbacks():
    """Return tracking for llamaindex platform"""
    _default_callbacks = []

    # init lunary callback
    lunary_public_key = get_lunary_public_key()
    if lunary_public_key is not None:
        _default_callbacks.append(LlamaIndexLunaryCallbackHandler(lunary_public_key))

    return _default_callbacks


def get_langchain_default_callbacks():
    """Return tracking for langchain platform"""
    _default_callbacks = []

    # init lunary callback
    lunary_callback = create_lunary_callback()
    if lunary_callback is not None:
        _default_callbacks.append(lunary_callback)

    return _default_callbacks


DEFAULT_CALLBACKS_MAP = {
    LLMFramework.LANGCHAIN: get_langchain_default_callbacks,
    LLMFramework.LLAMA_INDEX: get_llamaindex_default_callbacks,
}


def get_default_callbacks_list(
    framework_name: str = LLMFramework.LANGCHAIN,
) -> List[BaseCallbackHandler]:
    """Return list of defaults tracking"""
    _default_callbacks = []
    dc_factory = DEFAULT_CALLBACKS_MAP.get(framework_name, None)

    if callable(dc_factory):
        _default_callbacks = dc_factory()
    else:
        msg = "Default callbacks are not implemented for {} framework".format(framework_name)
        logging.warning(msg)

    return _default_callbacks


def add_callback_handlers_to_config(
    config: RunnableConfig,
    handlers: List[BaseCallbackHandler],
    unique_cls: bool = True,
) -> RunnableConfig:
    """
    Add callback handlers to langchain config
    unique_cls: bool - flag adding callback with a unique class
    return : modified config
    """
    if isinstance(config.get("callbacks"), BaseCallbackManager):
        callback_manager = config.get("callbacks")
        existing_handlers = callback_manager.handlers
    else:
        callback_manager = config.get("callbacks") or []
        existing_handlers = config.get("callbacks") or []

    def add_handler(handler):
        if isinstance(callback_manager, BaseCallbackManager):
            callback_manager.add_handler(handler)
        else:
            callback_manager.append(handler)

    for handler in handlers:
        if unique_cls and not any(
            isinstance(handler, existing.__class__) for existing in existing_handlers
        ):
            add_handler(handler)
        elif handler not in existing_handlers:
            add_handler(handler)

    config["callbacks"] = callback_manager
    return config


def add_default_callbacks_to_langchain_config(
    config: Optional[RunnableConfig] = None,
) -> RunnableConfig:
    """Add default callback to langchain config
    return: modified config
    """
    if config is None:
        config = ensure_config(config)

    default_callbacks = get_default_callbacks_list()
    if default_callbacks:
        config = add_callback_handlers_to_config(config, default_callbacks)
    return config
