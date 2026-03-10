import os


class Settings:
    def __init__(self):
        self.LIVERAMP_ORG_ID = os.getenv("DEFAULT_LR_ORG_ID")
        self.LR_CLIENT_ID = os.getenv("LR_CLIENT_ID")
        self.LR_CLIENT_SECRET = os.getenv("LR_CLIENT_SECRET")

        if not self.LIVERAMP_ORG_ID:
            raise RuntimeError("DEFAULT_LR_ORG_ID must be set in environment")

        if not self.LR_CLIENT_ID:
            raise RuntimeError("LR_CLIENT_ID must be set in environment")

        if not self.LR_CLIENT_SECRET:
            raise RuntimeError("LR_CLIENT_SECRET must be set in environment")


settings = Settings()
