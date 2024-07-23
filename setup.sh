mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
[theme]\n\
base = \"dark\"\n\
layout=\"centered\"\n\
initial_sidebar_state=\"expanded\"\n\
page_title=\"3D Med Viewer\"\n\
sidebar_title=\"3D Med Viewer\"\n\
" > ~/.streamlit/config.toml