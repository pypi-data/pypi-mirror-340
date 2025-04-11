#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2025.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import json
import os
from pathlib import Path
from typing import Any

import tomli
import typer
from ibm_watsonx_ai import APIClient, Credentials  # type: ignore[import-untyped]

from ibm_watsonx_ai_cli.utils.config import (
    get_deployment_id,
    get_deployment_space_id,
    get_deployment_url,
    get_payload_path,
    load_config,
)

REPO_ZIP_URL = (
    "https://github.com/IBM/watsonx-developer-hub/archive/refs/heads/main.zip"
)
EXTRACTED_REPO_DIR = "watsonx-developer-hub-main"
AGENTS_SUBDIR = "agents"


def get_from_env(
    key: str, env_key: str, default: str | None = None, allow_empty: bool = False
) -> str | None:
    """
    Retrieve the value of an environment variable, ensuring it is non-empty.

    Parameters:
        key (str): A descriptive name for the variable (used in error messages).
        env_key (str): The name of the environment variable to retrieve.
        default (str | None, optional): The default value to return if the environment variable
            is not set or is empty. Defaults to None.
        allow_empty (bool): Skip raise error, Default to False.

    Returns:
        str: The non-empty value of the environment variable, or the default value if provided.

    Raises:
        ValueError: If the environment variable is not set or is empty and no default is provided.
    """
    value = os.environ.get(env_key, "").strip()
    if value:
        return value
    elif default is not None:
        return default
    else:
        if not allow_empty:
            raise ValueError(
                f"Did not find {key}. Please set environment variable `{env_key}` with a valid value."
            )
        return None


def get_project_or_space_from_env() -> dict:
    """
    Get project_id or space_id from environment variable.

    Raises:
        ValueError: If not exactly one of `WATSONX_SPACE_ID` or `WATSONX_PROJECT_ID` is set.
    """
    space_id = os.environ.get("WATSONX_SPACE_ID", "").strip() or None
    project_id = os.environ.get("WATSONX_PROJECT_ID", "").strip() or None

    if (bool(space_id) and bool(project_id)) or (not space_id and not project_id):
        raise ValueError(
            "Please ensure that only one of the environment variables, `WATSONX_SPACE_ID` or `WATSONX_PROJECT_ID`, is set. Do not set both simultaneously."
        )

    return {"space_id": space_id, "project_id": project_id}


def prepare_client() -> APIClient:
    """
    Prepares and returns an initialized IBM watsonx.ai APIClient.

    Returns:
        APIClient: An initialized API client created using the retrieved configuration.
    """
    try:
        config = load_config()
        dep_config = config["deployment"]

        url = dep_config["watsonx_url"]
        api_key = dep_config.get("watsonx_apikey") or None
        token = dep_config.get("watsonx_token") or None
        password = dep_config.get("watsonx_password") or None
        username = dep_config.get("watsonx_username") or None
        instance_id = dep_config.get("watsonx_instance_id") or None

        project_space_dict = {
            "space_id": dep_config.get("space_id", None),
            "project_id": dep_config.get("project_id", None),
        }

    except FileNotFoundError:
        url = get_from_env("watsonx_url", "WATSONX_URL", allow_empty=False)

        api_key = get_from_env("watsonx_apikey", "WATSONX_APIKEY", allow_empty=True)
        token = get_from_env("watsonx_token", "WATSONX_TOKEN", allow_empty=True)
        password = get_from_env(
            "watsonx_password", "WATSONX_PASSWORD", allow_empty=True
        )
        username = get_from_env(
            "watsonx_username", "WATSONX_USERNAME", allow_empty=True
        )
        instance_id = get_from_env(
            "watsonx_instance_id", "WATSONX_INSTANCE_ID", allow_empty=True
        )
        if "cloud.ibm.com" in url:
            if api_key is None and token is None:
                raise ValueError(
                    "Did not find `watsonx_apikey` or `watsonx_token`. Please set environment variable `WATSONX_APIKEY` or `WATSONX_TOKEN` with a valid value."
                )
        else:
            if api_key is None and token is None and password is None:
                raise ValueError(
                    "Did not find `watsonx_apikey`, `watsonx_token` or `watsonx_password`. Please set environment variable `WATSONX_APIKEY`, `WATSONX_TOKEN` or `WATSONX_PASSWORD` with a valid value."
                )
            if (api_key or password) is not None and username is None:
                raise ValueError(
                    "Did not find `watsonx_username`. Please set environment variable `WATSONX_USERNAME` with a valid value."
                )
            if instance_id is None:
                raise ValueError(
                    "Did not find `watsonx_instance_id`. Please set environment variable `WATSONX_INSTANCE_ID` with a valid value."
                )

        project_space_dict = get_project_or_space_from_env()

    return APIClient(
        credentials=Credentials(
            url=url,
            api_key=api_key,
            token=token,
            password=password,
            username=username,
            instance_id=instance_id,
        ),
        space_id=project_space_dict["space_id"],
        project_id=project_space_dict["project_id"],
    )


def prepare_agents_prompt(agents: list, ask: bool = False) -> str:
    """
    Construct a formatted prompt listing available templates.

    Args:
        agents (List): A list of available template names.
        ask (bool, optional): If True, append a question prompting the user to choose a template. Defaults to False.

    Returns:
        str: The formatted prompt string.
    """
    prompt = typer.style(
        "\nList of available templates:\n\n", fg="bright_blue", bold=True
    )
    for i, agent in enumerate(agents):
        prompt += typer.style(f"{i + 1}. {agent}\n")
    if ask:
        prompt += typer.style(
            "\nWhich template do you want to start with?", fg="bright_blue", bold=True
        )

    return prompt


def get_package_root(agent_dir: Path | None = None) -> Path:
    """
    Locate the package root by searching for a pyproject.toml file.

    Starts from the current working directory (optionally extended by agent_dir)
    and traverses upward until a directory containing a pyproject.toml file is found.

    Args:
        agent_dir (Optional[Path], optional): An optional subdirectory to start from. Defaults to None.

    Returns:
        Path: The directory containing the pyproject.toml file.

    Raises:
        FileNotFoundError: If no pyproject.toml file is found in any parent directory.
    """
    package_root = Path.cwd()
    if agent_dir:
        package_root = package_root / agent_dir
    visited: set[Path] = set()
    while package_root not in visited:
        visited.add(package_root)
        pyproject_path = package_root / "pyproject.toml"
        if pyproject_path.exists():
            return package_root
        package_root = package_root.parent
    raise FileNotFoundError(
        "No pyproject.toml found. Please ensure you are in the template folder's directory."
    )


def template_exists(template: str, available_templates: list) -> bool:
    """
    Check if a given template exists within the available templates list.

    The function treats the input as a full template path if it contains a "/".
    Otherwise, it checks if any available template ends with "/{template}".

    Args:
        template (str): The template name or full path to check.
        available_templates (list): List of available template paths.

    Returns:
        bool: True if the template exists, False otherwise.
    """
    if "/" in template:
        return template in available_templates
    else:
        return any(item.endswith(f"/{template}") for item in available_templates)


def prompt_choice(question: str, options: list[str]) -> str:
    """
    Displays a question along with a list of allowed options and continues to prompt
    until the user provides a valid answer.

    Args:
        question (str): The question to display.
        options (list[str]): A list of allowed answers.

    Returns:
        str: The user's answer from the list of allowed options.
    """
    options_str = "/".join(options)
    while True:
        answer = (
            typer.prompt(typer.style(f"{question} ({options_str})", fg="bright_blue"))
            .strip()
            .lower()
        )
        if answer in options:
            return answer
        typer.echo(
            typer.style(
                f"Invalid option. Please choose one of: {options_str}.", fg="bright_red"
            )
        )


def select_template_by_index(value: str, available_templates: list[str]) -> str | None:
    """Attempts to return the template based on the provided index (as a string)."""
    try:
        index = int(value) - 1
        if index < 0:
            return None
        return available_templates[index]
    except (ValueError, IndexError):
        return None


def get_template_name(
    available_templates: list[str], template_name: str | None = None
) -> str:
    """
    Validate the provided template name or prompt the user to select one.

    Args:
        available_templates (list[str]): A list of valid template names.
        template_name (str | None): The template name provided by the user. If None,
            the user will be prompted to select a template.

    Returns:
        str: The validated template name selected or provided by the user.

    Raises:
        typer.Exit: If the provided or selected template name is not found in the available_agents list.
    """
    if template_name is None:
        template_name = typer.prompt(
            prepare_agents_prompt(available_templates, ask=True)
        )

    selected = select_template_by_index(template_name, available_templates)
    if selected is not None:
        return selected

    if template_name.isnumeric():
        typer.echo(
            typer.style(
                f"!!! Cannot find template numbered {template_name}",
                fg="bright_red",
                bold=True,
            )
        )
        raise typer.Exit(code=1)

    if not template_exists(template_name, available_templates):
        typer.echo(
            typer.style(
                f"!!! Cannot find template '{template_name}'. Available templates: {available_templates}",
                fg="bright_red",
                bold=True,
            )
        )
        raise typer.Exit(code=1)
    return template_name


def get_directory(selected_agent: str, directory: str | None) -> str:
    """
    Retrieve the target directory for template creation.

    Args:
        directory (str | None): The target directory name. If None, the user will be prompted.

    Returns:
        str: The directory name to be used as the target folder.
    """
    shorted_selected_agent = selected_agent.split("/")[-1]
    if directory is None:
        directory = typer.prompt(
            typer.style(
                f"The name of the folder to create (press Enter to use default name: '{shorted_selected_agent}')",
                fg="bright_blue",
            ),
            default=shorted_selected_agent,
            show_default=False,
        )
    return directory


def load_question_payload() -> Any:
    """
    Load the question payload from the file specified in the configuration.

    Returns:
        Any: The JSON-decoded payload from the file.

    Raises:
        typer.Exit: If the payload path is not defined or if loading the JSON fails.
    """
    payload_path = get_payload_path()
    if payload_path:
        try:
            with open(payload_path, "r") as f:
                return json.load(f)
        except Exception as e:
            typer.echo(
                typer.style(
                    f"Failed to load payload from {payload_path}: {e}",
                    fg="bright_red",
                    bold=True,
                )
            )
            raise typer.Exit(code=1)
    else:
        typer.echo(
            typer.style(
                "Payload not provided. Please specify the `question` parameter or define the `payload_path` in the `[cli.options]` section of `config.toml` file.",
                fg="bright_red",
                bold=True,
            )
        )
        raise typer.Exit(code=1)


def get_ai_service_dashboard_url(client: APIClient, deployment_id: str) -> str | None:
    """
    Generate the AI service dashboard URL for a given deployment.

    Args:
        client (APIClient): The APIClient instance.
        deployment_id (str): The unique identifier for the deployment.

    Returns:
        str | None: The formatted AI service dashboard URL. If any component is
                    missing, it returns None.
    """
    space_id = get_deployment_space_id()
    platform_url = client.PLATFORM_URLS_MAP[get_deployment_url()]

    ai_service_dashboard_url = (
        f"{platform_url}/ml-runtime/deployments/{deployment_id}?space_id={space_id}"
    )

    return ai_service_dashboard_url.replace("api.", "")


def prompt_and_get_deployment_id() -> str | None:
    typer.echo(
        typer.style(
            "The `deployment_id`, as specified in the `deployment` section of your config.toml file, is employed.",
            fg="bright_green",
            bold=True,
        )
    )

    return get_deployment_id()


def get_package_name(pyproject_path: Path) -> str:
    """
    Extract the package name from a pyproject.toml file.

    Args:
        pyproject_path (Path): Path to the pyproject.toml file.

    Returns:
        str: A str containing the package name.

    Raises:
        ValueError: If either the package name is missing in the file.
    """
    with open(pyproject_path, "rb") as f:
        pyproject_data = tomli.load(f)
    tool_poetry = pyproject_data.get("tool", {}).get("poetry", {})
    package_name = tool_poetry.get("name")
    if not package_name:
        raise ValueError("Package name is missing in pyproject.toml.")
    return package_name
