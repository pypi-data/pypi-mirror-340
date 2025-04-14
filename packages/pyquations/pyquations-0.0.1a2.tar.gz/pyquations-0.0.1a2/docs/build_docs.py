import os
import subprocess


def build_docs() -> None:
    # Clean Old RST Files for pyquations
    clean_cmd: list[str] = [
        "rm",
        "-rf",
        "_api/*",
    ]
    subprocess.run(clean_cmd, check=True)

    # Build RST Files for pyquations
    # TODO: Make fail on any error/warning
    sphinx_apidoc_cmd: list[str] = [
        "sphinx-apidoc",
        "-o",
        "_api",
        "../pyquations",
    ]
    subprocess.run(sphinx_apidoc_cmd, check=True)

    rename_rst_header()

    # Clean Previous Builds
    make_clean_cmd: list[str] = ["make", "clean"]
    subprocess.run(make_clean_cmd, check=True, cwd=".")

    # Create HTML Documentation
    make_html_cmd: list[str] = ["make", "html"]
    subprocess.run(make_html_cmd, check=True, cwd=".")


def rename_rst_header() -> None:
    # Rename the header of the _api/modules.rst file
    with open("_api/modules.rst", "r") as file:
        lines: list[str] = file.readlines()

    # Modify the first line
    title: str = "API Reference"
    lines[0] = f"{title}\n"
    lines[1] = "=" * len(title) + "\n"

    with open("_api/modules.rst", "w") as file:
        file.writelines(lines)


if __name__ == "__main__":
    try:
        # Change working directory to the directory of this script
        script_dir: str = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)

        build_docs()
        print("Documentation build completed successfully.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
