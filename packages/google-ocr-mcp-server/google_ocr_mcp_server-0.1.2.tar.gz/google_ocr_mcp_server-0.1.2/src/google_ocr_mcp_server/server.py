import json
from contextlib import asynccontextmanager
from typing import AsyncIterator

from google.auth import credentials
from google.cloud import vision
from google.protobuf.json_format import MessageToDict
from loguru import logger
from mcp.server.fastmcp import FastMCP
from pydantic_settings import SettingsConfigDict

from .settings import configs


@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[dict[str, any]]:
    try:
        logger.info("Google OCR MCP server starting up")
        yield {}
    finally:
        logger.info("Google OCR MCP server shut down")


mcp = FastMCP(
    name="google-ocr-mcp-server",
    instructions="Google OCR on images",
    model_config=SettingsConfigDict(
        env_prefix="FASTMCP_",
        env_file=".env",
        extra="ignore",
    ),
    debug=False,
    log_level="INFO",
    host="0.0.0.0",
    port=8080,
    sse_path="/sse",
    message_path="/messages/",
    warn_on_duplicate_resources=True,
    warn_on_duplicate_tools=True,
    warn_on_duplicate_prompts=True,
    dependencies=["GOOGLE_APPLICATION_CREDENTIALS"],
    lifespan=lifespan,
)

_client: vision.ImageAnnotatorClient | None = None


def get_client() -> vision.ImageAnnotatorClient | None:
    global _client
    if not configs.GOOGLE_APPLICATION_CREDENTIALS:
        return None
    if _client is None:
        logger.info("Initializing `ImageAnnotatorClient` ...")
        try:
            credentials = json.load(configs.GOOGLE_APPLICATION_CREDENTIALS)
        except json.JSONDecodeError:
            credentials = configs.GOOGLE_APPLICATION_CREDENTIALS
        try:
            if isinstance(credentials, dict):
                _client = vision.ImageAnnotatorClient.from_service_account_info(
                    credentials
                )
            elif isinstance(credentials, str):
                _client = vision.ImageAnnotatorClient.from_service_account_json(
                    configs.GOOGLE_APPLICATION_CREDENTIALS
                )
            logger.info("`ImageAnnotatorClient` successfully initialized.")
        except Exception as exc:
            logger.error(
                f"Failed to initialize `ImageAnnotatorClient`. Please check the provided credentials and try again. ({exc})"
            )
    return _client


def _without_ext(path: str) -> str:
    return ".".join(path.split(".")[:-1])


@mcp.tool()
async def ocr(path: str) -> str:
    """
    Perform Optical Character Recognition (OCR) on the provided image file.

    Args:
        path (str): The absolute file path to the image on which OCR will be performed.

    Returns:
        str: The extracted text from the image.

    Raises:
        Exception: If an error occurs during the OCR process, it will be logged.

    Notes:
        - The function uses Google Cloud Vision API for text detection.
        - If SAVE_RESULTS is enabled, the OCR results will be saved as a JSON file
          in the same directory as the input image, with the same name but a .json extension.
    """
    client = get_client()
    if client is None:
        return "Google credentials not found. Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable."
    with open(path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    if response.error.message:
        logger.error(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    if configs.SAVE_RESULTS:
        response_dict = MessageToDict(response._pb)
        _path = _without_ext(path)
        with open(_path + ".json", "w") as file:
            json.dump(response_dict, file, ensure_ascii=False)
    return response.full_text_annotation.text
