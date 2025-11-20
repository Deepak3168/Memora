from typing import ClassVar
from datetime import datetime
from .entity import EntityNode
from neontology import BaseRelationship


class BaseRelation(BaseRelationship):
    __relationshiptype__: ClassVar[str] = "RELATION"

    source: EntityNode
    target: EntityNode
    created_at: datetime = datetime.utcnow()
    last_updated: datetime = datetime.utcnow()


# ---------------------------------------------------
# A. STRUCTURAL RELATIONS
# ---------------------------------------------------

class HAS_CATEGORY(BaseRelation):
    __relationshiptype__ = "HAS_CATEGORY"


class BELONGS_TO(BaseRelation):
    __relationshiptype__ = "BELONGS_TO"


class OWNS(BaseRelation):
    __relationshiptype__ = "OWNS"


# ---------------------------------------------------
# B. SEMANTIC RELATIONS
# ---------------------------------------------------

class USES(BaseRelation):
    __relationshiptype__ = "USES"


class REQUIRES(BaseRelation):
    __relationshiptype__ = "REQUIRES"


class RELATED_TO(BaseRelation):
    __relationshiptype__ = "RELATED_TO"


class PART_OF(BaseRelation):
    __relationshiptype__ = "PART_OF"


class DERIVED_FROM(BaseRelation):
    __relationshiptype__ = "DERIVED_FROM"


class MENTIONS(BaseRelation):
    __relationshiptype__ = "MENTIONS"


# ---------------------------------------------------
# C. OPTIONAL / USER–PROJECT RELATIONS
# ---------------------------------------------------

class WORKS_ON(BaseRelation):
    __relationshiptype__ = "WORKS_ON"


class LEARNED(BaseRelation):
    __relationshiptype__ = "LEARNED"


class INTERESTED_IN(BaseRelation):
    __relationshiptype__ = "INTERESTED_IN"
