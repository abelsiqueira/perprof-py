"""Improved logging tests - focused, lean, and less coupled."""

import logging
import re
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from perprof.main import set_arguments, setup_logging


class TestLoggingSetup:
    """Unit tests for logging configuration - focused on infrastructure."""

    def teardown_method(self):
        """Clean up logging configuration."""
        logger = logging.getLogger("perprof")
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        logger.setLevel(logging.NOTSET)

    def test_logging_levels(self, capsys):
        """Test that logging levels are set correctly."""
        # Test default (WARNING)
        setup_logging()
        logger = logging.getLogger("perprof.test")
        logger.info("info")
        logger.warning("warning")

        captured = capsys.readouterr()
        assert "info" not in captured.err
        assert "warning" in captured.err

        # Test verbose (INFO)
        setup_logging(verbose=True)
        logger.info("info")
        captured = capsys.readouterr()
        assert "info" in captured.err

        # Test debug (DEBUG)
        setup_logging(debug=True)
        logger.debug("debug")
        captured = capsys.readouterr()
        assert "debug" in captured.err

    def test_log_format_structure(self, capsys):
        """Test log format without coupling to exact messages."""
        setup_logging(verbose=True)
        logger = logging.getLogger("perprof.module.submodule")
        logger.info("test message")

        captured = capsys.readouterr()
        # Test format structure: [LEVEL] logger.name: message
        log_pattern = r"\[INFO\] perprof\.module\.submodule: test message"
        assert re.search(log_pattern, captured.err)

    def test_file_logging_works(self):
        """Test file logging without asserting on specific content."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            log_file_path = tmp_file.name

        try:
            setup_logging(verbose=True, log_file=log_file_path)
            logger = logging.getLogger("perprof.test")
            logger.info("test message")

            # Verify file was created and has content
            log_file = Path(log_file_path)
            assert log_file.exists()
            assert log_file.stat().st_size > 0

            # Verify it contains structured log format
            content = log_file.read_text()
            assert "[INFO] perprof.test:" in content
        finally:
            Path(log_file_path).unlink(missing_ok=True)

    def test_no_duplicate_handlers(self, capsys):
        """Test that multiple setup calls don't create duplicates."""
        setup_logging(verbose=True)
        setup_logging(verbose=True)  # Second call

        logger = logging.getLogger("perprof.test")
        logger.info("once")

        captured = capsys.readouterr()
        # Should appear exactly once
        assert captured.err.count("once") == 1


class TestLoggingCLIIntegration:
    """Integration tests for logging with CLI - minimal coupling."""

    def test_logging_cli_args_parsed(self):
        """Test that logging CLI arguments are parsed correctly."""
        args = set_arguments(["--verbose", "--demo", "--mp"])
        assert args.verbose is True
        assert args.debug is False
        assert args.log_file is None

        args = set_arguments(["--debug", "--log-file", "test.log", "--demo", "--mp"])
        assert args.debug is True
        assert args.log_file == "test.log"

    def test_logging_setup_integration(self, capsys):
        """Test that logging setup works with real CLI args."""
        # Test that we can parse args and setup logging without errors
        args = set_arguments(["--verbose", "--demo", "--mp"])
        setup_logging(verbose=args.verbose, debug=args.debug, log_file=args.log_file)

        # Test that the setup actually works
        logger = logging.getLogger("perprof.test")
        logger.info("integration test")

        captured = capsys.readouterr()
        assert "integration test" in captured.err


class TestLoggingBehaviorProperties:
    """Property-based tests for logging behavior."""

    def teardown_method(self):
        """Clean up logging configuration."""
        logger = logging.getLogger("perprof")
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        logger.setLevel(logging.NOTSET)

    @pytest.mark.parametrize(
        "verbose,debug,should_log_info,should_log_debug",
        [
            (False, False, False, False),  # Default: only WARNING+
            (True, False, True, False),  # Verbose: INFO+
            (False, True, True, True),  # Debug: DEBUG+
            (True, True, True, True),  # Both: DEBUG+ (debug overrides)
        ],
    )
    def test_logging_level_behavior(
        self, verbose, debug, should_log_info, should_log_debug, capsys
    ):
        """Test logging level behavior across different configurations."""
        setup_logging(verbose=verbose, debug=debug)
        logger = logging.getLogger("perprof.test")

        logger.debug("debug_msg")
        logger.info("info_msg")
        logger.warning("warning_msg")

        captured = capsys.readouterr()

        # WARNING should always appear
        assert "warning_msg" in captured.err

        # INFO should appear based on configuration
        assert ("info_msg" in captured.err) == should_log_info

        # DEBUG should appear based on configuration
        assert ("debug_msg" in captured.err) == should_log_debug

    def test_logging_doesnt_interfere_with_stdout(self, capsys):
        """Test that logging goes to stderr, not stdout."""
        setup_logging(verbose=True)
        logger = logging.getLogger("perprof.test")

        print("stdout message")  # Application output
        logger.info("stderr message")  # Log output

        captured = capsys.readouterr()
        assert "stdout message" in captured.out
        assert "stderr message" in captured.err
        assert "stderr message" not in captured.out

    def test_logger_hierarchy_works(self, capsys):
        """Test that logger hierarchy works correctly."""
        setup_logging(verbose=True)

        # Different loggers should all work
        main_logger = logging.getLogger("perprof.main")
        data_logger = logging.getLogger("perprof.profile_data")

        main_logger.info("main message")
        data_logger.info("data message")

        captured = capsys.readouterr()
        assert "perprof.main: main message" in captured.err
        assert "perprof.profile_data: data message" in captured.err


# Optional: Minimal smoke test for real application usage
class TestLoggingSmoke:
    """Smoke tests to ensure logging doesn't break real usage."""

    def test_logging_with_demo_execution(self, capsys):
        """Test that logging works with actual demo execution."""
        from perprof.main import main

        with patch("sys.argv", ["perprof", "--verbose", "--demo", "--raw"]):
            # This should run without errors and produce logs
            main()

            captured = capsys.readouterr()
            # Verify logging infrastructure worked (without exact message coupling)
            assert "[INFO] perprof.main:" in captured.err
            # Verify app still works (raw output should appear)
            assert captured.out  # Some output was produced
