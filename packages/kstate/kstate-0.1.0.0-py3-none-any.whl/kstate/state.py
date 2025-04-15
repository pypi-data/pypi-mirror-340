from kmodels.models import CoreModel
from pydantic import ConfigDict


class State(CoreModel):
    model_config = ConfigDict(frozen=True)
