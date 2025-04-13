
from judgeval.data import Example
from judgeval.common.tracer import Tracer, wrap
from judgeval.scorers import JudgevalScorer, AnswerCorrectnessScorer
from judgeval import JudgmentClient
from openai import OpenAI, AsyncOpenAI
import os

client = OpenAI()
async_client = AsyncOpenAI()


class QodoScorer(JudgevalScorer):

    def __init__(self,
                 threshold=0.5,
                 score_type="CodeReviewScorer",
                 include_reason=True,
                 async_mode=True,
                 strict_mode=False,
                 verbose_mode=True):
        super().__init__(
            threshold=threshold,
            score_type=score_type,
            include_reason=include_reason,
            async_mode=async_mode,
            strict_mode=strict_mode,
            verbose_mode=verbose_mode)

    def score_example(self, example: Example) -> float:
        """
        Score the trace based on the code review criteria.
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a QoDo reviewer. You will be given CODE, a PR_REQUEST and QoDo's improved summary of the PR_REQUEST as well as its review of the PR_REQUEST given as PR_QUALITY. Your job is to review the CODE and PR_REQUEST and determine how factually accurate and thorough QoDo is. Give reasoning for why or why not you think the QoDo's review if accurate and thorough."},
                {"role": "user", "content": f"INPUT: {example.input}, CONTEXT: {example.context}, QoDo's REViEW: {example.actual_output}"},
            ],
        )
        self.reason = response.choices[0].message.content

        score_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system",
                    "content": "You are a judge, you will be given a review of the performance of Qodo (a code review tool) on the accuracy and thoroughness of its review of a PR_REQUEST given as PR_QUALITY. Your job is to give a score from 0 to 1 on how well Qodo performed based on the REVIEW given to you. Do not output anything except the score."},
                {"role": "user", "content": f"REVIEW: {self.reason}"},
            ],
        )
        self.score = float(score_response.choices[0].message.content)
        return self.score

    async def a_score_example(self, example: Example) -> float:
        """
        Score the trace based on the code review criteria.
        """
        # In this case, the async implementation is the same as the sync one
        # In a real scenario, you might want to use async APIs for better performance
        response = await async_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a QoDo reviewer. You will be given CODE, a PR_REQUEST and QoDo's improved summary of the PR_REQUEST as well as its review of the PR_REQUEST given as PR_QUALITY. Your job is to review the CODE and PR_REQUEST and determine how factually accurate and thorough QoDo is. Give reasoning for why or why not you think the QoDo's review if accurate and thorough."},
                {"role": "user", "content": f"INPUT: {example.input}, CONTEXT: {example.context}, QoDo's REViEW: {example.actual_output}"},
            ],
        )
        self.score = 1.0
        return self.score_example(example)

    def _success_check(self):
        if self.error is not None:
            return False
        return self.score >= self.threshold

    @property
    def __name__(self):
        return "Qodo Scorer"
