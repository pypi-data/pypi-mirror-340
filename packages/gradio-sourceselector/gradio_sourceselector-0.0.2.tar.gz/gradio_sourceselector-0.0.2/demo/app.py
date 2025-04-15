
import gradio as gr
from gradio_sourceselector import SourceSelector

demo = gr.Interface(
    lambda x: x,
    SourceSelector(choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    gr.Text(),
)

if __name__ == "__main__":
    demo.launch()
