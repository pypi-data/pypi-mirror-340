#!/usr/bin/env python3

import argparse
import json
import logging
import math
import subprocess
import sys
from dataclasses import dataclass, field
from io import StringIO
from typing import Dict, List, Optional


# Configure logging to display only messages
class SimpleFormatter(logging.Formatter):
    def format(self, record):
        return record.getMessage()


logger = logging.getLogger("node-drain-analyzer")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(SimpleFormatter())
logger.addHandler(handler)


@dataclass
class Taint:
    """Represents Kubernetes node taint"""

    key: str
    value: Optional[str] = None
    effect: str = "NoSchedule"

    def __str__(self) -> str:
        return f"{self.key}={self.value}:{self.effect}" if self.value else f"{self.key}:{self.effect}"


@dataclass
class TaintList:
    """Represents a list of Kubernetes node taints"""

    items: List[Taint] = field(default_factory=list)

    def add_taint(self, taint: Taint):
        self.items.append(taint)

    def remove_taint(self, taint: Taint):
        self.items.remove(taint)

    def __str__(self) -> str:
        return ", ".join(str(taint) for taint in self.items)

    def __len__(self) -> int:
        return len(self.items)


@dataclass
class Toleration:
    """Represents Pod toleration"""

    key: str
    operator: str = "Equal"  # 'Exists' or 'Equal'
    value: Optional[str] = None
    effect: Optional[str] = None
    toleration_seconds: Optional[int] = None

    def __str__(self) -> str:
        return f"{self.key}={self.value}:{self.effect}" if self.value else f"{self.key}:{self.effect}"


@dataclass
class TolerationList:
    """Represents a list of Pod tolerations"""

    items: List[Toleration] = field(default_factory=list)

    def add_toleration(self, toleration: Toleration):
        self.items.append(toleration)

    def remove_toleration(self, toleration: Toleration):
        self.items.remove(toleration)

    def __str__(self) -> str:
        return ", ".join(str(toleration) for toleration in self.items)

    def __len__(self) -> int:
        return len(self.items)


def toleration_matches_taint(toleration: Toleration, taint: Taint) -> bool:
    """Check if toleration matches taint"""
    # Special case 1: If toleration.key is empty and operator is Exists, it matches all keys
    if toleration.key == "" and toleration.operator == "Exists":
        # But effect still needs to match
        return toleration.effect == taint.effect or toleration.effect == ""

    # General case: key must match
    if toleration.key != taint.key:
        return False

    # Special case 2: If effect is empty, it matches all effects with the same key
    if toleration.effect == "":
        # Only check operator and value
        pass
    # General case: effect needs to match
    elif toleration.effect != taint.effect:
        return False

    # Check operator and value
    if toleration.operator == "Exists":
        # Exists operator does not care about value
        return True
    elif toleration.operator == "Equal":
        # Equal operator requires value to match
        return toleration.value == taint.value

    # Default case does not match
    return False


def pod_tolerates_node_taints(tolerations: List[Toleration], taints: List[Taint]) -> bool:
    """Check if Pod tolerations allow it to be scheduled to a node with taints"""
    if not taints:
        return True

    for taint in taints:
        if not any(toleration_matches_taint(toleration, taint) for toleration in tolerations):
            return False

    return True


@dataclass
class Resource:
    cpu: int
    memory: int

    def __add__(self, other: "Resource") -> "Resource":
        return Resource(self.cpu + other.cpu, self.memory + other.memory)

    def __sub__(self, other: "Resource") -> "Resource":
        return Resource(self.cpu - other.cpu, self.memory - other.memory)

    def __str__(self) -> str:
        return f"CPU: {self.cpu}m, Memory: {math.ceil(self.memory)}Mi"


@dataclass
class Pod:
    namespace: str
    name: str
    requests: Resource
    limits: Resource
    metrics: Resource
    priority: Optional[int] = None
    node: Optional[str] = None
    tolerations: TolerationList = field(default_factory=TolerationList)
    controller_type: Optional[str] = None
    node_selector: Dict[str, str] = field(default_factory=dict)
    affinity: Optional[str] = None
    anti_affinity: Optional[str] = None
    status: Optional[str] = None

    def row(self, headers: List[str]) -> List[str]:
        """Return a row of data for the Pod"""
        row: List[str] = []
        for header in headers:
            if header == "Namespace":
                row.append(self.namespace)
            elif header == "Name":
                row.append(self.name)
            elif header == "Node":
                row.append(self.node or "")
            elif header == "CPU":
                row.append(f"{self.metrics.cpu}m")
            elif header == "Memory":
                row.append(f"{math.ceil(self.metrics.memory)}Mi")
            elif header == "RequestCPU":
                row.append(f"{self.requests.cpu}m")
            elif header == "RequestMemory":
                row.append(f"{math.ceil(self.requests.memory)}Mi")
            elif header == "LimitCPU":
                row.append(f"{self.limits.cpu}m")
            elif header == "LimitMemory":
                row.append(f"{math.ceil(self.limits.memory)}Mi")
            elif header == "ControlledBy":
                row.append(self.controller_type or "")
            elif header == "Priority":
                row.append(str(self.priority) if self.priority else "")
            elif header == "Tolerations":
                row.append(f"{len(self.tolerations)}")
            else:
                row.append("")
        return row


@dataclass
class PodList:
    items: List[Pod] = field(default_factory=list)
    requests: Resource = field(default_factory=lambda: Resource(0, 0))
    limits: Resource = field(default_factory=lambda: Resource(0, 0))
    metrics: Resource = field(default_factory=lambda: Resource(0, 0))

    def add_pod(self, pod: Pod):
        self.items.append(pod)
        self.requests += pod.requests
        self.limits += pod.limits
        self.metrics += pod.metrics

    def remove_pod(self, pod: Pod):
        self.items.remove(pod)
        self.requests -= pod.requests
        self.limits -= pod.limits
        self.metrics -= pod.metrics

    def get_pods_by_namespace(self, namespace: str) -> "PodList":
        pods_in_namespace = PodList()
        for pod in self.items:
            if pod.namespace == namespace:
                pods_in_namespace.add_pod(pod)
        return pods_in_namespace

    def get_pods_by_node(self, node: str) -> "PodList":
        pods_on_node = PodList()
        for pod in self.items:
            if pod.node == node:
                pods_on_node.add_pod(pod)
        return pods_on_node

    def __len__(self) -> int:
        return len(self.items)

    def __add__(self, other: "PodList") -> "PodList":
        combined = PodList()
        combined.items = self.items + other.items
        combined.requests = self.requests + other.requests
        combined.limits = self.limits + other.limits
        combined.metrics = self.metrics + other.metrics
        return combined

    def __sub__(self, other: "PodList") -> "PodList":
        combined = PodList()
        combined.items = [pod for pod in self.items if pod not in other.items]
        combined.requests = self.requests - other.requests
        combined.limits = self.limits - other.limits
        combined.metrics = self.metrics - other.metrics
        return combined


@dataclass
class Image:
    names: List[str]
    sizeBytes: int

    def __str__(self) -> str:
        return f"{', '.join(self.names) if self.names else '-'}, Size: {self.sizeBytes} bytes"


@dataclass
class ImageList:
    items: List[Image] = field(default_factory=list)

    def add_image(self, image: Image):
        self.items.append(image)

    def remove_image(self, image: Image):
        self.items.remove(image)

    def size(self) -> int:
        return sum(image.sizeBytes for image in self.items)

    def __len__(self) -> int:
        return len(self.items)

    def __str__(self) -> str:
        return "\n".join(str(image) for image in self.items)


@dataclass
class NodeResource:
    cpu: int
    ephemeralStorage: int
    memory: int
    pods: int

    def __add__(self, other: "NodeResource") -> "NodeResource":
        return NodeResource(
            self.cpu + other.cpu,
            self.ephemeralStorage + other.ephemeralStorage,
            self.memory + other.memory,
            self.pods + other.pods,
        )

    def __sub__(self, other: "NodeResource") -> "NodeResource":
        return NodeResource(
            self.cpu - other.cpu,
            self.ephemeralStorage - other.ephemeralStorage,
            self.memory - other.memory,
            self.pods - other.pods,
        )

    def __str__(self) -> str:
        return f"CPU: {self.cpu}m, Ephemeral Storage: {self.ephemeralStorage}Mi, Memory: {math.ceil(self.memory)}Mi, Pods: {self.pods}"


@dataclass
class Node:
    name: str
    architecture: str
    operatingSystem: str
    allocatable: NodeResource
    capacity: NodeResource
    labels: Dict[str, str] = field(default_factory=dict)
    annotations: Dict[str, str] = field(default_factory=dict)
    taints: TaintList = field(default_factory=TaintList)
    images: ImageList = field(default_factory=ImageList)
    podList: PodList = field(default_factory=PodList)
    metrics: Resource = field(default_factory=lambda: Resource(0, 0))

    def row(self, headers: List[str]) -> List[str]:
        """Return a row of data for the Node"""
        row: List[str] = []
        for header in headers:
            if header == "Node":
                row.append(self.name)
            elif header == "CPU":
                row.append(f"{self.metrics.cpu}m")
            elif header == "Memory":
                row.append(f"{math.ceil(self.metrics.memory)}Mi")
            elif header == "Pods":
                row.append(str(len(self.podList.items)))
            elif header == "AllocatableCPU":
                row.append(f"{self.allocatable.cpu}m")
            elif header == "AllocatableMemory":
                row.append(f"{math.ceil(self.allocatable.memory)}Mi")
            elif header == "AllocatablePods":
                row.append(str(self.allocatable.pods))
            elif header == "Taints":
                row.append(f"{len(self.taints)}")
            elif header == "Images":
                row.append(f"{len(self.images.items)}")
            elif header == "Architecture":
                row.append(self.architecture)
            elif header == "OperatingSystem":
                row.append(self.operatingSystem)
            elif header == "Metrics":
                row.append(f"CPU: {self.metrics.cpu}m, Memory: {math.ceil(self.metrics.memory)}Mi")
            else:
                row.append("")
        return row


@dataclass
class NodeList:
    items: List[Node] = field(default_factory=list)
    allocatable: NodeResource = field(default_factory=lambda: NodeResource(0, 0, 0, 0))
    capacity: NodeResource = field(default_factory=lambda: NodeResource(0, 0, 0, 0))
    podList: PodList = field(default_factory=PodList)

    def add_node(self, node: Node):
        self.items.append(node)
        self.allocatable += node.allocatable
        self.capacity += node.capacity
        self.podList += node.podList

    def remove_node(self, name: str) -> Optional[Node]:
        node = next((n for n in self.items if n.name == name), None)
        if node:
            self.items.remove(node)
            self.allocatable -= node.allocatable
            self.capacity -= node.capacity
            self.podList -= node.podList
            return node
        return None

    def __len__(self) -> int:
        return len(self.items)


def node_selector_matches(node_selector: dict, node: Node) -> bool:
    """Check if node selector matches node labels"""
    for key, value in node_selector.items():
        if key not in node.labels or node.labels[key] != value:
            return False
    return True


def node_selector_matches_node_list(node_selector: dict, node_list: NodeList) -> bool:
    """Check if node selector matches any node in the node list"""
    for node in node_list.items:
        if node_selector_matches(node_selector, node):
            return True
    return False


KUBECTL = "kubectl"


def kubectl(args: List[str], exit_on_error: bool = True) -> str:
    """Run kubectl command and return output"""
    command = [KUBECTL] + args
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing command: {e}")
        if exit_on_error:
            sys.exit(1)
        raise e


def parse_cpu(cpu_str: str) -> int:
    """
    Parse CPU resource value and convert it to an integer in millicores

    Examples:
    - "100m" -> 100
    - "0.1" -> 100
    - "1" -> 1000
    """
    if not cpu_str:
        return 0

    if isinstance(cpu_str, int):
        return cpu_str

    cpu_str = str(cpu_str)

    if cpu_str.endswith("m"):
        return int(cpu_str[:-1])
    else:
        # If in decimal form, convert to millicores
        try:
            return int(float(cpu_str) * 1000)
        except ValueError:
            logger.error(f"Unable to parse CPU value: {cpu_str}")
            return 0


def parse_storage(memory_str: str) -> int:
    """
    Parse memory resource value and convert it to an integer in MiB

    Examples:
    - "100Mi" -> 100
    - "1Gi" -> 1024
    - "1G" -> 953  (1000MB)
    - "1000Ki" -> 1
    """
    if not memory_str:
        return 0

    if isinstance(memory_str, int):
        return memory_str

    memory_str = str(memory_str)

    # Define unit conversions
    units = {
        "Ki": 1 / 1024,  # KiB to MiB
        "Mi": 1,  # MiB to MiB
        "Gi": 1024,  # GiB to MiB
        "Ti": 1024 * 1024,  # TiB to MiB
        "K": 1 / 1000,  # KB to MB, then convert to MiB
        "M": 1,  # MB to MiB (approximately)
        "G": 1000,  # GB to MiB (approximately)
        "T": 1000 * 1000,  # TB to MiB (approximately)
    }

    # Try parsing different unit formats
    for unit, multiplier in units.items():
        if memory_str.endswith(unit):
            try:
                value = float(memory_str[: -len(unit)])
                return int(value * multiplier)
            except ValueError:
                continue

    # If no unit, assume bytes
    try:
        return int(int(memory_str) / (1024 * 1024))  # Convert to MiB
    except ValueError:
        logger.error(f"Unable to parse memory value: {memory_str}")
        return 0


def collect_pod_list() -> PodList:
    """Collect information for all Pods"""

    # collect all pods metrics first, store it into a Dict, use the namespace/name as key, Resource as value
    top_pods_metrics = {}
    try:
        top_pods_output = kubectl(["top", "pods", "-A", "--no-headers"], exit_on_error=False)
        top_pods_lines = top_pods_output.splitlines()
        for line in top_pods_lines:
            parts = line.split()
            namespace = parts[0]
            name = parts[1]
            cpu = parse_cpu(parts[2])
            memory = parse_storage(parts[3])
            top_pods_metrics[f"{namespace}/{name}"] = Resource(cpu=cpu, memory=memory)
    except Exception:
        top_pods_metrics = {}

    # collect all pods info
    pod_list = PodList()
    output = kubectl(["get", "pods", "-A", "-o", "json"])
    pods = json.loads(output)["items"]

    for pod in pods:
        namespace = pod["metadata"]["namespace"]
        name = pod["metadata"]["name"]
        node_name = pod["spec"].get("nodeName")
        tolerations = TolerationList(
            items=[
                Toleration(
                    key=t.get("key"),
                    operator=t.get("operator", "Equal"),
                    value=t.get("value"),
                    effect=t.get("effect"),
                    toleration_seconds=t.get("tolerationSeconds"),
                )
                for t in pod["spec"].get("tolerations", [])
            ]
        )
        requests = Resource(0, 0)
        limits = Resource(0, 0)
        containers = pod["spec"].get("containers", [])
        for container in containers:
            requests += Resource(
                cpu=parse_cpu(container["resources"].get("requests", {}).get("cpu", 0)),
                memory=parse_storage(container["resources"].get("requests", {}).get("memory", 0)),
            )
            limits += Resource(
                cpu=parse_cpu(container["resources"].get("limits", {}).get("cpu", 0)),
                memory=parse_storage(container["resources"].get("limits", {}).get("memory", 0)),
            )

        # Get Pod metrics
        metrics = top_pods_metrics.get(f"{namespace}/{name}", Resource(0, 0))

        pod_list.add_pod(
            Pod(
                namespace=namespace,
                name=name,
                requests=requests,
                limits=limits,
                metrics=metrics,
                node=node_name,
                tolerations=tolerations,
                priority=pod["spec"].get("priority"),
                controller_type=pod["metadata"].get("ownerReferences", [{}])[0].get("kind"),
                node_selector=pod["spec"].get("nodeSelector"),
                affinity=pod["spec"].get("affinity"),
                anti_affinity=pod["spec"].get("antiAffinity"),
                status=pod["status"].get("phase"),
            )
        )

    return pod_list


def collect_node_list() -> NodeList:
    """Collect information for all nodes"""
    # collect all nodes metrics first, store it into a Dict, use the node name as key, Resource as value
    top_nodes_metrics = {}
    try:
        top_nodes_output = kubectl(["top", "nodes", "--no-headers"], exit_on_error=False)
        top_nodes_lines = top_nodes_output.splitlines()
        for line in top_nodes_lines:
            parts = line.split()
            name = parts[0]
            cpu = parse_cpu(parts[1])
            memory = parse_storage(parts[3])
            top_nodes_metrics[name] = Resource(cpu=cpu, memory=memory)
    except Exception:
        top_nodes_metrics = {}

    # collect all pods info
    pod_list = collect_pod_list()

    # collect all nodes info
    node_list = NodeList()
    output = kubectl(["get", "nodes", "-o", "json"])
    nodes = json.loads(output)["items"]

    for node in nodes:
        name = node["metadata"]["name"]
        architecture = node["status"]["nodeInfo"]["architecture"]
        operating_system = node["status"]["nodeInfo"]["operatingSystem"]
        allocatable = NodeResource(
            cpu=int(node["status"]["allocatable"].get("cpu", 0)) * 1000,  # Convert to millicores
            ephemeralStorage=int(parse_storage(node["status"]["allocatable"].get("ephemeral-storage", 0))),
            memory=int(parse_storage(node["status"]["allocatable"].get("memory", 0))),
            pods=int(node["status"]["allocatable"].get("pods", 0)),
        )
        capacity = NodeResource(
            cpu=int(node["status"]["capacity"].get("cpu", 0)) * 1000,  # Convert to millicores
            ephemeralStorage=int(parse_storage(node["status"]["capacity"].get("ephemeral-storage", 0))),
            memory=int(parse_storage(node["status"]["capacity"].get("memory", 0))),
            pods=int(node["status"]["capacity"].get("pods", 0)),
        )
        taints = TaintList(
            items=[
                Taint(
                    key=t["key"],
                    value=t.get("value"),
                    effect=t.get("effect"),
                )
                for t in node["spec"].get("taints", [])
            ]
        )

        image_list = ImageList()
        for image in node["status"].get("images", []):
            names = image.get("names", [])
            size_bytes = image.get("sizeBytes", 0)
            image_list.add_image(Image(names=names, sizeBytes=size_bytes))

        node_list.add_node(
            Node(
                name=name,
                architecture=architecture,
                operatingSystem=operating_system,
                allocatable=allocatable,
                capacity=capacity,
                taints=taints,
                images=image_list,
                podList=pod_list.get_pods_by_node(name),
                metrics=top_nodes_metrics.get(name, Resource(0, 0)),
                labels=node["metadata"].get("labels", {}),
                annotations=node["metadata"].get("annotations", {}),
            )
        )

    return node_list


@dataclass
class Table:
    """Represents a table of data"""

    headers: List[str]
    rows: List[List[str]] = field(default_factory=list)

    def add_row(self, row: List[str]):
        self.rows.append(row)

    def __str__(self) -> str:
        max_lengths = [max(len(str(item)) for item in col) for col in zip(*([self.headers] + self.rows))]
        header_row = " | ".join(f"{header:<{max_length}}" for header, max_length in zip(self.headers, max_lengths))
        separator_row = "-+-".join("-" * max_length for max_length in max_lengths)
        data_rows = "\n".join(
            " | ".join(f"{item:<{max_length}}" for item, max_length in zip(row, max_lengths)) for row in self.rows
        )
        return f"{header_row}\n{separator_row}\n{data_rows}"

    def print_table(self, format: str = "table"):
        """Print the table to the specified format"""
        if format == "table":
            logger.info(str(self))
        elif format == "json":
            logger.info(json.dumps({"headers": self.headers, "rows": self.rows}, indent=4))
        elif format == "csv":
            import csv

            io = StringIO()
            writer = csv.writer(io)
            writer.writerow(self.headers)
            writer.writerows(self.rows)
            logger.info(io.getvalue())
        else:
            logger.error(f"Unknown output format: {format}")


NODE_HEADERS = ["Node", "CPU", "Memory", "Pods", "AllocatableCPU", "AllocatableMemory", "AllocatablePods"]

NODE_HEADERS_WIDE = NODE_HEADERS + [
    "Taints",
    "Images",
    "Architecture",
    "OperatingSystem",
    "Metrics",
]

POD_HEADERS = [
    "Namespace",
    "Name",
    "Node",
    "CPU",
    "Memory",
    "RequestCPU",
    "RequestMemory",
    "LimitCPU",
    "LimitMemory",
]

POD_HEADERS_WIDE = POD_HEADERS + [
    "ControlledBy",
    "Priority",
    "Tolerations",
]


def parse_args() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Kubernetes Node Drain Calculator")
    parser.add_argument(
        "--wide",
        default=False,
        action="store_true",
        help="Show wide output with additional columns",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="stdout",
        help="Output destination (default: stdout)",
    )
    parser.add_argument(
        "nodes",
        nargs="*",
        help="Node name to analyze",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        default=False,
        action="store_true",
        help="Enable verbose output",
    )
    parser.add_argument(
        "--images",
        default=False,
        action="store_true",
        help="Show images information",
    )
    parser.add_argument(
        "--pods",
        default=False,
        action="store_true",
        help="Show pods information",
    )
    parser.add_argument(
        "--taints",
        default=False,
        action="store_true",
        help="Show taints information",
    )
    parser.add_argument(
        "--metrics",
        default=False,
        action="store_true",
        help="Show metrics information",
    )
    parser.add_argument(
        "--factor",
        type=float,
        default=1.5,
        help="The factor for resource calculations (default: 1.5)",
    )
    return parser.parse_args()


def print_node_list(
    node_list: NodeList,
    format: str,
    wide: bool,
):
    """Print the NodeList to the specified format"""
    headers = NODE_HEADERS_WIDE if wide else NODE_HEADERS
    table = Table(headers=headers)
    for node in node_list.items:
        table.add_row(node.row(headers))
    table.print_table(format)


def print_pod_list(
    pod_list: PodList,
    format: str,
    wide: bool,
):
    """Print the PodList to the specified format"""
    headers = POD_HEADERS_WIDE if wide else POD_HEADERS
    table = Table(headers=headers)
    for pod in pod_list.items:
        table.add_row(pod.row(headers))
    table.print_table(format)


@dataclass
class AnalysisResult:
    """Represents the result of an analysis"""

    message: str
    severity: str = "low"  # none, low, medium, high

    def __str__(self) -> str:
        return f"{self.severity}:\t{self.message}"


@dataclass
class Reporter:
    """Represents a reporter for analysis results"""

    results: List[AnalysisResult] = field(default_factory=list)

    def add_result(self, result: AnalysisResult):
        self.results.append(result)

    def print_report(self):
        """Print the analysis report"""
        if not self.results:
            logger.info("No issues found")
            return

        logger.info("Analysis Report:")
        for result in self.results:
            logger.info("\t" + str(result))

        logger.info("")
        logger.info("Summary:")
        severity_count = {"none": 0, "low": 0, "medium": 0, "high": 0}
        for result in self.results:
            severity_count[result.severity] += 1

        for severity, count in severity_count.items():
            logger.info(f"\t{severity.capitalize()}:\t{count} issue(s)")

        logger.info("")
        logger.info("Conclusions:")
        conclusion = ""
        if severity_count["high"] > 0:
            conclusion = "🚫 High severity issues found. Please review the report carefully."
        elif severity_count["medium"] > 0:
            conclusion = "❗️ Medium severity issues found. Please review the report."
        elif severity_count["low"] > 0:
            conclusion = "⚠️ Low severity issues found. Please review the report."
        else:
            conclusion = "✅ No issues found. All nodes are safe to drain."
        logger.info("\t" + conclusion)


def group_pods_by_namespace(pod_list: List[Pod]) -> str:
    """Group pods by their namespace and return a formatted string"""
    namespace_dict = {}
    for pod in pod_list:
        namespace = pod.namespace
        if namespace not in namespace_dict:
            namespace_dict[namespace] = []
        namespace_dict[namespace].append(pod.name)

    grouped_info = []
    for namespace, pods in namespace_dict.items():
        grouped_info.append(f"{namespace} ({', '.join(pods)})")

    return ", ".join(grouped_info)


def analyze(node_list: NodeList, nodes: List[str], factor: float = 1.5):
    """Analyze the node list with a scale factor"""
    drain_node_list = NodeList()
    for name in nodes:
        node = node_list.remove_node(name)
        if node is None:
            logger.error(f"Node {name} not found")
            continue
        drain_node_list.add_node(node)

    if len(drain_node_list) == 0:
        logger.info("❓ No nodes to drain")
        return

    if len(node_list) == 0:
        logger.info("⚠️ No remaining nodes")
        return

    logger.info("Remaining nodes:")
    print_node_list(node_list, "table", True)
    logger.info("")

    logger.info("Drain node details:")
    print_node_list(drain_node_list, "table", True)
    logger.info("")

    # Calculate the risk of draining the nodes, the following points are considered:
    # 1. the pod controlled by daemonsets should be ignored.
    # 2. the pod controlled by jobs/cronjobs and is running, we should notify the user waiting for the job to finish.
    #    if the job is not running, we can ignore it.
    # 3. the pod has no controller, we should notify the user to check it.
    # 4. the pod has defined the node selector and the selected node is not in the remaining nodes, we should notify the user.
    # 5. the pod has node/pod affinity/anti-affinity, we should notify the user to check it.
    # 6. the remaining nodes have taints, but some pods have no tolerations, we should notify the user.
    # 7. the remaining nodes have insufficient resources, we should notify the user.
    # 8. the remaining nodes have mismatched architecture/operating system, we should notify the user.
    # 9. the remaining nodes have insufficient allocatable pods, we should notify the user.
    #
    # According to the above points, we can calculate the risk of draining the nodes.
    # Core points:
    # 1. controller type
    # 2. node selector
    # 3. affinity and anti-affinity
    # 4. taints and tolerations
    # 5. resources
    # 6. architecture and operating system

    reporter = Reporter()

    # Check for pods controlled by daemonsets
    daemonset_pods = [pod for pod in drain_node_list.podList.items if pod.controller_type == "DaemonSet"]
    if daemonset_pods:
        reporter.add_result(
            AnalysisResult(
                message=f"Pods controlled by DaemonSets will not be affected by node drain, they are {group_pods_by_namespace(daemonset_pods)}.",
                severity="none",
            )
        )

    # Check for running jobs/cronjobs
    job_pods = [
        pod
        for pod in drain_node_list.podList.items
        if pod.controller_type in ["Job", "CronJob"] and pod.status == "Running"
    ]
    if job_pods:
        reporter.add_result(
            AnalysisResult(
                message=f"Pods controlled by Jobs/CronJobs are running: {group_pods_by_namespace(job_pods)}. Please wait for them to finish.",
                severity="medium",
            )
        )

    # Check for pods with no controller
    no_controller_pods = [pod for pod in drain_node_list.podList.items if pod.controller_type is None]
    if no_controller_pods:
        reporter.add_result(
            AnalysisResult(
                message=f"Pods with no controller: {group_pods_by_namespace(no_controller_pods)}. Please check them.",
                severity="medium",
            )
        )

    # Check for pods with node selector
    node_selector_pods = [
        pod for pod in drain_node_list.podList.items if pod.node_selector and pod.controller_type != "DaemonSet"
    ]
    if node_selector_pods:
        for pod in node_selector_pods:
            if not node_selector_matches_node_list(pod.node_selector, node_list):
                reporter.add_result(
                    AnalysisResult(
                        message=f"Pod {pod.namespace}/{pod.name} has a node selector that does not match remaining nodes.",
                        severity="high",
                    )
                )

    # Check for pods with affinity/anti-affinity
    affinity_pods = [
        pod
        for pod in drain_node_list.podList.items
        if (pod.affinity or pod.anti_affinity) and pod.controller_type != "DaemonSet"
    ]
    if affinity_pods:
        for pod in affinity_pods:
            reporter.add_result(
                AnalysisResult(
                    message=f"Pods with affinity/anti-affinity: {pod.namespace}/{pod.name}. Please check if they can be scheduled on remaining nodes.",
                    severity="medium",
                )
            )

    # Check for taints and tolerations
    pods_to_reschedule = [pod for pod in drain_node_list.podList.items if pod.controller_type != "DaemonSet"]
    for pod in pods_to_reschedule:
        schedulable_nodes = []
        for node in node_list.items:
            if node.taints and len(node.taints) > 0:
                if not pod_tolerates_node_taints(pod.tolerations.items, node.taints.items):
                    continue
            schedulable_nodes.append(node.name)

        if not schedulable_nodes:
            reporter.add_result(
                AnalysisResult(
                    message=f"Pod {pod.namespace}/{pod.name} cannot be scheduled on any remaining nodes due to taints/tolerations.",
                    severity="high",
                )
            )

    # Check for resource constraints
    total_requests = Resource(0, 0)
    for pod in pods_to_reschedule:
        # Here we need to check if the pod has defined requests, if not, we should consider its metrics as the requests.
        # But sometimes the runtime metrics value may be less than the value when the pod was created, so we need to scale it up.
        total_requests.cpu += int(pod.requests.cpu if pod.requests.cpu else pod.metrics.cpu * factor)
        total_requests.memory += int(pod.requests.memory if pod.requests.memory else pod.metrics.memory * factor)

    total_allocatable = Resource(0, 0)
    for node in node_list.items:
        total_allocatable.cpu += node.allocatable.cpu
        total_allocatable.memory += node.allocatable.memory

    if total_requests.cpu > total_allocatable.cpu:
        reporter.add_result(
            AnalysisResult(
                message=f"Insufficient CPU resources in remaining nodes. Required: {total_requests.cpu}m, Available: {total_allocatable.cpu}m",
                severity="high",
            )
        )

    if total_requests.memory > total_allocatable.memory:
        reporter.add_result(
            AnalysisResult(
                message=f"Insufficient memory resources in remaining nodes. Required: {math.ceil(total_requests.memory)}Mi, Available: {math.ceil(total_allocatable.memory)}Mi",
                severity="high",
            )
        )

    # Check for architecture and OS compatibility
    drain_architectures = {node.architecture for node in drain_node_list.items}
    drain_os = {node.operatingSystem for node in drain_node_list.items}

    remaining_architectures = {node.architecture for node in node_list.items}
    remaining_os = {node.operatingSystem for node in node_list.items}

    # Check for missing architectures using set operations
    missing_architectures = drain_architectures - remaining_architectures
    if missing_architectures:
        reporter.add_result(
            AnalysisResult(
                message=f"Architecture(s) {', '.join(missing_architectures)} from drain nodes not available in remaining nodes. Some pods may not be schedulable.",
                severity="high",
            )
        )

    # Check for missing operating systems using set operations
    missing_os = drain_os - remaining_os
    if missing_os:
        reporter.add_result(
            AnalysisResult(
                message=f"Operating system(s) {', '.join(missing_os)} from drain nodes not available in remaining nodes. Some pods may not be schedulable.",
                severity="high",
            )
        )

    # Check for allocatable pods
    total_allocatable_pods = sum(node.allocatable.pods for node in node_list.items) - sum(
        len(node.podList.items) for node in node_list.items
    )
    if total_allocatable_pods < len(pods_to_reschedule):
        reporter.add_result(
            AnalysisResult(
                message=f"Insufficient allocatable pods in remaining nodes. Required: {len(pods_to_reschedule)}, Available: {total_allocatable_pods}",
                severity="high",
            )
        )

    # Check pod distribution after drain
    # Calculate the average pod count per node before and after drain
    current_pod_count = sum(len(node.podList.items) for node in node_list.items) + sum(
        len(node.podList.items) for node in drain_node_list.items
    )
    current_node_count = len(node_list.items) + len(drain_node_list.items)

    future_pod_count = sum(len(node.podList.items) for node in node_list.items) + len(pods_to_reschedule)
    future_node_count = len(node_list.items)

    if current_node_count > 0 and future_node_count > 0:
        current_avg = current_pod_count / current_node_count
        future_avg = future_pod_count / future_node_count

        if future_avg > current_avg * 1.5:  # 50% increase in pod density
            reporter.add_result(
                AnalysisResult(
                    message=f"Pod density will increase significantly from {current_avg:.1f} to {future_avg:.1f} pods per node.",
                    severity="medium",
                )
            )

    # After a comprehensive analysis, summarize into overall recommendations
    reporter.print_report()


def build_image_printable(image: Image) -> str:
    """Build a printable string for the image"""
    if not image:
        return "-"

    if not image.sizeBytes and not image.names:
        return "-"

    size = math.ceil(image.sizeBytes / 1024 / 1024)

    if not image.names and image.sizeBytes:
        return f"- ({size} MB)"

    image_name = next((i for i in image.names if ":" in i), None)
    if image_name:
        return f"{image_name} ({size} MB)"

    return f"{image.names[0]} ({size} MB)"


def main():
    args = parse_args()
    node_list = collect_node_list()

    output = sys.stdout
    file_opened = False
    try:
        if args.output != "stdout":
            try:
                output = open(args.output, "w")
                file_opened = True
                # If output file is specified, reconfigure the log handler
                for handler in logger.handlers[:]:
                    logger.removeHandler(handler)
                file_handler = logging.StreamHandler(output)
                file_handler.setFormatter(SimpleFormatter())
                logger.addHandler(file_handler)
            except IOError as e:
                logger.error(f"Error opening output file: {e}")
                sys.exit(1)

        if args.verbose:
            for node in node_list.items:
                logger.info(f"Node:\t\t{node.name}")

                if args.images:
                    logger.info(f"Images:\t\t{len(node.images)} / {math.ceil(node.images.size() / 1024 / 1024)}MB")
                    for image in node.images.items:
                        logger.info(f"  {build_image_printable(image)}")

                if args.taints:
                    logger.info(f"Taints:\t\t{node.taints}")

                if args.metrics:
                    logger.info(f"Metrics:\t{node.metrics}")

                logger.info(f"Allocatable:\t{node.allocatable}")
                logger.info(f"Capacity:\t{node.capacity}")
                if args.pods:
                    logger.info(f"Pods:\t\t{len(node.podList)}")
                    print_pod_list(node.podList, "table", args.wide)
                logger.info("")
                logger.info("")

        analyze(node_list, args.nodes, args.factor)
    finally:
        # Ensure the file is closed, even if an exception occurs
        if file_opened and output != sys.stdout:
            output.close()


if __name__ == "__main__":
    main()
