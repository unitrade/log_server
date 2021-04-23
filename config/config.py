class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    host = "127.0.0.1"
    port = 8000

    @property
    def SERVER_NAME(self):
        return f"{self.host}:{self.port}"


class ProductionConfig(Config):
    """Production configuration"""
    port = 8001


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    port = 8002


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    port = 8003
