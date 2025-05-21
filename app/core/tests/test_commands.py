from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error  # type: ignore
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase
from io import StringIO


class CommandTests(TestCase):
    """Test commands."""

    @patch("core.management.commands.wait_for_db.time.sleep")
    @patch("core.management.commands.wait_for_db.connections")
    def test_wait_for_db_delay(self, mock_connections, mocked_sleep):
        """Test waiting for db when getting operational error."""
        side_effect = [Psycopg2Error("Connection refused")] * 2 + \
                    [OperationalError("Database not ready")] * 3 + \
                    [None]  # Success

        mock_conn = mock_connections.__getitem__.return_value
        mock_conn.cursor.side_effect = side_effect

        call_command("wait_for_db")

        self.assertEqual(mock_connections.__getitem__.call_count, 6)
        mock_connections.__getitem__.assert_called_with('default')
        self.assertEqual(mocked_sleep.call_count, 5)
        mocked_sleep.assert_called_with(2)
    
    @patch("core.management.commands.wait_for_db.connections")
    def test_wait_for_db_ready(self, mock_connections):
        """Test waiting for db when db is available."""
        mock_cursor = mock_connections.__getitem__.return_value.cursor
        mock_cursor.return_value = None  # Simulate success

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            call_command("wait_for_db")
            mock_connections.__getitem__.assert_called_with('default')
            self.assertEqual(mock_connections.__getitem__.call_count, 1)
            self.assertIn("Database available after 1 attempt(s)!", mock_stdout.getvalue())


