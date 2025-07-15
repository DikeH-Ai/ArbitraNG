from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
# SCRAPER ENGINE UTILS
# CREATE PRODUCT CLUSTERS USING SBERT


# Lightly preprocess product titles


def preprocess_title(title: str):
    # Remove promotional stopwords
    promotional_stopwords = [
        "original", "authentic", "genuine", "branded", "premium", "high quality", "top quality", "best",
        "oem", "luxury", "grade a", "hq", "standard", "durable", "super",
        "cheap", "discount", "offer", "promo", "clearance", "bargain", "hot sale", "deal", "special",
        "lowest price", "affordable", "value", "price slash", "free",
        "new", "brand new", "factory sealed", "sealed", "with box", "no box", "pack of", "bundle", "set",
        "kit", "single", "piece", "unit",
        "fast delivery", "express", "24hrs", "same day", "next day", "instant", "ready stock", "in stock",
        "available now", "limited stock", "free shipping", "free delivery",
        "size", "color", "variant", "version", "model", "edition", "gen", "type", "capacity", "option",
        "for", "with", "and", "plus", "by", "from", "compatible", "suitable", "support", "use", "ideal",
        "uk used", "london used", "dubai used", "tokunbo", "naija", "imported", "direct", "naija stock",
        "working perfectly", "clean"
    ]
    title = ' '.join([word for word in title.split()
                     if word.lower() not in promotional_stopwords])
    # Remove extra spaces
    title = ' '.join(title.split())
    return title.lower()

# Convert sentence to vector embeddings


model = SentenceTransformer("all-MiniLM-L6-v2")


def titles_to_vectors(model: SentenceTransformer, title: str):
    return model.encode(title)


# compare againt product embedding
