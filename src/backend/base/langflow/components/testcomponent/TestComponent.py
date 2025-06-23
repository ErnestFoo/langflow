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
    CustomInput
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
    
    form_cache: Dict[str, Any] | None = formpopulate.JSONFileReader().safe_read()

    inputs = [
        MultilineInput(name="title", display_name="Form Title", required=True),
        DropdownInput(
            name="form",
            display_name="Form to display",
            options=form_cache.keys(),
            value= "",
            real_time_refresh=True,
            advanced=True
        ),
        CustomInput(
            name="banana",
            display_name="Modal to Display",
            value="",
            modal="",
            real_time_refresh=True
            ),
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
        print(field_name+ " " + field_value)
        if field_name == "form":
            
            # Get the selected color
            selected_form = field_value

            # Lookup the corresponding value from the form_cache
            modal_content = self.form_cache.get(selected_form, "")
            print("modal_content: "+ modal_content)

            # Update the CustomInput modal value
            build_config["banana"]["modal"] = modal_content
            print("Modal content changed")
                
        return build_config

    async def build_output(self) -> Data:
        modal_content = self.form_cache.get(self.color, "")
        text = f"Title: {self.title}, Color: {self.color}, Subscribe: {self.subscribe}, Selected: {self.form_cache.get(self.color)}, Modal: {self.banana}"
        self.status = f"Modal preview: {modal_content}"
        return Data(content=text)
