# src/app/security/logging.py
import logging
import re


class SecurityFormatter(logging.Formatter):
    SENSITIVE_PATTERNS = {
        "password": re.compile(r'("password"\s*:\s*)"[^"]*"', re.IGNORECASE),
        "token": re.compile(r'("token"\s*:\s*)"[^"]*"', re.IGNORECASE),
    }

    def format(self, record):
        message = super().format(record)
        return self.mask_sensitive_data(message)

    def mask_sensitive_data(self, message: str) -> str:
        for pattern in self.SENSITIVE_PATTERNS.values():
            message = pattern.sub(r'\1"***MASKED***"', message)
        return message
