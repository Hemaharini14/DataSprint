import gradio as gr

def dashboard_tab():
    with gr.Tab("Dashboard"):
        gr.Markdown("## 📊 Welcome to the Dashboard!")
        number = gr.Number(label="Enter a number", value=5)
        squared = gr.Number(label="Squared Value")

        def square(x):
            return x * x

        number.change(square, number, squared)
    return
