extensions: list = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_multiversion",
]

# Show the latest version by default
smv_latest_version: str = "main"
smv_tag_whitelist: str = r"^v\d+\.\d+.*$"
smv_branch_whitelist: str = r"^main$"
