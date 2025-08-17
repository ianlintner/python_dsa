import importlib
import typing as t

import pytest

from flask_app.app import app as flask_app  # type: ignore
from flask_app.app import discover_demos  # type: ignore


@pytest.fixture(scope="module")
def client():
    flask_app.testing = True
    with flask_app.test_client() as c:
        yield c


def _flatten_categories(categories: dict[str, list[dict]]) -> list[dict]:
    out: list[dict] = []
    for demos in categories.values():
        out.extend(demos)
    return out


def test_index_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    # Dashboard should contain some known entries injected at runtime
    assert b"Sorting Visualizations" in resp.data


def test_big_o_page(client):
    resp = client.get("/big-o")
    assert resp.status_code == 200


@pytest.mark.parametrize(
    "url",
    [
        "/viz/sorting?algo=quick",
        "/viz/graph?algo=bfs",
        "/viz/path?algo=astar",
        "/viz/arrays?algo=binary_search",
        "/viz/mst?algo=kruskal",
        "/viz/topo?algo=kahn",
        "/viz/nn",
    ],
)
def test_visualization_pages(client, url):
    resp = client.get(url)
    assert resp.status_code == 200


def test_api_viz_sorting(client):
    resp = client.post(
        "/api/viz/sorting",
        data={"algo": "quick", "n": "10", "seed": "0", "unique": "true"},
    )
    assert resp.status_code == 200
    payload = resp.get_json()
    assert isinstance(payload, dict)
    assert "frames" in payload
    assert isinstance(payload["frames"], list)


def test_api_viz_graph(client):
    resp = client.post(
        "/api/viz/graph",
        data={"algo": "bfs", "n": "8", "p": "0.2", "start": "0", "seed": "0"},
    )
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), dict)


def test_api_viz_path(client):
    resp = client.post(
        "/api/viz/path",
        data={"algo": "astar", "rows": "10", "cols": "15", "density": "0.2", "seed": "0"},
    )
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), dict)


def test_api_viz_arrays(client):
    resp = client.post(
        "/api/viz/arrays",
        data={"algo": "binary_search", "n": "10", "seed": "0", "target": "5"},
    )
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), dict)


def test_api_viz_mst(client):
    resp = client.post(
        "/api/viz/mst",
        data={"algo": "kruskal", "n": "8", "k": "3", "start": "0", "seed": "0"},
    )
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), dict)


def test_api_viz_topo(client):
    resp = client.post(
        "/api/viz/topo",
        data={"algo": "kahn", "n": "8", "layers": "3", "p": "0.35", "seed": "0"},
    )
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), dict)


def test_api_viz_nn(client):
    # Keep this light: small dataset, few epochs, small grid
    resp = client.post(
        "/api/viz/nn",
        data={"dataset": "blobs", "n": "50", "hidden": "4", "lr": "0.1", "epochs": "1", "grid": "16", "seed": "0"},
    )
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), dict)


def test_demo_and_source_flows(client):
    cats = discover_demos()
    all_demos = _flatten_categories(cats)
    # Ensure we have at least one demo
    assert len(all_demos) > 0
    mod_id = all_demos[0]["id"]

    # /demo GET renders the page
    r1 = client.get(f"/demo?module={mod_id}")
    assert r1.status_code == 200

    # /api/demo executes the demo headlessly
    r2 = client.post("/api/demo", json={"module": mod_id})
    assert r2.status_code == 200
    data = r2.get_json()
    assert isinstance(data, dict)
    assert "output" in data

    # /demo POST renders output page (should not 5xx even if demo has errors)
    r3 = client.post("/demo", data={"module": mod_id})
    assert r3.status_code == 200

    # /source shows code for the module
    r4 = client.get(f"/source?module={mod_id}")
    assert r4.status_code == 200
