import json
import os
from pathlib import Path
from pandas.core.frame import DataFrame
from task.scripts.normalize_nodes import normalize_nodes
from task.scripts.download_network_graph import download_network_graph


class TaskResult:
    
    def __init__(self, result: dict) -> None:
        self.full_results = result
        self.parameters = result["parameters"]
        self.nodes = normalize_nodes(result, self.parameters)
        self.path_to_download_folder = str(Path.home() / "Downloads/")

    def to_dict(self) -> dict:
        """Returns a dict with the result."""
        return self.nodes

    def get_parameters(self) -> dict:
        """Returns a dict with the parameters of the task."""
        return self.parameters

    def get_full_results(self) -> dict:
        """Returns the unfiltered results, as they come from the server."""
        return self.full_results

    def to_json(self):
        """Downloads a json file with the results to the users downloads folder."""

        downloads_path = str(Path.home() / "Downloads/result.json")
        path_exists = os.path.exists(downloads_path)
        iterations = 1
        while path_exists:
            if not downloads_path.endswith(").json"):
                downloads_path = downloads_path[:len(downloads_path)-5] + "(1).json"
            else:
                downloads_path = downloads_path[:len(downloads_path)-7] + str(iterations) + ").json"
                iterations = iterations + 1
            path_exists = os.path.exists(downloads_path)

        with open(downloads_path, "x") as f:
            json.dump(self.nodes, f, indent=4)

    def to_pandas_dataframe(self) -> DataFrame:
        return DataFrame(self.nodes).T

    def proteins_to_csv(self) -> None:
        downloads_path = str(Path.home() / "Downloads/proteins.csv")
        data = {}
        for name, detail in self.nodes.items():
            if detail["node_type"] == "protein":
                data[name] = detail
        df = DataFrame(data).T
        df.to_csv(downloads_path)

    def drugs_to_csv(self) -> None:
        downloads_path = str(Path.home() / "Downloads/drugs.csv")
        data = {}
        for name, detail in self.nodes.items():
            if detail["node_type"] == "drug":
                data[name] = detail
        df = DataFrame(data).T
        df.to_csv(downloads_path)

    def edges_to_csv(self) -> None:
        # downloads_path = self.path_to_download_folder + "edges.xlsx"
        downloads_path = str(Path.home() / "Downloads/edges.csv")

        edges = []
        for n in [*self.nodes]:
            for e in self.nodes[n]["edges"]:
                edges.append([e["from"], e["to"]])

        data = {}
        for n in [*self.nodes]:
            data[n] = {}
            for e in [*self.nodes]:
                data[n][e] = 1 if [n, e] in edges or [e, n] in edges else 0

        df = DataFrame(data)
        df.to_csv(downloads_path)

    def to_graph(self) -> None:
        """Downloads a graph of the nodes in a html file."""
        download_network_graph(self.nodes)
