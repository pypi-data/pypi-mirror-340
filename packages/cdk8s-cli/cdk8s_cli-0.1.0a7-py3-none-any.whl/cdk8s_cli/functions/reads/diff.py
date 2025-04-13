from argparse import Namespace
from kubernetes import client
from pathlib import Path
from typing import Optional
from cdk8s import App


def _diff(
    app: App,
    name: Optional[str],
    output_dir: Path,
    k8s_client: Optional[client.ApiClient],
    args: Namespace,
):
    raise NotImplementedError("Diffing is not implemented yet")
