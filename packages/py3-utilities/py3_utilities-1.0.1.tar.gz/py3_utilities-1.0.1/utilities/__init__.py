"""
project_utils: Shared utilities for configuration and logging.
"""
__all__ = []

# Import Config parser and writer
try:
    from .config_utils import parse_config, write_config
    __all__.append("parse_config")
    __all__.append("write_config")
except ImportError:
    pass

# Import Logger module
try:
    from .logger import Logger, LogDecorator, LogWrapper, log
    __all__.append("Logger")
    __all__.append("LogDecorator")
    __all__.append("LogWrapper")
    __all__.append("log")
except ImportError:
    pass

# Import Excel utils
try:
    from .excel_utils import ExcelComparer, ExcelWriter
    __all__.append("ExcelComparer")
    __all__.append("ExcelWriter")
except ImportError:
    pass

# Import Jira utils
try:
    from .jira_utils import JiraClient
    __all__.append("JiraClient")
except ImportError:
    pass

# Import OS utils
try:
    from .os_utils import DirectoryWatcher, DirectoryChangeEvent, FileScanner, ContentScanner, TraversalMethod
    __all__.append("DirectoryWatcher")
    __all__.append("DirectoryChangeEvent")
    __all__.append("FileScanner")
    __all__.append("ContentScanner")
    __all__.append("TraversalMethod")
except ImportError:
    pass

# Import AI utils
try:
    from .ai_utils import AzureOpenAIClient, OpenAIClientError, AzureDocumentIntelligenceClient, DocumentIntelligenceClientError
    __all__.append("AzureOpenAIClient")
    __all__.append("OpenAIClientError")
    __all__.append("AzureDocumentIntelligenceClient")
    __all__.append("DocumentIntelligenceClientError")
except ImportError:
    raise
