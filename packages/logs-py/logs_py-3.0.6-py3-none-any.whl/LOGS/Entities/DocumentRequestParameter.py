from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Interfaces.IProjectBased import IProjectBasedRequest


@dataclass
class DocumentRequestParameter(EntityRequestParameter, IProjectBasedRequest):
    name: Optional[str] = None
    creationDate: Optional[datetime] = None
    publicationTypes: Optional[List[int]] = None
    doi: Optional[str] = None
    authorIds: Optional[List[int]] = None
    datasetIds: Optional[List[int]] = None
    documentIds: Optional[List[int]] = None
    sampleIds: Optional[List[int]] = None
    organizationIds: Optional[List[int]] = None
