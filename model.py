from pydantic import BaseModel,Field

class Speech_Analysis(BaseModel):
    tense_errors: list[str]=Field(description="list the tense errors")
    article_errors: list[str]=Field(description="list all the article error")
    subject_verb_errors:list[str]=Field(description="subject verb agreement errors")
    filler_words: list[str]=Field(description="Detected Filler words")
    fluency_score:int=Field(description="Score out of 10")
    improved_version:str=Field(description="Better polished version of the speech")

