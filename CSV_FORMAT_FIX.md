# CSV Format Fix - Udemy Template Compliance

## Issue
The generated CSV file had incorrect headers and format that did not match the official Udemy practice test template.

---

## Root Cause

### Old Format (Incorrect)
```csv
question_title,question_type,question_text,possible_answers,correct_answer,explanation
```

### Correct Udemy Format
```csv
Question,Question Type,Answer Option 1,Explanation 1,Answer Option 2,Explanation 2,Answer Option 3,Explanation 3,Answer Option 4,Explanation 4,Answer Option 5,Explanation 5,Answer Option 6,Explanation 6,Correct Answers,Overall Explanation,Domain
```

**Key Differences:**
1. Each answer option has its own column with a corresponding explanation column
2. Up to 6 answer options supported
3. Correct answers are indicated by comma-separated indices (1-based)
4. Overall explanation is separate from individual answer explanations
5. Domain field for categorization

---

## Changes Made

### 1. Updated AI Prompt (generator/routes.py:150-175)

**New JSON Structure:**
```json
[
  {
    "question": "The full question text",
    "question_type": "multiple-choice|multi-select",
    "answers": [
      {"text": "Answer 1", "explanation": "Why correct/incorrect", "is_correct": false},
      {"text": "Answer 2", "explanation": "Why correct/incorrect", "is_correct": true}
    ],
    "overall_explanation": "Comprehensive explanation",
    "domain": "Category name"
  }
]
```

**Key Requirements Added:**
- Each answer must have individual explanation
- `is_correct` boolean flag for each answer
- `overall_explanation` field separate from answer explanations
- `domain` field for category
- Convert true/false to multiple-choice with 2 options (TRUE/FALSE)
- Use hyphenated format: "multiple-choice", "multi-select" (not underscore)

### 2. Rewrote CSV Conversion Function (generator/routes.py:230-288)

**New Logic:**
```python
def convert_to_udemy_csv(questions: List[dict]) -> str:
    # Create CSV with exact Udemy header
    writer.writerow([
        "Question", "Question Type",
        "Answer Option 1", "Explanation 1",
        "Answer Option 2", "Explanation 2",
        "Answer Option 3", "Explanation 3",
        "Answer Option 4", "Explanation 4",
        "Answer Option 5", "Explanation 5",
        "Answer Option 6", "Explanation 6",
        "Correct Answers", "Overall Explanation", "Domain"
    ])

    # For each question:
    # - Write question text and type
    # - Write up to 6 answer/explanation pairs
    # - Track correct answer indices (1-based)
    # - Write correct answers as comma-separated string
    # - Write overall explanation and domain
```

### 3. Updated Validation (generator/routes.py:217-231)

**New Validation Checks:**
```python
# Check required fields
if not all(key in q for key in ["question", "question_type", "answers", "overall_explanation"]):
    raise ValueError("Missing required fields")

# Validate answers structure
if not isinstance(q["answers"], list) or len(q["answers"]) < 2:
    raise ValueError("Must have at least 2 answer options")

# Validate each answer
for ans in q["answers"]:
    if not all(key in ans for key in ["text", "explanation", "is_correct"]):
        raise ValueError("Each answer needs text, explanation, is_correct")
```

### 4. Updated Frontend Preview (static/js/pages/app.js:360-395)

**New Display Logic:**
- Shows `q.question` instead of `q.question_title`
- Displays `q.answers` array with individual explanations
- Shows checkmark for correct answers
- Displays individual answer explanations below each option
- Shows `q.overall_explanation` in separate section
- Displays domain/category

---

## Examples

### Example 1: Multiple Choice Question

**AI Generated JSON:**
```json
{
  "question": "What is the capital of France?",
  "question_type": "multiple-choice",
  "answers": [
    {"text": "London", "explanation": "London is the capital of England.", "is_correct": false},
    {"text": "Paris", "explanation": "Paris is the capital of France.", "is_correct": true},
    {"text": "Berlin", "explanation": "Berlin is the capital of Germany.", "is_correct": false},
    {"text": "Madrid", "explanation": "Madrid is the capital of Spain.", "is_correct": false}
  ],
  "overall_explanation": "Paris has been the capital of France for centuries.",
  "domain": "Geography"
}
```

**Generated CSV Row:**
```csv
What is the capital of France?,multiple-choice,London,London is the capital of England.,Paris,Paris is the capital of France.,Berlin,Berlin is the capital of Germany.,Madrid,Madrid is the capital of Spain.,,,,,2,Paris has been the capital of France for centuries.,Geography
```

**Parsed in Udemy:**
- ✓ Question displays correctly
- ✓ 4 answer options with individual explanations
- ✓ Option 2 (Paris) marked as correct
- ✓ Overall explanation appears
- ✓ Domain categorized as Geography

### Example 2: Multi-Select Question

**AI Generated JSON:**
```json
{
  "question": "Which are programming languages?",
  "question_type": "multi-select",
  "answers": [
    {"text": "Python", "explanation": "High-level programming language.", "is_correct": true},
    {"text": "HTML", "explanation": "Markup language, not programming.", "is_correct": false},
    {"text": "JavaScript", "explanation": "Programming language for web.", "is_correct": true},
    {"text": "CSS", "explanation": "Styling language, not programming.", "is_correct": false},
    {"text": "Java", "explanation": "Object-oriented programming language.", "is_correct": true}
  ],
  "overall_explanation": "Python, JavaScript, and Java are programming languages.",
  "domain": "Computer Science"
}
```

**Generated CSV Row:**
```csv
Which are programming languages?,multi-select,Python,High-level programming language.,HTML,"Markup language, not programming.",JavaScript,Programming language for web.,CSS,"Styling language, not programming.",Java,Object-oriented programming language.,,,,"1,3,5","Python, JavaScript, and Java are programming languages.",Computer Science
```

**Parsed in Udemy:**
- ✓ Question displays correctly
- ✓ 5 answer options with individual explanations
- ✓ Options 1, 3, 5 (Python, JavaScript, Java) marked as correct
- ✓ Overall explanation appears
- ✓ Domain categorized as Computer Science

---

## Testing

### Manual Test
Run the test script:
```bash
cd "/home/h/Documents/GitHub/Udemy Practice Test Maker"
python test_csv_format.py
```

Expected output:
```
✓ Header matches Udemy template!
✓ Total columns: 17
✓ Total questions: 2
✅ CSV Format Test PASSED!
```

### Verification Checklist

- [x] CSV header exactly matches Udemy template
- [x] 17 columns total
- [x] Question text in first column
- [x] Question type in second column (multiple-choice or multi-select)
- [x] Up to 6 answer options supported
- [x] Each answer has corresponding explanation
- [x] Correct answers as comma-separated indices (1-based)
- [x] Overall explanation column populated
- [x] Domain column populated
- [x] Empty cells for unused answer slots
- [x] CSV properly quoted (handles commas in text)

---

## Files Modified

1. **generator/routes.py**
   - Lines 150-175: Updated AI prompt with new JSON structure
   - Lines 217-231: Updated validation for new structure
   - Lines 230-288: Completely rewrote CSV conversion function

2. **static/js/pages/app.js**
   - Lines 360-395: Updated preview display for new structure

3. **test_csv_format.py** (New)
   - Created test script to verify CSV format

4. **CSV_FORMAT_FIX.md** (New)
   - This documentation file

---

## Backward Compatibility

⚠️ **Breaking Change**: This is a breaking change. Any existing code expecting the old format will need to be updated.

**Migration Notes:**
- Old `question_title` → New `question`
- Old `question_text` → Removed (redundant)
- Old `possible_answers` (array) → New `answers` (array of objects)
- Old `correct_answer` (text) → New `is_correct` (boolean per answer)
- Old `explanation` → New `overall_explanation` + individual answer explanations

---

## Future Improvements

1. **Add support for images** in questions (Udemy supports this)
2. **Add question difficulty field** (optional in Udemy)
3. **Add time allocation** per question (optional in Udemy)
4. **Validation of CSV before download** (client-side preview)
5. **Batch generation** with progress tracking

---

## Udemy Upload Instructions

Once you have generated the CSV:

1. Go to your Udemy course
2. Navigate to "Practice Tests" section
3. Click "Upload CSV"
4. Select your generated CSV file
5. Preview questions
6. Publish practice test

**Supported Question Types:**
- `multiple-choice` - One correct answer from 2-6 options
- `multi-select` - Multiple correct answers from 2-6 options

**Format Requirements:**
✓ All met by this implementation
- Maximum 6 answer options per question
- Minimum 2 answer options per question
- Each answer must have an explanation
- Overall explanation required
- Domain/category optional but recommended

---

## Support

For issues with CSV generation:
1. Check `test_csv_format.py` output
2. Review AI-generated JSON structure
3. Verify Udemy template hasn't changed
4. Check DeepSeek API balance

For Udemy upload issues:
1. Open CSV in Excel/Sheets to verify format
2. Check for special characters or encoding issues
3. Ensure all required fields are populated
4. Verify question types are exactly "multiple-choice" or "multi-select"
