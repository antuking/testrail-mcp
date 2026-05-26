"""Composable TestRail API client."""
from testrail_mcp.client.base import BaseClient
from testrail_mcp.client.cases import CasesAPI
from testrail_mcp.client.attachments import AttachmentsAPI
from testrail_mcp.client.users import UsersAPI
from testrail_mcp.client.groups import GroupsAPI
from testrail_mcp.client.projects import ProjectsAPI
from testrail_mcp.client.runs import RunsAPI
from testrail_mcp.client.results import ResultsAPI
from testrail_mcp.client.sections import SectionsAPI
from testrail_mcp.client.datasets import DatasetsAPI
from testrail_mcp.client.labels import LabelsAPI
from testrail_mcp.client.milestones import MilestonesAPI
from testrail_mcp.client.plans import PlansAPI
from testrail_mcp.client.suites import SuitesAPI
from testrail_mcp.client.tests import TestsAPI
from testrail_mcp.client.shared_steps import SharedStepsAPI
from testrail_mcp.client.statuses import StatusesAPI
from testrail_mcp.client.configurations import ConfigurationsAPI
from testrail_mcp.client.templates import TemplatesAPI
from testrail_mcp.client.priorities import PrioritiesAPI


class TestRailClient(
    BaseClient,
    AttachmentsAPI,
    CasesAPI,
    UsersAPI,
    GroupsAPI,
    ProjectsAPI,
    RunsAPI,
    ResultsAPI,
    SectionsAPI,
    DatasetsAPI,
    LabelsAPI,
    MilestonesAPI,
    PlansAPI,
    SuitesAPI,
    TestsAPI,
    SharedStepsAPI,
    StatusesAPI,
    ConfigurationsAPI,
    TemplatesAPI,
    PrioritiesAPI,
):
    """TestRail API client composed of feature mixins."""


__all__ = ["TestRailClient"]
