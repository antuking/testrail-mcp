"""MCP server implementation for TestRail."""
from fastmcp import FastMCP

from testrail_mcp.testrail_client import TestRailClient
from testrail_mcp.config import TESTRAIL_URL, TESTRAIL_USERNAME, TESTRAIL_API_KEY, validate_config
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
        self.client = TestRailClient(
            TESTRAIL_URL or "https://placeholder",
            TESTRAIL_USERNAME or "placeholder",
            TESTRAIL_API_KEY or "placeholder"
        )
        self._register_features()

    async def run_stdio_async(self):
        """Run the server in stdio mode asynchronously, validating config first."""
        validate_config()
        await super().run_stdio_async()

    def run_stdio(self):
        """Run the server in stdio mode, validating config first."""
        validate_config()
        super().run_stdio()

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


# Create a global instance for use as an entrypoint (e.g., testrail_mcp.mcp_server:mcp)
mcp = TestRailMCPServer()
