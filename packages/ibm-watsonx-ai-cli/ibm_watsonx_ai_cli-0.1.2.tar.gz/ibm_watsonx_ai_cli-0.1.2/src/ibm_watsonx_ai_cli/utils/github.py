#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2025.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import os
import re
import shutil
import tempfile
import zipfile

import httpx

# ibm_watsonx_ai requre requests package
import requests  # type:ignore[import-untyped]
import typer

from ibm_watsonx_ai_cli.utils.utils import prompt_choice

REPO_ZIP_URL = (
    "https://github.com/IBM/watsonx-developer-hub/archive/refs/heads/main.zip"
)
EXTRACTED_REPO_DIR = "watsonx-developer-hub-main"
AGENTS_SUBDIR = "agents"


def get_available_agents(raw: bool = False) -> list:
    """
    Retrieve a list of available agent templates from the IBM/watsonx-developer-hub repository.

    Args:
        raw (bool): If True, return the raw list of tree items from the GitHub API.
                    If False, return a formatted list of agent template identifiers.
                    Defaults to False.

    Returns:
        list: A list of available agent templates. The list will contain formatted strings
              (e.g., "base/template-name" or "community/template-name") unless 'raw' is True,
              in which case it returns the raw dictionary items from the API response.

    Note:
        In case of HTTP errors or JSON decoding errors, the function prints an error message
        and returns an empty list.
    """
    response = httpx.get(
        "https://api.github.com/repos/IBM/watsonx-developer-hub/git/trees/main?recursive=true",
    )
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
        return []

    try:
        repo_data = response.json()
        tree_items = repo_data.get("tree", [])
    except ValueError:
        print("Error decoding JSON response")
        return []

    agent_regex = r"^agents/(?:base|community)/[A-Za-z0-9_-]+$"
    formatted_agents = []
    for tree in tree_items:
        if tree.get("type") == "tree" and re.match(agent_regex, tree.get("path", "")):
            parts = tree["path"].split("/")
            if len(parts) >= 3:
                formatted_agents.append(f"{parts[1]}/{parts[2]}")

    if raw:
        return [
            tree
            for tree in tree_items
            if tree.get("type") == "tree"
            and re.match(agent_regex, tree.get("path", ""))
        ]
    else:
        return formatted_agents


def download_and_extract_template(agent_name: str, target_dir: str) -> str:
    """
    Download the repository ZIP, extract the specified template folder, and copy it to the target directory.

    Args:
        agent_name (str): The name of the template to download and extract.
        target_dir (str): The local directory where the template should be copied.

    Raises:
        typer.Exit: If the repository ZIP cannot be downloaded successfully, if the expected template folder is not
                    found in the extracted contents, or if any error occurs during the extraction/copy process.
    """
    folder_to_extract = os.path.join(EXTRACTED_REPO_DIR, AGENTS_SUBDIR, agent_name)

    try:
        with tempfile.TemporaryDirectory() as tmpdirname:
            zip_path = os.path.join(tmpdirname, "repo.zip")
            response = requests.get(REPO_ZIP_URL)
            if response.status_code != 200:
                raise Exception(
                    f"Failed to download repository ZIP (status code {response.status_code})"
                )
            with open(zip_path, "wb") as f:
                f.write(response.content)

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(tmpdirname)

            source_folder = os.path.join(tmpdirname, folder_to_extract)
            if not os.path.exists(source_folder):
                raise Exception(
                    f"Template folder '{agent_name}' not found in repository."
                )

            if os.path.exists(target_dir) and os.listdir(target_dir):
                overwrite = prompt_choice(
                    question=f"Folder '{target_dir}' already exists. Do you want to overwrite it?",
                    options=["y", "n"],
                )
                if overwrite == "y":
                    shutil.rmtree(target_dir)
                else:
                    target_dir = typer.prompt(
                        typer.style(
                            text="Please specify a new name for the template folder",
                            fg="bright_blue",
                        )
                    )
                    while os.path.exists(target_dir):
                        target_dir = typer.prompt(
                            typer.style(
                                text=f"Folder '{target_dir}' already exists. Please specify a different name",
                                fg="bright_red",
                            )
                        )

            os.makedirs(target_dir, exist_ok=True)

            for item in os.listdir(source_folder):
                src_item_path = os.path.join(source_folder, item)
                dst_item_path = os.path.join(target_dir, item)
                if os.path.isdir(src_item_path):
                    shutil.copytree(src_item_path, dst_item_path, dirs_exist_ok=True)
                else:
                    shutil.copy2(src_item_path, dst_item_path)

            return target_dir

    except Exception as e:
        typer.echo(
            typer.style(
                f"!!! Error downloading template: {e}", fg="bright_red", bold=True
            )
        )
        raise typer.Exit(code=1)
