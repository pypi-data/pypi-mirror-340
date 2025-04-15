
import gradio as gr
from app import demo as app
import os

_docs = {'SourceSelector': {'description': 'Creates a dropdown of choices from which a single entry or multiple entries can be selected (as an input component) or displayed (as an output component).\n', 'members': {'__init__': {'choices': {'type': 'Sequence[\n        str | int | float | tuple[str, str | int | float]\n    ]\n    | None', 'default': 'None', 'description': 'A list of string options to choose from. An option can also be a tuple of the form (name, value), where name is the displayed name of the dropdown choice and value is the value to be passed to the function, or returned by the function.'}, 'value': {'type': 'str\n    | int\n    | float\n    | Sequence[str | int | float]\n    | Callable\n    | None', 'default': 'None', 'description': 'default value(s) selected in dropdown. If None, no value is selected by default. If callable, the function will be called whenever the app loads to set the initial value of the component.'}, 'type': {'type': 'Literal["value", "index"]', 'default': '"value"', 'description': 'Type of value to be returned by component. "value" returns the string of the choice selected, "index" returns the index of the choice selected.'}, 'allow_custom_value': {'type': 'bool', 'default': 'False', 'description': 'If True, allows user to enter a custom value that is not in the list of choices.'}, 'max_choices': {'type': 'int | None', 'default': 'None', 'description': 'maximum number of choices that can be selected. If None, no limit is enforced.'}, 'filterable': {'type': 'bool', 'default': 'True', 'description': 'If True, user will be able to type into the dropdown and filter the choices by typing. Can only be set to False if `allow_custom_value` is False.'}, 'label': {'type': 'str | None', 'default': 'None', 'description': 'The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.'}, 'info': {'type': 'str | None', 'default': 'None', 'description': 'additional component description.'}, 'every': {'type': 'Timer | float | None', 'default': 'None', 'description': 'Continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.'}, 'inputs': {'type': 'Component | Sequence[Component] | set[Component] | None', 'default': 'None', 'description': 'Components that are used as inputs to calculate `value` if `value` is a function (has no effect otherwise). `value` is recalculated any time the inputs change.'}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display label.'}, 'container': {'type': 'bool', 'default': 'True', 'description': 'If True, will place the component in a container - providing some extra padding around the border.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.'}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': 'if True, choices in this dropdown will be selectable; if False, selection will be disabled. If not provided, this is inferred based on whether the component is used as an input or output.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}, 'key': {'type': 'int | str | None', 'default': 'None', 'description': None}}, 'postprocess': {'value': {'type': 'str | int | float | list[str | int | float] | None', 'description': 'Expects a `str | int | float` corresponding to the value of the dropdown entry to be selected. Or, if `multiselect` is True, expects a `list` of values corresponding to the selected dropdown entries.'}}, 'preprocess': {'return': {'type': 'str\n    | int\n    | float\n    | list[str | int | float]\n    | list[int | None]\n    | None', 'description': 'Passes the value of the selected dropdown choice as a `str | int | float` or its index as an `int` into the function, depending on `type`. Or, if `multiselect` is True, passes the values of the selected dropdown choices as a list of correspoding values/indices instead.'}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the SourceSelector changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'input': {'type': None, 'default': None, 'description': 'This listener is triggered when the user changes the value of the SourceSelector.'}, 'select': {'type': None, 'default': None, 'description': 'Event listener for when the user selects or deselects the SourceSelector. Uses event data gradio.SelectData to carry `value` referring to the label of the SourceSelector, and `selected` to refer to state of the SourceSelector. See EventData documentation on how to use this event data'}, 'focus': {'type': None, 'default': None, 'description': 'This listener is triggered when the SourceSelector is focused.'}, 'blur': {'type': None, 'default': None, 'description': 'This listener is triggered when the SourceSelector is unfocused/blurred.'}, 'key_up': {'type': None, 'default': None, 'description': 'This listener is triggered when the user presses a key while the SourceSelector is focused.'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'SourceSelector': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_sourceselector`

<div style="display: flex; gap: 7px;">
<a href="https://pypi.org/project/gradio_sourceselector/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_sourceselector"></a>  
</div>

Python library for easily interacting with trained machine learning models
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_sourceselector
```

## Usage

```python

import gradio as gr
from gradio_sourceselector import SourceSelector

demo = gr.Interface(
    lambda x: x,
    SourceSelector(choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    gr.Text(),
)

if __name__ == "__main__":
    demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `SourceSelector`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["SourceSelector"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["SourceSelector"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, passes the value of the selected dropdown choice as a `str | int | float` or its index as an `int` into the function, depending on `type`. Or, if `multiselect` is True, passes the values of the selected dropdown choices as a list of correspoding values/indices instead.
- **As output:** Should return, expects a `str | int | float` corresponding to the value of the dropdown entry to be selected. Or, if `multiselect` is True, expects a `list` of values corresponding to the selected dropdown entries.

 ```python
def predict(
    value: str
    | int
    | float
    | list[str | int | float]
    | list[int | None]
    | None
) -> str | int | float | list[str | int | float] | None:
    return value
```
""", elem_classes=["md-custom", "SourceSelector-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          SourceSelector: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
