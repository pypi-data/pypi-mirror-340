"""
project_utils: Shared utilities for configuration and logging.
"""
from .config_utils import parse_config, write_config
from .logger import Logger, LogDecorator, LogWrapper, log

# Expose public interfaces of the module
__all__ = [
    "Logger",
    "LogDecorator",
    "LogWrapper",
    "log",
    "parse_config",
    "write_config"
]

# Optional dependencies
try:
    from .excel_utils import ExcelComparer, ExcelWriter
    __all__.append("ExcelComparer")
    __all__.append("ExcelWriter")
except ImportError:
    pass

try:
    from .jira_utils import JiraClient
    __all__.append("JiraClient")
except ImportError:
    pass

try:
    from .os_utils import DirectoryWatcher, DirectoryChangeEvent, FileScanner, ContentScanner, TraversalMethod, open_buffered_output_file
    __all__.append("DirectoryWatcher")
    __all__.append("DirectoryChangeEvent")
    __all__.append("FileScanner")
    __all__.append("ContentScanner")
    __all__.append("TraversalMethod")
    __all__.append("open_buffered_output_file")
except ImportError:
    pass

try:
    from .ai_utils import AzureOpenAIClient, OpenAIClientError, AzureDocumentIntelligenceClient, DocumentIntelligenceClientError
    __all__.append("AzureOpenAIClient")
    __all__.append("OpenAIClientError")
    __all__.append("AzureDocumentIntelligenceClient")
    __all__.append("DocumentIntelligenceClientError")
except ImportError:
    raise
