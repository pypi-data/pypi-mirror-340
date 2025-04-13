"""Constants used throughout the SSLSpy toolkit."""

# Status codes
STATUS_VALID = "VALID"
STATUS_WARNING = "WARNING"
STATUS_EXPIRED = "EXPIRED"
STATUS_TIMEOUT = "TIMEOUT"
STATUS_ERROR = "ERROR"

# Default settings
DEFAULT_TIMEOUT = 5  # seconds
DEFAULT_WARNING_THRESHOLD = 30  # days
MAX_WORKERS = 10  # maximum concurrent connections

# UI settings
MAX_LOG_LINES = 10

# UI presentation constants
BOX_WIDTH = 100  # Total width of the UI box
DOMAIN_WIDTH = 45  # Width for domain display in log lines
STATUS_WIDTH = 20  # Width for status display in log lines
MAX_ERROR_LENGTH = 25  # Maximum length for error messages
LOG_DISPLAY_LIMIT = 10  # Number of log lines to display in the UI
PROGRESS_BAR_WIDTH = 70  # Width of the progress bar
STATS_ITEM_WIDTH = 5  # Width for count numbers in status summary

# Shared state flags for controlling execution
EXITING = False
PAUSED = False
