
from judgeval.data import CustomExample
from judgeval import JudgmentClient
from qodo_scorer import QodoScorer

judgment = JudgmentClient()

custom_example = CustomExample(
    code="print('Hello, world!')",
    original_code="print('Hello, world!')",
)

qodo_scorer = QodoScorer()
results = judgment.run_evaluation(
    examples=[custom_example],
    scorers=[qodo_scorer],
    model="gpt-4o",
    project_name="QoDoDemo",
    eval_run_name="QoDoDemoRun1",
)

print(f"{results=}")