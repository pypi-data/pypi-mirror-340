"""Openlayer platform MCP server.

Provides tools that an MCP client can use to interact with the Openlayer
platform.
"""

import os
from typing import Dict, List

from mcp.server.fastmcp import FastMCP
from openlayer import Openlayer
from openlayer.lib.data import commit

mcp = FastMCP("openlayer-mcp")
client = Openlayer()


# --------------------------------- Projects --------------------------------- #
@mcp.tool()
def list_projects() -> List[Dict]:
    """Get a list of the projects in the user's workspace."""
    project_list = client.projects.list()
    return [item.model_dump() for item in project_list.items]


@mcp.tool()
def create_project(
    name: str,
    task_type: str,
    description: str,
) -> Dict:
    """Create a new project in the user's workspace.

    Args:
        name: The name of the project to create.
        task_type: The type of task the project will be used for. Must be one of
            'llm-base', 'tabular-classification', 'tabular-regression', or
            'text-classification'.
        description: A short description for the project.
    """
    project = client.projects.create(
        name=name,
        task_type=task_type,
        description=description,
    )
    return project.model_dump()


# ---------------------------------- Commits --------------------------------- #
@mcp.tool()
def list_commits(project_id: str) -> List[Dict]:
    """List the commits in a project.

    Args:
        project_id: The ID of the project to list the commits for.
    """
    commits = client.projects.commits.list(project_id=project_id)
    return [item.model_dump() for item in commits.items]


@mcp.tool()
def retrieve_commit(project_version_id: str) -> Dict:
    """Retrieve a commit by ID.

    Args:
        project_version_id: The ID of the commit to retrieve.
    """
    commit = client.commits.retrieve(project_version_id=project_version_id)
    return commit.model_dump()


@mcp.tool()
def push_commit(
    project_id: str,
    directory: str,
    message: str = "New commit",
) -> str:
    """Push a commit to the project.

    Args:
        project_id: The ID of the project to push the commit to.
        directory: The directory containing the files to push. Usually has at least
            an `openlayer.json` file.
        message: The commit message.
    """
    # Check if the directory contains an openlayer.json file
    if not os.path.exists(os.path.join(directory, "openlayer.json")):
        raise ValueError(
            f"Directory {directory} does not contain an openlayer.json file, so "
            "it is not prepared to be pushed to Openlayer."
        )
    try:
        commit.push(
            client=client,
            directory=directory,
            project_id=project_id,
            message=message,
        )
    except Exception as exc:
        raise ValueError(f"Error pushing commit: {exc}")
    return "Commit pushed successfully."


# ---------------------------- Inference pipelines --------------------------- #
@mcp.tool()
def list_inference_pipelines(project_id: str) -> List[Dict]:
    """List the inference pipelines in a project."""
    inference_pipelines = client.projects.inference_pipelines.list(
        project_id=project_id
    )
    return [item.model_dump() for item in inference_pipelines.items]


@mcp.tool()
def retrieve_inference_pipeline(project_id: str, inference_pipeline_id: str) -> Dict:
    """Retrieve an inference pipeline by ID."""
    inference_pipeline = client.inference_pipelines.retrieve(
        inference_pipeline_id=inference_pipeline_id
    )
    return inference_pipeline.model_dump()


@mcp.tool()
def create_inference_pipeline(
    project_id: str,
    name: str,
    description: str,
) -> Dict:
    """Create a new inference pipeline in project.

    Args:
        project_id: The ID of the project to create the inference pipeline for.
        name: The name of the inference pipeline to create.
        description: The description of the inference pipeline to create.
    """
    inference_pipeline = client.projects.inference_pipelines.create(
        project_id=project_id,
        name=name,
        description=description,
    )
    return inference_pipeline.model_dump()


# ------------------------------- Test results ------------------------------- #
@mcp.tool()
def list_commit_test_results(project_version_id: str) -> List[Dict]:
    """List the test results for a commit.

    Args:
        project_version_id: The ID of the commit to list the test results for.
    """
    test_results = client.commits.test_results.list(
        project_version_id=project_version_id
    )
    return [item.model_dump() for item in test_results.items]


@mcp.tool()
def list_inference_pipeline_test_results(inference_pipeline_id: str) -> List[Dict]:
    """List the test results for an inference pipeline."""
    test_results = client.inference_pipelines.test_results.list(
        inference_pipeline_id=inference_pipeline_id
    )
    return [item.model_dump() for item in test_results.items]
