class TFIDFModel:

    """
    TF-IDF Model Container
    """

    def __init__(self):

        self.vocabulary = []
        self.document_frequency = {}
        self.vectors = []

    def set_vocabulary(self, vocabulary):

        self.vocabulary = vocabulary

    def set_document_frequency(self, df):

        self.document_frequency = df

    def set_vectors(self, vectors):

        self.vectors = vectors

    def summary(self):

        print("=" * 30)
        print("TF-IDF MODEL")
        print("=" * 30)

        print(
            f"Vocabulary Size: "
            f"{len(self.vocabulary)}"
        )

        print(
            f"Vector Count: "
            f"{len(self.vectors)}"
        )