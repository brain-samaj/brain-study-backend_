from __future__ import annotations


class FlashcardReviewEngine:

    def review(
        self,
        *,
        confidence: int,
    ):

        if confidence >= 5:
            return {
                "next_review_days": 14,
                "difficulty": "easy",
            }

        if confidence >= 3:
            return {
                "next_review_days": 7,
                "difficulty": "medium",
            }

        return {
            "next_review_days": 1,
            "difficulty": "hard",
        }

