import dspy


class MockLLM(dspy.LM):
    """
    Mock LLM client for DSPy.
    Simulates unpredictable or predictable responses based on provided list.
    """

    def __init__(self, model="mock-model", model_type="chat", responses=None, **kwargs):
        super().__init__(model, model_type=model_type, **kwargs)
        self.responses = responses or []
        self.history = []
        self.default_response = (
            '{"reasoning": "mock reasoning", "answer": "mock answer"}'
        )
        self.kwargs = kwargs

    def __call__(self, prompt=None, messages=None, **kwargs):
        # Record what was asked
        self.history.append({"prompt": prompt, "messages": messages, "kwargs": kwargs})

        # Pop next response or return default
        if self.responses:
            response = self.responses.pop(0)
        else:
            # We can return a relatively valid DSPy output string if it's parsing JSON or similar.
            # But just returning "Mocked Default Response" is fine for most cases.
            response = self.default_response

        return [response]
