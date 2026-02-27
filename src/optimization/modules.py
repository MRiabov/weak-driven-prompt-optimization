import dspy

class QASignature(dspy.Signature):
    """
    Answers a question based on the provided context or knowledge.
    """
    question = dspy.InputField(desc="The question to be answered.")
    answer = dspy.OutputField(desc="The concise and accurate answer.")

class QAModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate_answer = dspy.ChainOfThought(QASignature)

    def forward(self, question):
        return self.generate_answer(question=question)
