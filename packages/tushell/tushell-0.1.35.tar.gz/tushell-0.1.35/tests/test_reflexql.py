import pytest
from click.testing import CliRunner
from tushell.tushellcli import cli
import json
import time

def test_poll_clipboard_reflex_basic():
    runner = CliRunner()
    result = runner.invoke(cli, ['poll-clipboard-reflex', '--ttl', '5'])
    assert result.exit_code == 0
    assert "🌟 Starting ReflexQL clipboard polling loop..." in result.output

def test_poll_clipboard_reflex_verbose():
    runner = CliRunner()
    result = runner.invoke(cli, ['poll-clipboard-reflex', '--ttl', '5', '--verbose'])
    assert result.exit_code == 0
    assert "🌟 Starting ReflexQL clipboard polling loop..." in result.output

def test_poll_clipboard_reflex_custom_interval():
    runner = CliRunner()
    result = runner.invoke(cli, ['poll-clipboard-reflex', '--poll-interval', '0.5', '--ttl', '5'])
    assert result.exit_code == 0
    assert "🌟 Starting ReflexQL clipboard polling loop..." in result.output