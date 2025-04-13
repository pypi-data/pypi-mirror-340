import os

IGNORED_FILES = {"_app.tsx", "_document.tsx", "__layout.tsx", "_main.tsx", "_routes.tsx", "_actions.tsx"}
IGNORED_DIRS = {"components", "lib", "utils"}


def map_page_routes(root="pages"):
    routes = []

    for dir_name, _, files in os.walk(root):
        # Skip ignored folders
        if any(ignored in dir_name.split(os.sep) for ignored in IGNORED_DIRS):
            continue

        for file in files:
            if not file.endswith((".tsx", ".jsx")):
                continue

            if file in IGNORED_FILES or file.startswith("_"):
                continue

            rel_path = os.path.relpath(os.path.join(dir_name, file), root)
            web_path = rel_path.replace(os.sep, "/")
            web_path = web_path.replace("index.tsx", "").replace(".tsx", "")
            web_path = web_path.replace("index.jsx", "").replace(".jsx", "")
            web_path = "/" + web_path.strip("/")

            # Convert dynamic segments to colon-style
            if "[[" in web_path or "[" in web_path:
                web_path = web_path.replace("[[", ":").replace("]]", "")
                web_path = web_path.replace("[", ":").replace("]", "")

            routes.append(web_path)

    return sorted(routes)
