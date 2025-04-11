import uvicorn
from pathlib import Path
import json
from rich import print
from dotenv import load_dotenv
from langgraph_api.cli import patch_environment
import typer
import threading

from davia.app.application import Davia


def run_server(
    app: Davia,
    host: str = "127.0.0.1",
    port: int = 2025,
    n_jobs_per_worker: int = 1,
    browser: bool = True,
    reload: bool = True,
):
    local_url = f"http://{host}:{port}"
    preview_url = "https://dev.davia.ai/dashboard"

    def _open_browser():
        import time
        import urllib.request

        while True:
            try:
                with urllib.request.urlopen(f"{local_url}/info") as response:
                    if response.status == 200:
                        typer.launch(preview_url)
                        return
            except urllib.error.URLError:
                pass
            time.sleep(0.1)

    if browser:
        threading.Thread(target=_open_browser, daemon=True).start()

    print(f"""
        Welcome to
▗▄▄▄   ▗▄▖ ▗▖  ▗▖▗▄▄▄▖ ▗▄▖ 
▐▌  █ ▐▌ ▐▌▐▌  ▐▌  █  ▐▌ ▐▌
▐▌  █ ▐▛▀▜▌▐▌  ▐▌  █  ▐▛▀▜▌
▐▙▄▄▀ ▐▌ ▐▌ ▝▚▞▘ ▗▄█▄▖▐▌ ▐▌

- 🎨 UI: {preview_url}
""")

    filtered_graphs = {
        name: f"{Path(graph_data['source_file']).resolve().as_posix()}:{name}"
        for name, graph_data in app.graphs.items()
    }
    tasks = app.tasks

    # Get the absolute path to launcher_graph.py
    current_file_path = Path(__file__).resolve()
    # Get the directory containing launcher_graph.py
    current_dir = current_file_path.parent
    # Get the absolute path to custom_app.py in the same directory
    custom_app_path = current_dir / "custom_app.py"

    http = {"app": f"{custom_app_path.resolve().as_posix()}:app"}

    with patch_environment(
        MIGRATIONS_PATH="__inmem",
        DATABASE_URI=":memory:",
        REDIS_URI="fake",
        N_JOBS_PER_WORKER=str(n_jobs_per_worker if n_jobs_per_worker else 1),
        LANGSERVE_GRAPHS=json.dumps(filtered_graphs) if filtered_graphs else None,
        TASKS=json.dumps(tasks) if tasks else None,
        LANGSMITH_LANGGRAPH_API_VARIANT="local_dev",
        LANGGRAPH_HTTP=json.dumps(http) if http else None,
        # See https://developer.chrome.com/blog/private-network-access-update-2024-03
        ALLOW_PRIVATE_NETWORK="true",
    ):
        load_dotenv()
        uvicorn.run(
            "langgraph_api.server:app",
            host=host,
            port=port,
            reload=reload,
            log_level="warning",
            access_log=False,
            log_config={
                "version": 1,
                "incremental": False,
                "disable_existing_loggers": False,
                "formatters": {
                    "simple": {
                        "class": "langgraph_api.logging.Formatter",
                    }
                },
                "handlers": {
                    "console": {
                        "class": "logging.StreamHandler",
                        "formatter": "simple",
                        "stream": "ext://sys.stdout",
                    }
                },
                "root": {"handlers": ["console"]},
            },
        )
