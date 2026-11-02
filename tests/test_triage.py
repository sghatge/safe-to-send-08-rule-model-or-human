import unittest

from triage import triage


def t(f, l, j, a):
    return {"answers": {"fixed_answer": f, "needs_language": l, "needs_judgement": j, "accountable": a}}


class TriageTest(unittest.TestCase):
    def test_deterministic_check_is_a_rule(self):
        self.assertEqual(triage(t(True, False, False, True))[0], "rule")

    def test_explanation_is_rule_plus_model(self):
        self.assertEqual(triage(t(True, True, False, False))[0], "rule + model")

    def test_judgement_with_accountability_is_human(self):
        self.assertEqual(triage(t(False, False, True, True))[0], "human")

    def test_creative_language_is_model(self):
        self.assertEqual(triage(t(False, True, False, False))[0], "model")

    def test_accountable_model_output_needs_approval(self):
        self.assertIn("human approves", triage(t(True, True, False, True))[1])


if __name__ == "__main__":
    unittest.main()
