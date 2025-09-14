import orjson, pathlib, pytest
from src.aioworxmower.parsers.worx import parse_status, build_command

pytestmark = pytest.mark.unit

def load_fixture(name: str):
    p = pathlib.Path(__file__).parent / "fixtures" / name
    return orjson.loads(p.read_bytes())

def test_parse_status_fixture_1():
    payload = load_fixture("status_sample_1.json")
    m = parse_status(payload)
    assert m["battery"] == 72
    assert m["status_text"] == "mowing"
    assert m["latitude"] == 50.1 and m["longitude"] == 8.6

def test_parse_status_fixture_2_code_map():
    payload = load_fixture("status_sample_2.json")
    m = parse_status(payload)
    assert m["status_text"] in ("mowing", "code_2")

def test_numeric_commands():
    assert build_command("start") == {"cmd": 1}
    assert build_command("pause") == {"cmd": 4}
    assert build_command("home")  == {"cmd": 3}
