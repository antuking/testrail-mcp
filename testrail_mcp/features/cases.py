"""Case tools/resources registration."""
from typing import Dict, List, Any, Optional, Union
from fastmcp import FastMCP

from testrail_mcp.testrail_client import TestRailClient


def register_tools(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.tool("get_case_types", description="Get all available case types")
    def get_case_types() -> List[Dict]:
        return client.get_case_types()

    @mcp.tool("get_case_fields", description="Get all available test case custom fields")
    def get_case_fields() -> List[Dict]:
        return client.get_case_fields()

    @mcp.tool("add_case_field", description="Add a new test case custom field")
    def add_case_field(
        type: str,
        name: str,
        label: str,
        configs: List[Dict[str, Any]],
        description: Optional[str] = None,
        include_all: Optional[bool] = None,
        template_ids: Optional[List[int]] = None,
    ) -> Dict:
        data: Dict[str, Any] = {
            'type': type,
            'name': name,
            'label': label,
            'configs': configs,
        }
        if description is not None:
            data['description'] = description
        if include_all is not None:
            data['include_all'] = include_all
        if template_ids is not None:
            data['template_ids'] = template_ids
        return client.add_case_field(data)
    @mcp.tool("get_case", description="Get a test case by ID")
    def get_case(case_id: int) -> Dict:
        """Get a test case by ID."""
        return client.get_case(case_id)

    @mcp.tool("get_cases", description="Get all test cases for a project/suite")
    def get_cases(
        project_id: int,
        suite_id: Optional[int] = None,
        created_after: Optional[int] = None,
        created_before: Optional[int] = None,
        created_by: Optional[Union[int, List[int], str]] = None,
        filter: Optional[str] = None,
        limit: Optional[int] = None,
        milestone_id: Optional[Union[int, List[int], str]] = None,
        offset: Optional[int] = None,
        priority_id: Optional[Union[int, List[int], str]] = None,
        refs: Optional[str] = None,
        section_id: Optional[int] = None,
        template_id: Optional[Union[int, List[int], str]] = None,
        type_id: Optional[Union[int, List[int], str]] = None,
        updated_after: Optional[int] = None,
        updated_before: Optional[int] = None,
        updated_by: Optional[Union[int, List[int], str]] = None,
        label_id: Optional[Union[int, List[int], str]] = None,
    ) -> Dict:
        """Get all test cases for a project/suite."""
        return client.get_cases(
            project_id,
            suite_id=suite_id,
            created_after=created_after,
            created_before=created_before,
            created_by=created_by,
            filter=filter,
            limit=limit,
            milestone_id=milestone_id,
            offset=offset,
            priority_id=priority_id,
            refs=refs,
            section_id=section_id,
            template_id=template_id,
            type_id=type_id,
            updated_after=updated_after,
            updated_before=updated_before,
            updated_by=updated_by,
            label_id=label_id,
        )

    @mcp.tool("add_case", description="Add a new test case")
    def add_case(
        section_id: int,
        title: str,
        template_id: Optional[int] = None,
        type_id: Optional[int] = None,
        priority_id: Optional[int] = None,
        estimate: Optional[str] = None,
        milestone_id: Optional[int] = None,
        refs: Optional[str] = None,
        labels: Optional[List[str]] = None,
        custom_steps: Optional[str] = None,
        custom_expected: Optional[str] = None,
        custom_steps_separated: Optional[List[Dict[str, str]]] = None,
        steps_separated: Optional[List[Dict[str, str]]] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> Dict:
        data = {'title': title}
        if template_id is not None:
            data['template_id'] = template_id
        if type_id is not None:
            data['type_id'] = type_id
        if priority_id is not None:
            data['priority_id'] = priority_id
        if estimate is not None:
            data['estimate'] = estimate
        if milestone_id is not None:
            data['milestone_id'] = milestone_id
        if refs is not None:
            data['refs'] = refs
        if labels is not None:
            data['labels'] = labels
        if custom_steps_separated is not None:
            data['custom_steps_separated'] = custom_steps_separated
        if steps_separated is not None:
            data['steps_separated'] = steps_separated
        if custom_steps is not None:
            data['custom_steps'] = custom_steps
        if custom_expected is not None:
            data['custom_expected'] = custom_expected
        if custom_fields:
            data.update(custom_fields)
        return client.add_case(section_id, data)

    @mcp.tool("update_case", description="Update an existing test case")
    def update_case(
        case_id: int,
        title: Optional[str] = None,
        section_id: Optional[int] = None,
        template_id: Optional[int] = None,
        type_id: Optional[int] = None,
        priority_id: Optional[int] = None,
        estimate: Optional[str] = None,
        milestone_id: Optional[int] = None,
        refs: Optional[str] = None,
        labels: Optional[List[str]] = None,
        custom_steps: Optional[str] = None,
        custom_expected: Optional[str] = None,
        custom_steps_separated: Optional[List[Dict[str, str]]] = None,
        steps_separated: Optional[List[Dict[str, str]]] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> Dict:
        data: Dict[str, Any] = {}
        if title is not None:
            data['title'] = title
        if section_id is not None:
            data['section_id'] = section_id
        if template_id is not None:
            data['template_id'] = template_id
        if type_id is not None:
            data['type_id'] = type_id
        if priority_id is not None:
            data['priority_id'] = priority_id
        if estimate is not None:
            data['estimate'] = estimate
        if milestone_id is not None:
            data['milestone_id'] = milestone_id
        if refs is not None:
            data['refs'] = refs
        if labels is not None:
            data['labels'] = labels
        if custom_steps_separated is not None:
            data['custom_steps_separated'] = custom_steps_separated
        if steps_separated is not None:
            data['steps_separated'] = steps_separated
        if custom_steps is not None:
            data['custom_steps'] = custom_steps
        if custom_expected is not None:
            data['custom_expected'] = custom_expected
        if custom_fields:
            data.update(custom_fields)
        return client.update_case(case_id, data)

    @mcp.tool("delete_case", description="Delete a test case")
    def delete_case(case_id: int, soft: Optional[bool] = None) -> Dict:
        return client.delete_case(case_id, soft=soft)

    @mcp.tool("get_history_for_case", description="Get history for a test case")
    def get_history_for_case(
        case_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Dict]:
        return client.get_history_for_case(case_id, limit=limit, offset=offset)

    @mcp.tool("copy_cases_to_section", description="Copy cases to another section")
    def copy_cases_to_section(
        section_id: int,
        case_ids: Optional[List[int]] = None,
    ) -> Dict:
        return client.copy_cases_to_section(section_id, case_ids=case_ids)

    @mcp.tool("update_cases", description="Update multiple test cases with the same values")
    def update_cases(
        suite_id: int,
        case_ids: List[int],
        section_id: Optional[int] = None,
        title: Optional[str] = None,
        template_id: Optional[int] = None,
        type_id: Optional[int] = None,
        priority_id: Optional[int] = None,
        estimate: Optional[str] = None,
        milestone_id: Optional[int] = None,
        refs: Optional[str] = None,
        labels: Optional[List[str]] = None,
        custom_steps: Optional[str] = None,
        custom_expected: Optional[str] = None,
        custom_steps_separated: Optional[List[Dict[str, str]]] = None,
        steps_separated: Optional[List[Dict[str, str]]] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> Dict:
        data: Dict[str, Any] = {'case_ids': case_ids}
        if section_id is not None:
            data['section_id'] = section_id
        if title is not None:
            data['title'] = title
        if template_id is not None:
            data['template_id'] = template_id
        if type_id is not None:
            data['type_id'] = type_id
        if priority_id is not None:
            data['priority_id'] = priority_id
        if estimate is not None:
            data['estimate'] = estimate
        if milestone_id is not None:
            data['milestone_id'] = milestone_id
        if refs is not None:
            data['refs'] = refs
        if labels is not None:
            data['labels'] = labels
        if custom_steps_separated is not None:
            data['custom_steps_separated'] = custom_steps_separated
        if steps_separated is not None:
            data['steps_separated'] = steps_separated
        if custom_steps is not None:
            data['custom_steps'] = custom_steps
        if custom_expected is not None:
            data['custom_expected'] = custom_expected
        if custom_fields:
            data.update(custom_fields)
        return client.update_cases(suite_id, data)

    @mcp.tool("move_cases_to_section", description="Move cases to another section")
    def move_cases_to_section(
        section_id: int,
        suite_id: int,
        case_ids: List[int],
    ) -> Dict:
        return client.move_cases_to_section(section_id, suite_id, case_ids)

    @mcp.tool("delete_cases", description="Delete multiple test cases")
    def delete_cases(
        suite_id: int,
        project_id: int,
        case_ids: List[int],
        soft: Optional[bool] = None,
    ) -> Dict:
        return client.delete_cases(
            suite_id,
            project_id,
            case_ids,
            soft=soft,
        )


def register_resources(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.resource("testrail://case/{case_id}")
    def get_case_resource(case_id: int) -> Dict:
        return client.get_case(case_id)
