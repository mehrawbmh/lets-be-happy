from configs.settings import Settings

#TODO: make it singleton
class MongoClient:
    """
    Mongo DB client and connection
    """

    async def get_client(self):
        username = getattr(Settings, "MONGO_USERNAME", None)
        password = getattr(Settings, "MONGO_PASSWORD", None)
        host_name = getattr(Settings, "MONGO_HOST", "")
        port = getattr(Settings, "MONGO_PORT", "")
        if username and password:
            auth_key = username + ":" + password
            address = host_name + ":" + port
