"""Deterministic BPMN renderer.

Emits a BPMN 2.0 XML sidecar from the SAME StructuredState the prose is built
from, so the diagram and the document cannot diverge. Steps become tasks,
decision points become exclusive gateways, and a linear sequence flow threads
them between a start and an end event. Importable into drawio / Camunda.

No LLM involvement — this is pure state-to-XML.
"""
from __future__ import annotations

from xml.sax.saxutils import escape

from ..state import StructuredState

_NS = (
    'xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" '
    'xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" '
    'xmlns:di="http://www.omg.org/spec/DD/20100524/DI" '
    'xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"'
)


def _id(prefix: str, i: int) -> str:
    return f"{prefix}_{i}"


def render_bpmn(state: StructuredState) -> str:
    """Return BPMN 2.0 XML for the process flow described by ``state.steps``."""
    elements: list[str] = []
    flows: list[str] = []

    start_id = "StartEvent_1"
    end_id = "EndEvent_1"
    elements.append(f'<bpmn:startEvent id="{start_id}" name="Start"/>')

    prev = start_id
    flow_n = 0
    for i, step in enumerate(state.steps, start=1):
        if step.decision_points:
            # Represent the step's first decision as an exclusive gateway.
            gw = _id("Gateway", i)
            dp = step.decision_points[0]
            elements.append(
                f'<bpmn:exclusiveGateway id="{gw}" '
                f'name="{escape(dp.condition)}"/>'
            )
            flow_n += 1
            flows.append(
                f'<bpmn:sequenceFlow id="{_id("Flow", flow_n)}" '
                f'sourceRef="{prev}" targetRef="{gw}"/>'
            )
            prev = gw
        task = _id("Task", i)
        label = f"{step.who}: {step.what}"
        elements.append(f'<bpmn:task id="{task}" name="{escape(label)}"/>')
        flow_n += 1
        flows.append(
            f'<bpmn:sequenceFlow id="{_id("Flow", flow_n)}" '
            f'sourceRef="{prev}" targetRef="{task}"/>'
        )
        prev = task

    elements.append(f'<bpmn:endEvent id="{end_id}" name="End"/>')
    flow_n += 1
    flows.append(
        f'<bpmn:sequenceFlow id="{_id("Flow", flow_n)}" '
        f'sourceRef="{prev}" targetRef="{end_id}"/>'
    )

    process_id = "Process_BPA"
    body = "\n    ".join(elements + flows)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f"<bpmn:definitions {_NS} id=\"Definitions_BPA\" "
        'targetNamespace="http://bpmn.io/schema/bpmn">\n'
        f'  <bpmn:process id="{process_id}" name="{escape(state.process_name)}" '
        'isExecutable="false">\n'
        f"    {body}\n"
        "  </bpmn:process>\n"
        "</bpmn:definitions>\n"
    )
