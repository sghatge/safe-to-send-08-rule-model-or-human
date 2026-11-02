"""Rule, model or human? Triage CRM ops tasks before you throw AI at them.

Each task is scored on four questions. The answer decides who should own it:
deterministic code, a language model, or an accountable person.
Standard library only.
"""
import json
import sys

QUESTIONS = {
    "fixed_answer": "Is there one correct answer you could write as a rule?",
    "needs_language": "Does it need reading or writing natural language?",
    "needs_judgement": "Does it need judgement, taste or context nobody wrote down?",
    "accountable": "Would someone have to answer for it to a regulator, client or boss?",
}


def triage(task):
    a = task["answers"]
    if a["accountable"] and a["needs_judgement"]:
        owner, why = "human", "judgement plus accountability: a person decides, tools assist"
    elif a["fixed_answer"] and not a["needs_language"]:
        owner, why = "rule", "deterministic: code is cheaper, faster and auditable"
    elif a["fixed_answer"] and a["needs_language"]:
        owner, why = "rule + model", "rule decides, model explains or drafts"
    elif a["needs_language"]:
        owner, why = "model", "language task with no single right answer"
    else:
        owner, why = "human", "unclear: start with a person and write down what they do"
    if owner in ("model", "rule + model") and a["accountable"]:
        why += "; a human approves before it leaves the team"
    return owner, why


def main(path):
    with open(path, encoding="utf-8") as fh:
        tasks = json.load(fh)
    tally = {}
    for t in tasks:
        owner, why = triage(t)
        tally[owner] = tally.get(owner, 0) + 1
        print(f"{owner:<13} {t['task']}\n{'':<13} {why}")
    print("\n" + " | ".join(f"{k}: {v}" for k, v in sorted(tally.items())))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "examples/crm_ops_tasks.json")
