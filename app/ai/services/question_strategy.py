from __future__ import annotations


class QuestionStrategy:

    """
    Determines HOW the AI should generate questions
    based on the uploaded material.

    This prevents using one generic prompt
    for every university subject.
    """

    def build_strategy(
        self,
        analysis: dict,
    ) -> dict:

        subject = analysis.get(
            "Subject",
            "",
        ).lower()

        strategy = {
            "question_style": [],
            "requires_formula": False,
            "requires_calculation": False,
            "requires_case_study": False,
            "requires_definition": False,
            "requires_diagram": False,
            "requires_proof": False,
            "requires_code": False,
            "requires_worked_examples": False,
        }

        ###################################################
        # PHYSICS
        ###################################################

        if "physics" in subject:

            strategy["requires_formula"] = True
            strategy["requires_calculation"] = True
            strategy["requires_worked_examples"] = True

            strategy["question_style"] = [

                "conceptual",

                "numerical",

                "application",

                "real-life",

            ]

        ###################################################
        # MATHEMATICS
        ###################################################

        elif "mathematics" in subject:

            strategy["requires_formula"] = True

            strategy["requires_calculation"] = True

            strategy["requires_worked_examples"] = True

            strategy["question_style"] = [

                "problem-solving",

                "proof",

                "simplification",

                "derivation",

            ]

        ###################################################
        # CHEMISTRY
        ###################################################

        elif "chemistry" in subject:

            strategy["requires_formula"] = True

            strategy["requires_calculation"] = True

            strategy["requires_diagram"] = True

            strategy["question_style"] = [

                "equation",

                "mechanism",

                "calculation",

                "laboratory",

            ]

        ###################################################
        # BIOLOGY
        ###################################################

        elif "biology" in subject:

            strategy["requires_diagram"] = True

            strategy["requires_definition"] = True

            strategy["question_style"] = [

                "label",

                "process",

                "diagram",

                "comparison",

            ]

        ###################################################
        # ACCOUNTING
        ###################################################

        elif "accounting" in subject:

            strategy["requires_calculation"] = True

            strategy["requires_worked_examples"] = True

            strategy["question_style"] = [

                "journal",

                "ledger",

                "financial statement",

                "adjustment",

            ]

        ###################################################
        # LAW
        ###################################################

        elif "law" in subject:

            strategy["requires_case_study"] = True

            strategy["question_style"] = [

                "case analysis",

                "legal principle",

                "precedent",

                "application",

            ]

        ###################################################
        # COMPUTER SCIENCE
        ###################################################

        elif "computer" in subject:

            strategy["requires_code"] = True

            strategy["question_style"] = [

                "algorithm",

                "coding",

                "debugging",

                "analysis",

            ]

        ###################################################
        # DEFAULT
        ###################################################

        else:

            strategy["requires_definition"] = True

            strategy["question_style"] = [

                "definition",

                "explanation",

                "application",

            ]

        return strategy

    ###################################################
    # DIFFICULTY DISTRIBUTION
    ###################################################

    def difficulty_distribution(
        self,
        total_questions: int,
        difficulty: str,
    ) -> dict:

        difficulty = difficulty.lower()

        if difficulty == "easy":

            return {
                "easy": total_questions,
                "medium": 0,
                "hard": 0,
            }

        if difficulty == "medium":

            return {
                "easy": max(1, int(total_questions * 0.20)),
                "medium": max(1, int(total_questions * 0.60)),
                "hard": total_questions
                - max(1, int(total_questions * 0.20))
                - max(1, int(total_questions * 0.60)),
            }

        if difficulty == "hard":

            return {
                "easy": 0,
                "medium": max(1, int(total_questions * 0.30)),
                "hard": total_questions
                - max(1, int(total_questions * 0.30)),
            }

        return {
            "easy": max(1, int(total_questions * 0.30)),
            "medium": max(1, int(total_questions * 0.40)),
            "hard": total_questions
            - max(1, int(total_questions * 0.30))
            - max(1, int(total_questions * 0.40)),
        }


    ###################################################
    # BLOOM'S TAXONOMY
    ###################################################

    def blooms_levels(
        self,
    ) -> list[str]:

        return [

            "Remember",

            "Understand",

            "Apply",

            "Analyse",

            "Evaluate",

            "Create",

        ]


    ###################################################
    # UNIVERSITY LEVEL
    ###################################################

    def university_level(
        self,
        education_level: str,
    ) -> dict:

        level = education_level.lower()

        if "100" in level:

            return {
                "depth": "introductory",
                "calculation_complexity": "low",
                "critical_thinking": "low",
            }

        if "200" in level:

            return {
                "depth": "basic",
                "calculation_complexity": "medium",
                "critical_thinking": "medium",
            }

        if "300" in level:

            return {
                "depth": "intermediate",
                "calculation_complexity": "medium",
                "critical_thinking": "high",
            }

        if "400" in level:

            return {
                "depth": "advanced",
                "calculation_complexity": "high",
                "critical_thinking": "high",
            }

        if "500" in level:

            return {
                "depth": "expert",
                "calculation_complexity": "very_high",
                "critical_thinking": "very_high",
            }

        return {
            "depth": "adaptive",
            "calculation_complexity": "adaptive",
            "critical_thinking": "adaptive",
        }


    ###################################################
    # QUESTION MIX
    ###################################################

    def question_mix(
        self,
        strategy: dict,
    ) -> list[str]:

        mix = []

        if strategy["requires_definition"]:
            mix.append("definition")

        if strategy["requires_formula"]:
            mix.append("formula")

        if strategy["requires_calculation"]:
            mix.append("calculation")

        if strategy["requires_worked_examples"]:
            mix.append("worked_example")

        if strategy["requires_case_study"]:
            mix.append("case_study")

        if strategy["requires_diagram"]:
            mix.append("diagram")

        if strategy["requires_proof"]:
            mix.append("proof")

        if strategy["requires_code"]:
            mix.append("coding")

        mix.extend(

            strategy["question_style"]

        )

        return list(

            dict.fromkeys(mix)

        )


    ###################################################
    # TOPIC WEIGHTING
    ###################################################

    def topic_distribution(
        self,
        topics: list[str],
        total_questions: int,
    ) -> dict[str, int]:
        """
        Distribute questions evenly across all detected topics.

        Example

        4 Topics
        20 Questions

        Topic A -> 5
        Topic B -> 5
        Topic C -> 5
        Topic D -> 5
        """

        if not topics:
            return {}

        distribution: dict[str, int] = {}

        base = total_questions // len(topics)

        remainder = total_questions % len(topics)

        for topic in topics:
            distribution[topic] = base

        index = 0

        while remainder > 0:
            topic = topics[index]

            distribution[topic] += 1

            remainder -= 1

            index += 1

            if index >= len(topics):
                index = 0

        return distribution


    ###################################################
    # REMOVE DUPLICATE QUESTIONS
    ###################################################

    def remove_duplicates(
        self,
        questions: list[dict],
    ) -> list[dict]:

        seen: set[str] = set()

        unique: list[dict] = []

        for question in questions:

            text = (
                question.get("question", "")
                .strip()
                .lower()
            )

            if text in seen:
                continue

            seen.add(text)

            unique.append(question)

        return unique


    ###################################################
    # FINAL STRATEGY
    ###################################################

    def build_generation_plan(
        self,
        *,
        analysis: dict,
        education_level: str,
        total_questions: int,
        difficulty: str,
    ) -> dict:

        strategy = self.build_strategy(
            analysis,
        )

        plan = {
            "subject": analysis.get("Subject"),
            "main_topic": analysis.get("Main Topic"),
            "sub_topics": analysis.get(
                "Sub Topics",
                [],
            ),
            "strategy": strategy,
            "difficulty_distribution": self.difficulty_distribution(
                total_questions,
                difficulty,
            ),
            "blooms_levels": self.blooms_levels(),
            "university_level": self.university_level(
                education_level,
            ),
            "question_mix": self.question_mix(
                strategy,
            ),
            "topic_distribution": self.topic_distribution(
                analysis.get("Sub Topics", []),
                total_questions,
            ),
        }

        return plan
