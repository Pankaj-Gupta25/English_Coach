import os
import whisper
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from model import Speech_Analysis
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

# from there we will generate the transcript of the audio
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

model = whisper.load_model("base")
result = model.transcribe("audio1.aac")
# speech ="""Today is holi and its the festival of colours every one play it with joy but there are many
#              toxic elements also who try to spoil the joy out of it."""
speech=result['text']
# langchian work
# print(speech)
llm=ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="openai/gpt-oss-120b",
    temperature=0.3
)

parser=PydanticOutputParser(pydantic_object=Speech_Analysis)

prompt=ChatPromptTemplate.from_template("""

You are an English speaking coach and there is a 2 way communication going on so you need to tell the imporevment possible but don't 
go to technical as if you will tell about the proverbs and verbs it is possible the sudent will get boared just tell them you are wrong
here and it could have been inproved                                                                            

Student speech:
{speech}

Tasks:
1. Identify tense errors
2. Identify article errors
3. Identify subject-verb agreement errors
4. Detect filler words (um, uh, like, you know)
5. Give fluency score out of 10
6. Rewrite the speech in better English

{format_instruction}
                                        
The text which you are getting is a transcript of the voice so try to polish in that way since if you are going to be technical 
    then the student might not understand                                                                   
 """)

chain=prompt | llm

responce=chain.invoke({
    "speech":speech,
    "format_instruction":parser.get_format_instructions()
})

parsed_output=parser.parse(responce.content)

print("fluency score is : ",parsed_output.fluency_score)
print(parsed_output.improved_version)

print(responce.content)