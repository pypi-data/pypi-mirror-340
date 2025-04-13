# tests/test_handlers.py
import json
import xml.etree.ElementTree as ET
from unittest import mock

import pytest
import toml
import yaml
from src.bumpcalver.handlers import (
    DockerfileVersionHandler,
    JsonVersionHandler,
    MakefileVersionHandler,
    PythonVersionHandler,
    TomlVersionHandler,
    XmlVersionHandler,
    YamlVersionHandler,
    get_version_handler,
    update_version_in_files,
)


def test_python_handler_read_version(monkeypatch):
    handler = PythonVersionHandler()
    file_content = """
__version__ = "2023-10-10"
"""
    mock_open = mock.mock_open(read_data=file_content)
    monkeypatch.setattr("builtins.open", mock_open)

    version = handler.read_version("dummy_file.py", "__version__")
    assert version == "2023-10-10"


def test_python_handler_update_version(monkeypatch):
    handler = PythonVersionHandler()
    file_content = """
__version__ = "2023-10-10"
"""
    # Expected content after update
    mock_open = mock.mock_open(read_data=file_content)
    monkeypatch.setattr("builtins.open", mock_open)

    result = handler.update_version("dummy_file.py", "__version__", "2023-10-11")
    assert result is True

    handle = mock_open()
    handle.write.assert_called_once()
    written_content = handle.write.call_args[0][0]
    assert '__version__ = "2023-10-11"' in written_content


def test_python_handler_update_version_exception(monkeypatch, capsys):
    handler = PythonVersionHandler()
    file_content = '__version__ = "2023-10-10"'

    # Create a mock for 'open' that raises an exception when writing
    mock_open = mock.mock_open(read_data=file_content)
    mock_open.side_effect = [
        mock_open.return_value,
        IOError("Unable to open file for writing"),
    ]

    monkeypatch.setattr("builtins.open", mock_open)

    result = handler.update_version("dummy_file.py", "__version__", "2023-10-11")
    assert result is False

    captured = capsys.readouterr()
    assert (
        "Error updating dummy_file.py: Unable to open file for writing" in captured.out
    )


def test_toml_handler_read_version(monkeypatch):
    handler = TomlVersionHandler()
    toml_content = """
[tool.poetry]
version = "2023-10-10"
"""
    mock_open = mock.mock_open(read_data=toml_content)
    monkeypatch.setattr("builtins.open", mock_open)
    monkeypatch.setattr(
        toml, "load", lambda f: {"tool": {"poetry": {"version": "2023-10-10"}}}
    )

    version = handler.read_version("pyproject.toml", "tool.poetry.version")
    assert version == "2023-10-10"


def test_toml_handler_update_version(monkeypatch):
    handler = TomlVersionHandler()
    toml_content = """
[tool.poetry]
version = "2023-10-10"
"""
    mock_open = mock.mock_open(read_data=toml_content)
    monkeypatch.setattr("builtins.open", mock_open)
    toml_data = {"tool": {"poetry": {"version": "2023-10-10"}}}
    monkeypatch.setattr(toml, "load", lambda f: toml_data)
    dump_mock = mock.Mock()
    monkeypatch.setattr(toml, "dump", dump_mock)

    result = handler.update_version(
        "pyproject.toml", "tool.poetry.version", "2023-10-11"
    )
    assert result is True

    expected_data = {"tool": {"poetry": {"version": "2023-10-11"}}}
    dump_mock.assert_called_once()
    args, kwargs = dump_mock.call_args
    assert args[0] == expected_data


def test_yaml_handler_read_version(monkeypatch):
    handler = YamlVersionHandler()
    yaml_content = """
version: "2023-10-10"
"""
    mock_open = mock.mock_open(read_data=yaml_content)
    monkeypatch.setattr("builtins.open", mock_open)
    monkeypatch.setattr(yaml, "safe_load", lambda f: {"version": "2023-10-10"})

    version = handler.read_version("config.yaml", "version")
    assert version == "2023-10-10"


def test_yaml_handler_update_version(monkeypatch):
    handler = YamlVersionHandler()
    yaml_content = """
version: "2023-10-10"
"""
    mock_open = mock.mock_open(read_data=yaml_content)
    monkeypatch.setattr("builtins.open", mock_open)
    yaml_data = {"version": "2023-10-10"}
    monkeypatch.setattr(yaml, "safe_load", lambda f: yaml_data)
    dump_mock = mock.Mock()
    monkeypatch.setattr(yaml, "safe_dump", dump_mock)

    result = handler.update_version("config.yaml", "version", "2023-10-11")
    assert result is True

    expected_data = {"version": "2023-10-11"}
    dump_mock.assert_called_once_with(expected_data, mock.ANY)


def test_yaml_handler_read_version_exception(monkeypatch, capsys):
    handler = YamlVersionHandler()

    # Simulate an exception during file reading
    def mock_open(*args, **kwargs):
        raise IOError("Unable to open file")

    monkeypatch.setattr("builtins.open", mock_open)

    version = handler.read_version("config.yaml", "version")
    assert version is None

    captured = capsys.readouterr()
    assert "Error reading version from config.yaml: Unable to open file" in captured.out


def test_yaml_handler_update_version_exception(monkeypatch, capsys):
    handler = YamlVersionHandler()

    # Simulate an exception during yaml.safe_load
    def mock_yaml_load(f):
        raise yaml.YAMLError("Malformed YAML")

    monkeypatch.setattr("yaml.safe_load", mock_yaml_load)
    mock_open = mock.mock_open()
    monkeypatch.setattr("builtins.open", mock_open)

    result = handler.update_version("config.yaml", "version", "2023-10-11")
    assert result is False

    captured = capsys.readouterr()
    assert "Error updating config.yaml: Malformed YAML" in captured.out


def test_json_handler_read_version(monkeypatch):
    handler = JsonVersionHandler()
    json_content = """
{
    "version": "2023-10-10"
}
"""
    mock_open = mock.mock_open(read_data=json_content)
    monkeypatch.setattr("builtins.open", mock_open)
    monkeypatch.setattr(json, "load", lambda f: {"version": "2023-10-10"})

    version = handler.read_version("package.json", "version")
    assert version == "2023-10-10"


def test_json_handler_update_version(monkeypatch):
    handler = JsonVersionHandler()
    json_content = """
{
    "version": "2023-10-10"
}
"""
    mock_open = mock.mock_open(read_data=json_content)
    monkeypatch.setattr("builtins.open", mock_open)
    json_data = {"version": "2023-10-10"}
    monkeypatch.setattr(json, "load", lambda f: json_data)
    dump_mock = mock.Mock()
    monkeypatch.setattr(json, "dump", dump_mock)

    result = handler.update_version("package.json", "version", "2023-10-11")
    assert result is True

    expected_data = {"version": "2023-10-11"}
    dump_mock.assert_called_once_with(expected_data, mock.ANY, indent=2)


def test_json_handler_read_version_exception(monkeypatch, capsys):
    handler = JsonVersionHandler()

    # Simulate an exception during json.load
    def mock_json_load(f):
        raise json.JSONDecodeError("Malformed JSON", "", 0)

    monkeypatch.setattr("json.load", mock_json_load)
    mock_open = mock.mock_open()
    monkeypatch.setattr("builtins.open", mock_open)

    version = handler.read_version("package.json", "version")
    assert version is None

    captured = capsys.readouterr()
    assert "Error reading version from package.json: Malformed JSON" in captured.out


def test_json_handler_update_version_exception(monkeypatch, capsys):
    handler = JsonVersionHandler()

    # Simulate an exception during json.load
    def mock_json_load(f):
        raise json.JSONDecodeError("Malformed JSON", "", 0)

    monkeypatch.setattr("json.load", mock_json_load)
    mock_open = mock.mock_open()
    monkeypatch.setattr("builtins.open", mock_open)

    result = handler.update_version("package.json", "version", "2023-10-11")
    assert result is False

    captured = capsys.readouterr()
    assert "Error updating package.json: Malformed JSON" in captured.out


def test_xml_handler_read_version(monkeypatch):
    handler = XmlVersionHandler()
    mock_tree = mock.Mock()
    mock_root = mock.Mock()
    mock_element = mock.Mock()
    mock_element.text = "2023-10-10"
    mock_root.find.return_value = mock_element
    mock_tree.getroot.return_value = mock_root
    monkeypatch.setattr(ET, "parse", lambda f: mock_tree)

    version = handler.read_version("config.xml", "version")
    assert version == "2023-10-10"


def test_xml_handler_update_version(monkeypatch):
    handler = XmlVersionHandler()
    mock_tree = mock.Mock()
    mock_root = mock.Mock()
    mock_element = mock.Mock()
    mock_root.find.return_value = mock_element
    mock_tree.getroot.return_value = mock_root
    monkeypatch.setattr(ET, "parse", lambda f: mock_tree)

    result = handler.update_version("config.xml", "version", "2023-10-11")
    assert result is True

    assert mock_element.text == "2023-10-11"
    mock_tree.write.assert_called_once_with("config.xml")


def test_xml_handler_read_version_exception(monkeypatch, capsys):
    handler = XmlVersionHandler()

    # Simulate an exception during ET.parse
    def mock_et_parse(file):
        raise ET.ParseError("Malformed XML")

    monkeypatch.setattr("xml.etree.ElementTree.parse", mock_et_parse)

    version = handler.read_version("config.xml", "version")
    assert version is None

    captured = capsys.readouterr()
    assert "Error reading version from config.xml: Malformed XML" in captured.out


def test_xml_handler_update_version_exception(monkeypatch, capsys):
    handler = XmlVersionHandler()

    # Simulate an exception during ET.parse
    def mock_et_parse(file):
        raise ET.ParseError("Malformed XML")

    monkeypatch.setattr("xml.etree.ElementTree.parse", mock_et_parse)

    result = handler.update_version("config.xml", "version", "2023-10-11")
    assert result is False

    captured = capsys.readouterr()
    assert "Error updating config.xml: Malformed XML" in captured.out


def test_dockerfile_handler_read_version(monkeypatch):
    handler = DockerfileVersionHandler()
    dockerfile_content = """
FROM python:3.8
ARG VERSION=2023-10-10
"""
    mock_open = mock.mock_open(read_data=dockerfile_content)
    monkeypatch.setattr("builtins.open", mock_open)

    version = handler.read_version("Dockerfile", "VERSION", directive="ARG")
    assert version == "2023-10-10"


def test_dockerfile_handler_update_version(monkeypatch):
    handler = DockerfileVersionHandler()
    dockerfile_content = """
FROM python:3.8
ARG VERSION=2023-10-10
"""
    mock_open = mock.mock_open(read_data=dockerfile_content)
    monkeypatch.setattr("builtins.open", mock_open)

    result = handler.update_version(
        "Dockerfile", "VERSION", "2023-10-11", directive="ARG"
    )
    assert result is True

    handle = mock_open()
    handle.write.assert_called_once()
    written_content = handle.write.call_args[0][0]
    assert "ARG VERSION=2023-10-11" in written_content


def test_dockerfile_handler_update_version_invalid_directive(capsys):
    handler = DockerfileVersionHandler()

    result = handler.update_version(
        "Dockerfile", "VERSION", "2023-10-11", directive="INVALID"
    )
    assert result is False

    captured = capsys.readouterr()
    assert (
        "Invalid or missing directive for variable 'VERSION' in Dockerfile."
        in captured.out
    )


def test_dockerfile_handler_read_version_invalid_directive(capsys):
    handler = DockerfileVersionHandler()

    version = handler.read_version("Dockerfile", "VERSION", directive="INVALID")
    assert version is None

    captured = capsys.readouterr()
    assert (
        "Invalid or missing directive for variable 'VERSION' in Dockerfile."
        in captured.out
    )


def test_dockerfile_handler_update_version_exception(monkeypatch, capsys):
    handler = DockerfileVersionHandler()

    # Simulate an exception during file reading
    def mock_open(*args, **kwargs):
        raise IOError("Unable to open file")

    monkeypatch.setattr("builtins.open", mock_open)

    result = handler.update_version(
        "Dockerfile", "VERSION", "2023-10-11", directive="ARG"
    )
    assert result is False

    captured = capsys.readouterr()
    assert "Error updating Dockerfile: Unable to open file" in captured.out


def test_dockerfile_handler_read_version_exception(monkeypatch, capsys):
    handler = DockerfileVersionHandler()

    # Simulate an exception during file reading
    def mock_open(*args, **kwargs):
        raise IOError("Unable to open file")

    monkeypatch.setattr("builtins.open", mock_open)

    version = handler.read_version("Dockerfile", "VERSION", directive="ARG")
    assert version is None

    captured = capsys.readouterr()
    assert "Error reading version from Dockerfile: Unable to open file" in captured.out


def test_makefile_handler_read_version(monkeypatch):
    handler = MakefileVersionHandler()
    makefile_content = """
VERSION = 2023-10-10
"""
    mock_open = mock.mock_open(read_data=makefile_content)
    monkeypatch.setattr("builtins.open", mock_open)

    version = handler.read_version("Makefile", "VERSION")
    assert version == "2023-10-10"


def test_makefile_handler_update_version(monkeypatch):
    handler = MakefileVersionHandler()
    makefile_content = """
VERSION = 2023-10-10
"""
    mock_open = mock.mock_open(read_data=makefile_content)
    monkeypatch.setattr("builtins.open", mock_open)

    result = handler.update_version("Makefile", "VERSION", "2023-10-11")
    assert result is True

    handle = mock_open()
    handle.write.assert_called_once()
    written_content = handle.write.call_args[0][0]
    assert "VERSION = 2023-10-11" in written_content


def test_makefile_handler_read_version_exception(monkeypatch, capsys):
    handler = MakefileVersionHandler()

    # Simulate an exception during file reading
    def mock_open(*args, **kwargs):
        raise IOError("Unable to open file")

    monkeypatch.setattr("builtins.open", mock_open)

    version = handler.read_version("Makefile", "VERSION")
    assert version is None

    captured = capsys.readouterr()
    assert "Error reading version from Makefile: Unable to open file" in captured.out


def test_makefile_handler_update_version_exception(monkeypatch, capsys):
    handler = MakefileVersionHandler()

    # Simulate an exception during file reading
    def mock_open(*args, **kwargs):
        raise IOError("Unable to open file")

    monkeypatch.setattr("builtins.open", mock_open)

    result = handler.update_version("Makefile", "VERSION", "2023-10-11")
    assert result is False

    captured = capsys.readouterr()
    assert "Error updating Makefile: Unable to open file" in captured.out


def test_get_version_handler():
    handler = get_version_handler("python")
    assert isinstance(handler, PythonVersionHandler)

    with pytest.raises(ValueError):
        get_version_handler("unsupported")


def test_python_handler_read_version_exception(monkeypatch, capsys):
    handler = PythonVersionHandler()

    # Simulate an exception during file reading
    def mock_open(*args, **kwargs):
        raise IOError("Unable to open file")

    monkeypatch.setattr("builtins.open", mock_open)

    version = handler.read_version("nonexistent_file.py", "__version__")
    assert version is None

    captured = capsys.readouterr()
    assert (
        "Error reading version from nonexistent_file.py: Unable to open file"
        in captured.out
    )


def test_python_handler_update_version_variable_not_found(monkeypatch, capsys):
    handler = PythonVersionHandler()
    file_content = """
__not_version__ = "2023-10-10"
"""
    mock_open = mock.mock_open(read_data=file_content)
    monkeypatch.setattr("builtins.open", mock_open)

    result = handler.update_version("dummy_file.py", "__version__", "2023-10-11")
    assert result is False

    captured = capsys.readouterr()
    assert "Variable '__version__' not found in dummy_file.py" in captured.out


def test_toml_handler_read_version_malformed_toml(monkeypatch, capsys):
    from src.bumpcalver import handlers

    handler = handlers.TomlVersionHandler()

    # Simulate malformed TOML content
    def mock_toml_load(f):
        raise handlers.toml.TomlDecodeError("Malformed TOML", "", 0)

    # Monkeypatch the 'toml.load' function in the handlers module
    monkeypatch.setattr(handlers.toml, "load", mock_toml_load)

    mock_open = mock.mock_open()
    monkeypatch.setattr("builtins.open", mock_open)

    version = handler.read_version("pyproject.toml", "tool.poetry.version")
    assert version is None

    captured = capsys.readouterr()
    assert "Error reading version from pyproject.toml: Malformed TOML" in captured.out


def test_toml_handler_update_version_exception(monkeypatch, capsys):
    from src.bumpcalver import handlers

    handler = handlers.TomlVersionHandler()

    # Simulate an exception during toml.load
    def mock_toml_load(f):
        raise handlers.toml.TomlDecodeError("Malformed TOML", "", 0)

    monkeypatch.setattr(handlers.toml, "load", mock_toml_load)
    mock_open = mock.mock_open()
    monkeypatch.setattr("builtins.open", mock_open)

    result = handler.update_version(
        "pyproject.toml", "tool.poetry.version", "2023-10-11"
    )
    assert result is False

    captured = capsys.readouterr()
    assert "Error updating pyproject.toml: Malformed TOML" in captured.out


def test_get_version_handler_unsupported_file_type():
    with pytest.raises(ValueError) as exc_info:
        get_version_handler("unsupported")
    assert "Unsupported file type: unsupported" in str(exc_info.value)


def test_update_version_in_files_value_error(capsys):
    new_version = "2023-10-11"
    file_configs = [
        {
            "path": "dummy_file.unsupported",
            "file_type": "unsupported",
            "variable": "__version__",
        }
    ]

    try:
        update_version_in_files(new_version, file_configs)
    except ValueError as e:
        assert str(e) == "Unsupported file type: unsupported"


def test_toml_handler_read_version_variable_not_found(monkeypatch, capsys):
    handler = TomlVersionHandler()
    toml_content = """
[tool.poetry]
name = "example"
"""
    mock_open = mock.mock_open(read_data=toml_content)
    monkeypatch.setattr("builtins.open", mock_open)
    monkeypatch.setattr(
        toml, "load", lambda f: {"tool": {"poetry": {"name": "example"}}}
    )

    version = handler.read_version("pyproject.toml", "tool.poetry.version")
    assert version is None

    captured = capsys.readouterr()
    assert "Variable 'tool.poetry.version' not found in pyproject.toml" in captured.out


def test_toml_handler_update_version_variable_not_found(monkeypatch, capsys):
    handler = TomlVersionHandler()
    toml_content = """
[tool.poetry]
name = "example"
"""
    mock_open = mock.mock_open(read_data=toml_content)
    monkeypatch.setattr("builtins.open", mock_open)
    toml_data = {"tool": {"poetry": {"name": "example"}}}
    monkeypatch.setattr(toml, "load", lambda f: toml_data)
    dump_mock = mock.Mock()
    monkeypatch.setattr(toml, "dump", dump_mock)

    result = handler.update_version(
        "pyproject.toml", "tool.poetry.version", "2023-10-11"
    )
    assert result is False

    captured = capsys.readouterr()
    assert "Variable 'tool.poetry.version' not found in pyproject.toml" in captured.out


def test_yaml_handler_read_version_variable_not_found(monkeypatch, capsys):
    handler = YamlVersionHandler()
    yaml_content = """
version: "2023-10-10"
"""
    mock_open = mock.mock_open(read_data=yaml_content)
    monkeypatch.setattr("builtins.open", mock_open)
    monkeypatch.setattr(yaml, "safe_load", lambda f: {"version": "2023-10-10"})

    version = handler.read_version("config.yaml", "nonexistent_variable")
    assert version is None

    captured = capsys.readouterr()
    assert "Variable 'nonexistent_variable' not found in config.yaml" in captured.out


def test_xml_handler_update_version_variable_not_found(monkeypatch, capsys):
    handler = XmlVersionHandler()
    xml_content = """
<configuration>
    <version>2023-10-10</version>
</configuration>
"""
    mock_open = mock.mock_open(read_data=xml_content)
    monkeypatch.setattr("builtins.open", mock_open)
    monkeypatch.setattr(
        ET, "parse", lambda f: ET.ElementTree(ET.fromstring(xml_content))
    )

    result = handler.update_version("config.xml", "nonexistent_variable", "2023-10-11")
    assert result is False

    captured = capsys.readouterr()
    print(f"Captured output: {captured.out}")  # Debugging line
    assert "Variable 'nonexistent_variable' not found in config.xml" in captured.out


def test_dockerfile_handler_read_version_variable_not_found(monkeypatch, capsys):
    handler = DockerfileVersionHandler()
    dockerfile_content = """
FROM python:3.8
"""
    mock_open = mock.mock_open(read_data=dockerfile_content)
    monkeypatch.setattr("builtins.open", mock_open)

    version = handler.read_version("Dockerfile", "VERSION", directive="ARG")
    assert version is None

    captured = capsys.readouterr()
    assert "No ARG variable 'VERSION' found in Dockerfile" in captured.out


def test_dockerfile_handler_update_version_variable_not_found(monkeypatch, capsys):
    handler = DockerfileVersionHandler()
    dockerfile_content = """
FROM python:3.8
"""
    mock_open = mock.mock_open(read_data=dockerfile_content)
    monkeypatch.setattr("builtins.open", mock_open)

    result = handler.update_version(
        "Dockerfile", "VERSION", "2023-10-11", directive="ARG"
    )
    assert result is False

    captured = capsys.readouterr()
    assert "No ARG variable 'VERSION' found in Dockerfile" in captured.out


def test_xml_handler_read_version_variable_not_found(monkeypatch, capsys):
    handler = XmlVersionHandler()
    mock_tree = mock.Mock()
    mock_root = mock.Mock()
    mock_root.find.return_value = None
    mock_tree.getroot.return_value = mock_root
    monkeypatch.setattr(ET, "parse", lambda f: mock_tree)

    version = handler.read_version("config.xml", "version")
    assert version is None

    captured = capsys.readouterr()
    assert "Variable 'version' not found in config.xml" in captured.out


def test_makefile_handler_update_version_variable_not_found(monkeypatch, capsys):
    handler = MakefileVersionHandler()
    file_content = """
VERSION = 2023-10-10
"""
    mock_open = mock.mock_open(read_data=file_content)
    monkeypatch.setattr("builtins.open", mock_open)

    result = handler.update_version("Makefile", "NON_EXISTENT_VARIABLE", "2023-10-11")
    assert result is False

    captured = capsys.readouterr()
    assert "Variable 'NON_EXISTENT_VARIABLE' not found in Makefile" in captured.out


def test_update_version_in_files_no_file_type(capsys):
    new_version = "2023-10-11"
    file_configs = [{"path": "dummy_file.py", "variable": "__version__"}]

    try:
        update_version_in_files(new_version, file_configs)
    except ValueError as e:
        assert str(e) == "Unsupported file type: "
