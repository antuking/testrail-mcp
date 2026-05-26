"""MCP server implementation for TestRail."""
from fastmcp import FastMCP

from testrail_mcp.testrail_client import TestRailClient
from testrail_mcp.config import TESTRAIL_URL, TESTRAIL_USERNAME, TESTRAIL_API_KEY
from testrail_mcp.features import (
    projects,
    cases,
    sections,
    runs,
    results,
    datasets,
    labels,
    milestones,
    plans,
    suites,
    tests,
    attachments,
    users,
    groups,
    shared_steps,
    statuses,
    configurations,
    templates,
    priorities,
)


class TestRailMCPServer(FastMCP):
    """MCP server for TestRail integration using FastMCP."""

    def __init__(self):
        """Initialize the TestRail MCP server."""
        super().__init__(name="TestRail MCP Server", version="0.2.0")
        self.client = TestRailClient(TESTRAIL_URL, TESTRAIL_USERNAME, TESTRAIL_API_KEY)
        self._register_features()

    def _register_features(self) -> None:
        """Register all TestRail features (tools and resources) with the MCP server."""
        features = (
            projects,
            cases,
            sections,
            runs,
            results,
            datasets,
            labels,
            milestones,
            plans,
            suites,
            tests,
            attachments,
            users,
            groups,
            shared_steps,
            statuses,
            configurations,
            templates,
            priorities,
        )
        for module in features:
            if hasattr(module, "register_tools"):
                module.register_tools(self, self.client)
            if hasattr(module, "register_resources"):
                module.register_resources(self, self.client)
