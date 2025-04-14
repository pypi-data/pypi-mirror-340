"""Test suite for ReflexQL clipboard exchange protocol."""
import pytest
from unittest.mock import MagicMock, patch
from click.testing import CliRunner
from tushell.tushellcli import cli, get_memory_manager
from tushell.reflexql import ClipboardExchange, ReflexQLMemoryKeys
import time

# Mock our memory manager for testing
@pytest.fixture(autouse=True)
def mock_get_memory_manager(monkeypatch):
    """Create and inject a mock memory manager."""
    mock_manager = MagicMock()
    def mock_get_memory():
        return mock_manager
    monkeypatch.setattr('tushell.tushellcli.get_memory_manager', mock_get_memory)
    return mock_manager

@pytest.fixture
def mock_memory_manager():
    """Create a mock memory manager for testing."""
    return MagicMock()

@pytest.fixture
def clipboard_exchange(mock_memory_manager):
    """Create a ClipboardExchange instance with mock memory manager."""
    return ClipboardExchange(mock_memory_manager)

def test_poll_clipboard_reflex_basic():
    """Test basic CLI command execution."""
    runner = CliRunner()
    result = runner.invoke(cli, ['poll-clipboard-reflex', '--ttl', '5'])
    assert result.exit_code == 0
    assert "🌟 Starting ReflexQL clipboard polling loop..." in result.output

def test_poll_clipboard_reflex_verbose():
    """Test verbose mode CLI execution."""
    runner = CliRunner()
    result = runner.invoke(cli, ['poll-clipboard-reflex', '--ttl', '5', '--verbose'])
    assert result.exit_code == 0
    assert "🌟 Starting ReflexQL clipboard polling loop..." in result.output

def test_poll_clipboard_reflex_custom_interval():
    """Test custom polling interval."""
    runner = CliRunner()
    result = runner.invoke(cli, ['poll-clipboard-reflex', '--poll-interval', '0.5', '--ttl', '5'])
    assert result.exit_code == 0
    assert "🌟 Starting ReflexQL clipboard polling loop..." in result.output

def test_clipboard_exchange_init(clipboard_exchange):
    """Test ClipboardExchange initialization."""
    assert clipboard_exchange.memory is not None
    assert hasattr(clipboard_exchange, 'copy_cmd')
    assert hasattr(clipboard_exchange, 'paste_cmd')

@patch('subprocess.Popen')
def test_write_to_clipboard(mock_popen, clipboard_exchange):
    """Test writing to system clipboard."""
    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_popen.return_value = mock_process
    
    result = clipboard_exchange.write_to_clipboard("test content")
    assert result is True
    mock_popen.assert_called_once()

@patch('subprocess.run')
def test_read_from_clipboard(mock_run, clipboard_exchange):
    """Test reading from system clipboard."""
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = "test content"
    
    result = clipboard_exchange.read_from_clipboard()
    assert result == "test content"
    mock_run.assert_called_once()

def test_send_to_clipboard(clipboard_exchange):
    """Test sending content through clipboard exchange protocol."""
    clipboard_exchange.memory.get.side_effect = [True]  # Simulate delivery confirmation
    
    result = clipboard_exchange.send_to_clipboard("test content")
    
    clipboard_exchange.memory.set.assert_any_call(ReflexQLMemoryKeys.PENDING_CONTENT, "test content")
    clipboard_exchange.memory.set.assert_any_call(ReflexQLMemoryKeys.READY, True)
    assert result is True

def test_reset_memory_keys(clipboard_exchange):
    """Test memory key reset functionality."""
    clipboard_exchange._reset_memory_keys()
    
    # Verify all protocol keys were reset
    for key in [ReflexQLMemoryKeys.PENDING_CONTENT, ReflexQLMemoryKeys.READY,
                ReflexQLMemoryKeys.DELIVERED, ReflexQLMemoryKeys.ACK]:
        clipboard_exchange.memory.set.assert_any_call(key, None)

@patch('time.sleep')  # Prevent actual sleeping in tests
def test_poll_clipboard_loop_timeout(mock_sleep, clipboard_exchange):
    """Test polling loop timeout behavior."""
    start_time = time.time()
    clipboard_exchange.poll_clipboard_loop(poll_interval=0.1, ttl=1)
    
    # Verify the loop respected the TTL
    assert time.time() - start_time >= 1
    mock_sleep.assert_called()

def test_poll_clipboard_loop_exchange(clipboard_exchange):
    """Test complete clipboard exchange cycle."""
    clipboard_exchange.memory.get.side_effect = [
        True,  # Ready flag
        "test content",  # Pending content
        False, True  # Ack flag (not ready, then ready)
    ]
    
    with patch.object(clipboard_exchange, 'write_to_clipboard') as mock_write:
        mock_write.return_value = True
        clipboard_exchange.poll_clipboard_loop(poll_interval=0.1, ttl=1)
        
        mock_write.assert_called_once_with("test content")
        clipboard_exchange.memory.set.assert_any_call(ReflexQLMemoryKeys.DELIVERED, True)