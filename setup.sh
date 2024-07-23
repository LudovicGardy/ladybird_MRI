mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
[theme]\n\
base = \"dark\"\n\
layout="centered"
initial_sidebar_state="expanded"
page_title="3D Med Viewer"
sidebar_title="3D Med Viewer"
" > ~/.streamlit/config.toml