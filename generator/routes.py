# generator/routes.py - Practice test generation routes
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import csv
import io
import json
from openai import OpenAI
from anthropic import Anthropic
from auth.routes import get_current_user, supabase_client

from config import (
    AI_MODEL, AI_MAX_TOKENS, AI_TEMPERATURE, AI_PROVIDER,
    DEEPSEEK_BASE_URL, VALIDATION, ERROR_MESSAGES
)
from utils.logging_config import get_logger
from utils.exceptions import ValidationError, GenerationError

generator_router = APIRouter(prefix="/api/generator")

# Setup logging
logger = get_logger("generator")

# Initialize AI clients based on provider
if AI_PROVIDER == "deepseek":
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=DEEPSEEK_BASE_URL
    )
else:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


class GenerateTestRequest(BaseModel):
    """Request model for test generation"""
    working_title: str = Field(..., min_length=1)
    practice_test_title: str = Field(..., min_length=1)
    category: str
    learning_objectives: List[str] = Field(..., min_items=4)
    requirements: str
    target_audience: str
    difficulty_level: str
    num_questions: int = Field(..., ge=1, le=250)
    question_formats: List[str]
    explanation_style: str


def format_explanation_style_prompt(style: str) -> str:
    """Convert explanation style to AI prompt guidance"""
    style_map = {
        "beginner-friendly": "Use simple language, avoid jargon, and explain concepts step-by-step as if teaching a complete beginner.",
        "technical": "Use precise technical terminology and assume familiarity with domain concepts.",
        "very-detailed": "Provide comprehensive, in-depth explanations with multiple examples and edge cases.",
        "short-concise": "Keep explanations brief and to-the-point, 1-2 sentences maximum.",
        "fun-casual": "Use a conversational, friendly tone with occasional humor and relatable analogies.",
        "academic": "Use formal academic language with proper citations of best practices and industry standards."
    }
    return style_map.get(style, style_map["beginner-friendly"])


def format_difficulty_prompt(level: str) -> str:
    """Convert difficulty level to AI prompt guidance"""
    difficulty_map = {
        "beginner": "Create questions suitable for complete beginners. Focus on fundamental concepts, basic terminology, and simple application scenarios.",
        "intermediate": "Create questions for learners with basic knowledge. Include questions about practical application, common use cases, and some problem-solving.",
        "advanced": "Create challenging questions for experienced learners. Include complex scenarios, edge cases, troubleshooting, and optimization topics.",
        "mixed": "Create a balanced mix of beginner (30%), intermediate (50%), and advanced (20%) questions to test learners at all levels."
    }
    return difficulty_map.get(level, difficulty_map["beginner"])


def get_question_type_distribution(formats: List[str], total: int) -> dict:
    """Calculate how many questions of each type to generate"""
    if "mix-all" in formats:
        # Equal distribution if mixing all
        return {
            "multiple_choice": total // 3,
            "multiple_select": total // 3,
            "true_false": total - (2 * (total // 3))
        }

    # Calculate distribution based on selected formats
    types_selected = []
    if "single-choice" in formats:
        types_selected.append("multiple_choice")
    if "multiple-select" in formats:
        types_selected.append("multiple_select")
    if "true-false" in formats:
        types_selected.append("true_false")
    if "scenario-based" in formats:
        types_selected.append("multiple_choice")  # Scenarios are multiple choice

    if not types_selected:
        types_selected = ["multiple_choice"]  # Default

    per_type = total // len(types_selected)
    remainder = total % len(types_selected)

    distribution = {}
    for i, qtype in enumerate(types_selected):
        distribution[qtype] = per_type + (1 if i < remainder else 0)

    return distribution


async def generate_questions_with_ai(request: GenerateTestRequest) -> List[dict]:
    """Generate practice test questions using Claude AI"""

    # Determine question type distribution
    distribution = get_question_type_distribution(request.question_formats, request.num_questions)

    # Build the AI prompt
    prompt = f"""You are an expert educational content creator specializing in creating high-quality Udemy practice test questions.

COURSE DETAILS:
- Course Title: {request.working_title}
- Practice Test: {request.practice_test_title}
- Category: {request.category}
- Target Audience: {request.target_audience}
- Prerequisites: {request.requirements}
- Difficulty Level: {request.difficulty_level}

LEARNING OBJECTIVES:
{chr(10).join(f"- {obj}" for obj in request.learning_objectives)}

TASK:
Generate exactly {request.num_questions} practice test questions for "{request.practice_test_title}".
All questions should be specifically focused on the topics and concepts covered in this particular practice test section.

DIFFICULTY GUIDANCE:
{format_difficulty_prompt(request.difficulty_level)}

EXPLANATION STYLE:
{format_explanation_style_prompt(request.explanation_style)}

QUESTION TYPE DISTRIBUTION:
{json.dumps(distribution, indent=2)}

REQUIREMENTS:
1. Each question MUST directly relate to one or more of the learning objectives
2. Ensure good variety across all learning objectives
3. Questions should be clear, unambiguous, and professionally written
4. For multiple_choice: provide exactly 4 answer options with ONE correct answer
5. For multiple_select: provide 4-6 options with 2-3 correct answers
6. For true_false: provide a clear statement with explanation for both true/false cases
7. Avoid trick questions or overly obvious answers
8. Include {"at least 2 scenario-based questions" if "scenario-based" in request.question_formats else "practical application questions"}
9. Wrong answers should be plausible but clearly incorrect
10. Explanations should help learners understand WHY the answer is correct

OUTPUT FORMAT:
Return a JSON array of question objects with this EXACT structure for Udemy CSV format:
[
  {{
    "question": "The full question text",
    "question_type": "multiple-choice|multi-select",
    "answers": [
      {{"text": "Answer option 1", "explanation": "Why this is correct/incorrect", "is_correct": false}},
      {{"text": "Answer option 2", "explanation": "Why this is correct/incorrect", "is_correct": true}},
      {{"text": "Answer option 3", "explanation": "Why this is correct/incorrect", "is_correct": false}},
      {{"text": "Answer option 4", "explanation": "Why this is correct/incorrect", "is_correct": false}}
    ],
    "overall_explanation": "Overall explanation of the correct answer(s)",
    "domain": "{request.category}"
  }}
]

IMPORTANT NOTES:
- For multiple-choice: exactly 4-6 answer options, ONLY ONE with is_correct=true
- For multi-select: 4-6 answer options, 2-3 with is_correct=true
- For true/false: convert to multiple-choice with 2 options (TRUE and FALSE)
- Each answer option MUST have its own explanation (why it's correct or incorrect)
- overall_explanation should explain the correct answer(s) comprehensively
- Use "multiple-choice" not "multiple_choice", use "multi-select" not "multiple_select"

CRITICAL: Return ONLY the JSON array, no other text or markdown formatting."""

    try:
        logger.info(f"Generating {request.num_questions} questions using {AI_PROVIDER} for course: {request.working_title}")

        # Call AI API based on provider
        if AI_PROVIDER == "deepseek":
            # DeepSeek uses OpenAI-compatible API
            response = client.chat.completions.create(
                model=AI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert educational content creator specializing in creating high-quality Udemy practice test questions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=AI_MAX_TOKENS,
                temperature=AI_TEMPERATURE
            )

            logger.debug(f"DeepSeek response received, tokens used: {response.usage.prompt_tokens + response.usage.completion_tokens}")
            response_text = response.choices[0].message.content.strip()
        else:
            # Claude API
            message = client.messages.create(
                model=AI_MODEL,
                max_tokens=AI_MAX_TOKENS,
                temperature=AI_TEMPERATURE,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            logger.debug(f"Claude response received, tokens used: {message.usage.input_tokens + message.usage.output_tokens}")
            response_text = message.content[0].text.strip()

        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()
        elif response_text.startswith("```"):
            response_text = response_text.replace("```", "").strip()

        questions = json.loads(response_text)

        # Validate structure
        for q in questions:
            if not all(key in q for key in ["question", "question_type", "answers", "overall_explanation"]):
                raise ValueError("Invalid question structure returned by AI. Missing required fields.")

            # Validate answers structure
            if not isinstance(q["answers"], list) or len(q["answers"]) < 2:
                raise ValueError("Each question must have at least 2 answer options")

            for ans in q["answers"]:
                if not all(key in ans for key in ["text", "explanation", "is_correct"]):
                    raise ValueError("Each answer must have text, explanation, and is_correct fields")

        logger.info(f"Successfully validated {len(questions)} questions")
        return questions

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse AI response: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")


async def update_user_question_usage(user_id: str, num_questions: int):
    """Update user's monthly question usage counter"""
    try:
        # Get current usage
        response = supabase_client.table("users").select("monthly_chars_used").eq("id", user_id).execute()

        if not response.data:
            logger.error(f"User {user_id} not found when updating usage")
            return

        current_usage = response.data[0].get("monthly_chars_used", 0)
        new_usage = current_usage + num_questions

        # Update usage
        update_response = supabase_client.table("users").update({
            "monthly_chars_used": new_usage
        }).eq("id", user_id).execute()

        logger.info(f"Updated user {user_id} question usage: {current_usage} -> {new_usage}")

    except Exception as e:
        logger.error(f"Failed to update question usage for user {user_id}: {str(e)}")
        # Don't raise exception - we don't want to fail the request if tracking fails


def convert_to_udemy_csv(questions: List[dict]) -> str:
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


@generator_router.post("/generate")
async def generate_test(request: GenerateTestRequest, current_user: dict = Depends(get_current_user)):
    """Generate practice test questions and return as CSV"""

    # Validate inputs using config constants
    if len(request.learning_objectives) < VALIDATION["min_learning_objectives"]:
        logger.warning(f"Validation failed: Only {len(request.learning_objectives)} objectives provided")
        raise HTTPException(
            status_code=400,
            detail=ERROR_MESSAGES["insufficient_objectives"]
        )

    for obj in request.learning_objectives:
        if len(obj) > VALIDATION["learning_objective_max_length"]:
            logger.warning(f"Validation failed: Objective too long ({len(obj)} chars)")
            raise HTTPException(
                status_code=400,
                detail=f"Each learning objective must be max {VALIDATION['learning_objective_max_length']} characters"
            )

    # Generate questions
    questions = await generate_questions_with_ai(request)

    logger.info(f"Successfully generated {len(questions)} questions for: {request.working_title}")

    # Update user's question usage counter
    await update_user_question_usage(current_user["id"], request.num_questions)

    # Convert to CSV
    csv_content = convert_to_udemy_csv(questions)

    # Create filename
    safe_title = "".join(c for c in request.working_title if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_title = safe_title.replace(' ', '_')
    filename = f"{safe_title}_practice_test.csv"

    logger.info(f"Returning CSV file: {filename}")

    # Return as downloadable file
    return StreamingResponse(
        io.BytesIO(csv_content.encode('utf-8')),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


