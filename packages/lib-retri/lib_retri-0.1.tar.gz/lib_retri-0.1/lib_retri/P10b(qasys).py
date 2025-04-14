from transformers import pipeline

# Load the pre-trained question-answering model
qa_pipeline = pipeline("question-answering")

# Sample text passage (context)
context = """
The Pyramids of Egypt are one of the world's most iconic archaeological sites. They were built 
as tombs for pharaohs and queens of ancient Egypt and are located near Cairo, the capital city of Egypt. 
The largest and most famous pyramid is the Great Pyramid of Giza, built for the Pharaoh Khufu. 
It is the only surviving member of the Seven Wonders of the Ancient World. 
The pyramids were constructed during the Old Kingdom period, around 2580-2560 BCE.
"""

# Example questions
questions = [
    "What were the Pyramids of Egypt built for?",
    "Where are the Pyramids of Egypt located?",
    "Who built the Great Pyramid of Giza?",
    "When were the pyramids constructed?"
]

# Answer the questions
for question in questions:
    result = qa_pipeline(question=question, context=context)
    print(f"Question: {question}")
    print(f"Answer: {result['answer']}\n")
