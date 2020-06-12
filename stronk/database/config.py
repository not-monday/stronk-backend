import os


class Config(object):
    """Represents a database configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(object):
    """Represents a database configuration for testing."""
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
