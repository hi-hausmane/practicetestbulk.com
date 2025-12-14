#!/usr/bin/env python3
"""
Test script to verify CSV generation matches Udemy template format
"""
import csv
import io
import sys

# Mock question data in the new format
mock_questions = [
    {
        "question": "What is the capital of France?",
        "question_type": "multiple-choice",
        "answers": [
            {"text": "London", "explanation": "London is the capital of England, not France.", "is_correct": False},
            {"text": "Paris", "explanation": "Paris is indeed the capital of France.", "is_correct": True},
            {"text": "Berlin", "explanation": "Berlin is the capital of Germany.", "is_correct": False},
            {"text": "Madrid", "explanation": "Madrid is the capital of Spain.", "is_correct": False}
        ],
        "overall_explanation": "Paris has been the capital of France since ancient times and is known for landmarks like the Eiffel Tower.",
        "domain": "Geography"
    },
    {
        "question": "Which of the following are programming languages?",
        "question_type": "multi-select",
        "answers": [
            {"text": "Python", "explanation": "Python is a popular high-level programming language.", "is_correct": True},
            {"text": "HTML", "explanation": "HTML is a markup language, not a programming language.", "is_correct": False},
            {"text": "JavaScript", "explanation": "JavaScript is a programming language used for web development.", "is_correct": True},
            {"text": "CSS", "explanation": "CSS is a styling language, not a programming language.", "is_correct": False},
            {"text": "Java", "explanation": "Java is an object-oriented programming language.", "is_correct": True}
        ],
        "overall_explanation": "Python, JavaScript, and Java are programming languages. HTML and CSS are markup/styling languages.",
        "domain": "Computer Science"
    }
]

def convert_to_udemy_csv(questions):
    """Convert questions to Udemy CSV format matching the official template"""
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header matching Udemy template exactly
    writer.writerow([
        "Question",
        "Question Type",
        "Answer Option 1",
        "Explanation 1",
        "Answer Option 2",
        "Explanation 2",
        "Answer Option 3",
        "Explanation 3",
        "Answer Option 4",
        "Explanation 4",
        "Answer Option 5",
        "Explanation 5",
        "Answer Option 6",
        "Explanation 6",
        "Correct Answers",
        "Overall Explanation",
        "Domain"
    ])

    # Write questions
    for q in questions:
        row = [q["question"], q["question_type"]]

        # Process up to 6 answer options
        answers = q.get("answers", [])
        correct_indices = []

        for i in range(6):
            if i < len(answers):
                answer = answers[i]
                row.append(answer["text"])
                row.append(answer["explanation"])
                # Track correct answer indices (1-based for Udemy)
                if answer.get("is_correct", False):
                    correct_indices.append(str(i + 1))
            else:
                # Empty cells for unused answer slots
                row.append("")
                row.append("")

        # Correct answers as comma-separated indices
        row.append(",".join(correct_indices))

        # Overall explanation
        row.append(q.get("overall_explanation", ""))

        # Domain (category)
        row.append(q.get("domain", ""))

        writer.writerow(row)

    return output.getvalue()

def test_csv_format():
    """Test that generated CSV matches expected format"""
    print("Testing CSV Generation...")
    print("=" * 70)

    csv_content = convert_to_udemy_csv(mock_questions)

    print("\nGenerated CSV:")
    print("-" * 70)
    print(csv_content)
    print("-" * 70)

    # Parse the CSV to verify structure
    lines = csv_content.strip().split('\n')
    reader = csv.reader(io.StringIO(csv_content))

    rows = list(reader)
    header = rows[0]

    print("\nHeader Validation:")
    expected_header = [
        "Question", "Question Type",
        "Answer Option 1", "Explanation 1",
        "Answer Option 2", "Explanation 2",
        "Answer Option 3", "Explanation 3",
        "Answer Option 4", "Explanation 4",
        "Answer Option 5", "Explanation 5",
        "Answer Option 6", "Explanation 6",
        "Correct Answers", "Overall Explanation", "Domain"
    ]

    if header == expected_header:
        print("✓ Header matches Udemy template!")
    else:
        print("✗ Header mismatch!")
        print(f"Expected: {expected_header}")
        print(f"Got:      {header}")
        return False

    print(f"\n✓ Total columns: {len(header)}")
    print(f"✓ Total questions: {len(rows) - 1}")

    # Validate question rows
    print("\nQuestion Validation:")
    for i, row in enumerate(rows[1:], 1):
        print(f"\nQuestion {i}:")
        print(f"  Question: {row[0][:50]}...")
        print(f"  Type: {row[1]}")
        print(f"  Correct Answers: {row[14]}")
        print(f"  Domain: {row[16]}")

        # Count non-empty answer options
        answer_count = sum(1 for j in range(2, 14, 2) if row[j])
        print(f"  Answer options: {answer_count}")

    print("\n" + "=" * 70)
    print("✅ CSV Format Test PASSED!")
    return True

if __name__ == "__main__":
    success = test_csv_format()
    sys.exit(0 if success else 1)
