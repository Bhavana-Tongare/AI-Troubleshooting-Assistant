import json
from sklearn.feature_extraction.text import TfidfVectorizer   #TfidfVectorizer converts text into numerical values.
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path


THRESHOLD = 0.20
BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "knowledge_base.json", "r", encoding="utf-8") as file:
    kb = json.load(file)

    kb = json.load(file)

    # print("Loaded successfully")
    
# Prepare text for searching
documents =[
    entry["issue"] + " " + entry["symptoms"] 
    for entry in kb
]



# Convert knowledge-base text into numbers using TF-IDF
vectorizer = TfidfVectorizer(stop_words="english")
matrix = vectorizer.fit_transform(documents)


# search fuunction
def search(question):

     # convert user question into numbers
    question_vector = vectorizer.transform([question])

    # compare question with  kb entries
    scores = cosine_similarity(question_vector, matrix).flatten()

    # entry with the highest similarity score
    best_index = scores.argmax()


    # highest similarity score
    best_score = scores[best_index].item()

    if best_score < THRESHOLD:
        return None,best_score

    return kb[best_index], best_score

# test the search function 
if __name__ == "__main__":

    test_questions = [
        "Payment API returning HTTP 500 error",
        "database connection failed",
        "user cannot login",
        "user cannot make payment",
        "system lagging",
        "how to install application"
    ]

    for question in test_questions:

        result, score = search(question)
        print("Question: ", question)

        if result is not None:

            print("Matched Issue: ", result["issue"])
            print("Knowledge Base ID:", result["id"])
            print("Similarity Score:", round(score, 2))

        else:
            print("No relevant knowledge base entry found.")
            print("Similarity Score : ", round(score, 2))





