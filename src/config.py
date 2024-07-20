import os

class Config:
    BASE_URL = os.getenv("CSFD_BASE_URL", "https://www.csfd.cz")
    HEADERS = {
        "User-agent": os.getenv("CSFD_USER_AGENT", "csfd crawler")
    }
    INTERESTED_SECTIONS = [
        "Nejnavštěvovanější seriály",
        "Nejnavštěvovanější filmy"
    ]
    LOG_LEVEL = os.getenv("CSFD_LOG_LEVEL", "INFO")