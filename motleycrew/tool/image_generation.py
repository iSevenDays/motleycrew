import logging
from typing import Optional

import os
import requests
import mimetypes

from langchain.agents import Tool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper

from .tool import MotleyTool
import motleycrew.common.utils as motley_utils


def download_image(url: str, file_path: str) -> Optional[str]:
    response = requests.get(url, stream=True)
    if response.status_code == requests.codes.ok:
        content_type = response.headers.get("content-type")
        extension = mimetypes.guess_extension(content_type)
        if not extension:
            extension = ".png"  # default to .png if content-type is not recognized

        file_path_with_extension = file_path + extension
        logging.info("Downloading image %s to %s", url, file_path_with_extension)

        with open(file_path_with_extension, "wb") as f:
            for chunk in response:
                f.write(chunk)

        return file_path_with_extension
    else:
        logging.error("Failed to download image. Status code: %s", response.status_code)


class DallEImageGeneratorTool(MotleyTool):
    def __init__(self, images_directory: Optional[str] = None):
        langchain_tool = create_dalle_image_generator_langchain_tool(
            images_directory=images_directory
        )
        super().__init__(langchain_tool)


class DallEToolInput(BaseModel):
    """Input for the Dall-E tool."""

    description: str = Field(description="image description")


def run_dalle_and_save_images(
    description: str, images_directory: Optional[str] = None, file_name_length: int = 8
) -> Optional[list[str]]:
    dalle_api = DallEAPIWrapper()
    dalle_result = dalle_api.run(query=description)
    logging.info("Dall-E API output: %s", dalle_result)

    urls = dalle_result.split(dalle_api.separator)
    if not len(urls) or not motley_utils.is_http_url(urls[0]):
        logging.error("Dall-E API did not return a valid url: %s", dalle_result)
        return

    if images_directory:
        os.makedirs(images_directory, exist_ok=True)
        file_paths = []
        for url in urls:
            file_name = motley_utils.generate_hex_hash(url, length=file_name_length)
            file_path = os.path.join(images_directory, file_name)

            file_path_with_extension = download_image(url=url, file_path=file_path)
            file_paths.append(file_path_with_extension)
        return file_paths
    else:
        logging.info("Images directory is not provided, returning URLs")
        return urls


def create_dalle_image_generator_langchain_tool(images_directory: Optional[str] = None):
    def run_dalle_and_save_images_partial(description: str):
        return run_dalle_and_save_images(
            description=description, images_directory=images_directory
        )

    return Tool(
        name="Dall-E-Image-Generator",
        func=run_dalle_and_save_images_partial,
        description="A wrapper around OpenAI DALL-E API. Useful for when you need to generate images from a text description. "
        "Input should be an image description.",
        args_schema=DallEToolInput,
    )
