from kmodels.models import CoreModel
from pydantic import ConfigDict


class Command(CoreModel):
    model_config = ConfigDict(frozen=True)
