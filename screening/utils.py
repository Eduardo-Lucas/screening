import os
from pdfminer.high_level import extract_text

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_resume_text(file_path):
    if os.path.exists(file_path):
        text = extract_text(file_path)
        return text
    return ""


def calculate_similarity(job_description, resume_texts):
    """
    Calculate cosine similarity between the job description and resumes.
    """
    documents = [job_description] + resume_texts
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    return cosine_similarities
