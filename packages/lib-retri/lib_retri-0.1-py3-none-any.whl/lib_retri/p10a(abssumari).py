from transformers import pipeline

# Sample input text
text = """
The T5 model is a powerful transformer-based model developed by Google. It treats every NLP problem as a text-to-text problem, 
allowing a single model to be fine-tuned on a wide variety of tasks including summarization, translation, question answering, and classification. 
T5 stands for Text-To-Text Transfer Transformer.
"""

# Use a valid free model like t5-small
summarization_pipeline = pipeline("summarization", model="t5-small", tokenizer="t5-small")

# Add "summarize:" prefix as required by T5
input_text = "summarize: " + text

# Generate summary
summary = summarization_pipeline(input_text, max_length=100, min_length=20, do_sample=False)[0]['summary_text']

# Print summary
print("Abstractive Summary:")
print(summary)
