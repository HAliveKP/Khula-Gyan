"""Check that the configured multilingual embedding model handles Nepali and English."""

from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-m3"
EXAMPLES = [
    "सवारी चालक अनुमतिपत्र नवीकरण कसरी गर्ने?",
    "नवीकरणका लागि कुन कागजात चाहिन्छ?",
    "मेरो लाइसेन्सको म्याद सकिएको छ, अब के गर्ने?",
    "नजिकको यातायात कार्यालय कहाँ छ?",
    "शुल्क र जरिवाना कहाँ जाँच गर्न सकिन्छ?",
    "How do I renew my driving license?",
    "Which documents are required for renewal?",
    "My license has expired. What should I do next?",
    "Where can I find the nearest transport office?",
    "Where can I verify the current renewal fee?",
]


def main() -> None:
    print(f"Loading {MODEL_NAME}. The first run downloads the model.")
    model = SentenceTransformer(MODEL_NAME)
    vectors = model.encode(EXAMPLES, normalize_embeddings=True)

    if len(vectors) != len(EXAMPLES):
        raise RuntimeError(f"Expected {len(EXAMPLES)} vectors; got {len(vectors)}")
    if vectors.shape[1] == 0:
        raise RuntimeError("The model returned empty vectors")

    print(
        f"Embedding smoke check passed: {len(vectors)} examples "
        f"(5 Nepali + 5 English), vector size {vectors.shape[1]}"
    )


if __name__ == "__main__":
    main()
