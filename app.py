import gradio as gr
from practice import practice_tab
from dashboard import dashboard_tab

# Fake DB
USER_DB = {"test": "1234"}

def login(username, password, state):
    if username in USER_DB and USER_DB[username] == password:
        state["logged_in"] = True
        state["user"] = username
        return gr.Tabs.update(visible=True), gr.Tab.update(visible=False), f"✅ Welcome, {username}!"
    else:
        return gr.Tabs.update(visible=False), gr.Tab.update(visible=True), "❌ Invalid login"

def signup(username, password, state):
    if username in USER_DB:
        return "⚠️ User already exists"
    USER_DB[username] = password
    return "✅ Signup successful! Please login."

def logout(state):
    state["logged_in"] = False
    state["user"] = None
    return gr.Tabs.update(visible=False), gr.Tab.update(visible=True), "You have been logged out."

def create_app():
    with gr.Blocks() as demo:
        state = gr.State({"logged_in": False, "user": None})

        # --- Login Page ---
        with gr.Tab("Login/Signup", visible=True) as login_tab:
            gr.Markdown("### 🔐 Login / Signup")
            with gr.Row():
                with gr.Column():
                    login_username = gr.Textbox(label="Username")
                    login_password = gr.Textbox(label="Password", type="password")
                    login_btn = gr.Button("Login")
                    login_status = gr.Label()

                with gr.Column():
                    signup_username = gr.Textbox(label="New Username")
                    signup_password = gr.Textbox(label="New Password", type="password")
                    signup_btn = gr.Button("Signup")
                    signup_status = gr.Label()

        # --- Home Tabs ---
        with gr.Tabs(visible=False) as home_tabs:
            practice_tab()
            dashboard_tab()
            logout_btn = gr.Button("Logout")
            home_status = gr.Label()

        # Event bindings
        login_btn.click(login, [login_username, login_password, state], [home_tabs, login_tab, login_status])
        signup_btn.click(signup, [signup_username, signup_password, state], signup_status)
        logout_btn.click(logout, [state], [home_tabs, login_tab, home_status])

    return demo
