import gradio as gr

def practice_tab():
    with gr.Tab("Practice"):
        gr.Markdown("## 📘 Welcome to the Practice tab!")
        txt = gr.Textbox(label="Enter some text")
        out = gr.Textbox(label="Echo Output")

        def echo(x):
            return f"You typed: {x}"

        txt.submit(echo, txt, out)
    return
