# from langflow.field_typing import Data
from concurrent.futures import ProcessPoolExecutor
from typing import Any, Dict, List

from Helper import formpopulate

from langflow.base.flow_processing.utils import build_data_from_run_outputs
from langflow.custom import Component
from langflow.field_typing.range_spec import RangeSpec
from langflow.graph.graph.base import Graph
from langflow.helpers.flow import run_flow
from langflow.inputs.inputs import (
    DropdownInput,
    InputTypes,
    MessageInput,
)
from langflow.io import (
    BoolInput,
    CodeInput,
    DropdownInput,
    IntInput,
    LinkInput,
    MessageTextInput,
    MultilineInput,
    MultiselectInput,
    Output,
    PromptInput,
    SecretStrInput,
    SliderInput,
    StrInput,
    TabInput,
    TableInput,
)  # noqa: F401
from langflow.schema import Data, dotdict
from langflow.schema.dataframe import DataFrame
from langflow.schema.message import Message
from langflow.template import Output


class CustomComponent(Component):
    display_name = "My popup form"
    description = "Shows a custom form when clicked"
    documentation: str = "https://docs.langflow.org/components-custom-components"
    icon = "📝"
    name = "Popup"

    inputs = [
        MultilineInput(name="title", display_name="Form Title", required=True),
        DropdownInput(name="color", display_name="Favorite Color", options=["Red", "Green", "Blue"], value="Red"),
        BoolInput(name="subscribe", display_name="Subscribe to newsletter", value=False),
        MultiselectInput(
            name="interests",
            display_name="Select your interests",
            options=["Technology", "Science", "Art", "Music"],
            value=["Technology", "Science"],
        ),
        SliderInput(
            name="Int Input",
            display_name="IntInput",
            range_spec=RangeSpec(min=0, max=100, step=1),
            slider_input=True,
            slider_buttons=True,
            min_label="⬇️",
            max_label="⬆️",
            max_label_icon="⬆️",
            min_label_icon="⬇️",
        ),
    ]

    # Define the outputs of the component
    outputs = [
        Output(display_name="Output", name="output", method="build_output"),
    ]

    async def update_build_config(self, build_config: dotdict, field_value: Any, field_name: str | None = None):
        """Updates the component's config when a field value is changed (especially 'input_value').

        Args:
            build_config (dotdict): Current configuration.
            field_value (Any): New field value.
            field_name (str | None): Name of the field being updated.

        Returns:
            dotdict: Updated configuration.
        """
        return build_config

    async def build_output(self) -> Data:
        form = formpopulate.JSONFileReader().safe_read()

        text = f"Title: {self.title}, Color: {self.color}, Subscribe: {self.subscribe}, Test: {form}"
        self.status = "Form submitted"
        return Data(content=text)
