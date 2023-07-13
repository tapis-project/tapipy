from tapis import Tapis


class TapisRunner:
    def __init__(self):
        # Instantiate the tapis client
        self._client = Tapis(
            base_url=self.env.get("TAPIS_BASE_URL"),
            username=self.env.get("TAPIS_USERNAME"),
            password=self.env.get("TAPIS_PASSWORD")
        )
        self._client.get_tokens()

    def submit(self, request: dict):
        print("REQUEST", request)
        # self._client.workflows.submit(**request)

    class Config:
        prompt_missing = False
        env = {
            "TAPIS_BASE_URL": {"type": str},
            "TAPIS_USERNAME": {"type": str},
            "TAPIS_PASSWORD": {"type": str, "secret": True}
        }