from pydantic import BaseModel

class MessageAdditionalChecksType(BaseModel):
    remembrance: bool
    personalMessage: bool
    specialPhrases: bool
    futureMessage: bool

class MessageType(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    telegram: str
    formRole: str
    songFor: str
    heroName: str
    heroOrigin: str
    heroItem: str
    job: str
    equipment: str
    motivation: str
    comrades: str
    moments: str
    words: str
    additionalChecks: MessageAdditionalChecksType
    remembranceText: str
    personalMessageText: str
    specialPhrasesText: str
    futureMessageText: str
    otherText: str
    planName: str