import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

def load_data():
    # Load job postings
    jobs_df = pd.read_csv('data/processed/job_postings_clean.csv')
    # Load resumes
    resumes_df = pd.read_csv('data/processed/resumes_text.csv')
    return jobs_df, resumes_df

def preprocess_text(text):
    # Simple preprocessing: lowercase, remove punctuation (can be enhanced)
    import re
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def match_resumes_to_jobs(jobs_df, resumes_df, top_n=5):
    # Combine job descriptions and resume texts
    job_texts = jobs_df['description'].fillna('').apply(preprocess_text)
    resume_texts = resumes_df['text'].fillna('').apply(preprocess_text)

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    all_texts = list(job_texts) + list(resume_texts)
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # Split back
    job_vectors = tfidf_matrix[:len(job_texts)]
    resume_vectors = tfidf_matrix[len(job_texts):]

    # Compute cosine similarity
    similarity_matrix = cosine_similarity(resume_vectors, job_vectors)

    # For each resume, find top matching jobs
    matches = []
    for i, resume in enumerate(resumes_df['filename']):
        similarities = similarity_matrix[i]
        top_indices = similarities.argsort()[-top_n:][::-1]
        top_jobs = jobs_df.iloc[top_indices][['title', 'description']].copy()
        top_jobs['similarity'] = similarities[top_indices]
        top_jobs['resume'] = resume
        matches.append(top_jobs)

    return pd.concat(matches, ignore_index=True)

if __name__ == "__main__":
    jobs_df, resumes_df = load_data()
    matches_df = match_resumes_to_jobs(jobs_df, resumes_df)
    matches_df.to_csv('data/processed/matching_results.csv', index=False)
    print("Matching completed. Results saved to data/processed/matching_results.csv")
    print(matches_df.head())