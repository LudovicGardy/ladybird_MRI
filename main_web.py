import streamlit as st

from src.env_global.config.config import get_path
from src.env_web.config.config import page_config
from src.env_web.modules.home import Home
from src.env_web.modules.ui_components import (
    init_page_config,
    init_session_state,
    local_css,
)

init_page_config(page_config)  ### Must be called before any other st. function
local_css(get_path()["styles.css"])

st.markdown(
    """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    """,
    unsafe_allow_html=True,
)


### Main class for the imagery widget
class App:
    def __init__(self):
        init_session_state()
        self.run()

    def run(self):
        Home()


if __name__ == "__main__":
    app = App()
