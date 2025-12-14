# config.py - Application Configuration and Constants

from typing import Dict, Any

# ==================== TIER CONFIGURATION ====================

TIER_LIMITS: Dict[str, Dict[str, Any]] = {
    "free": {
        "name": "Free",
        "questions_per_month": 20,
        "max_questions_per_test": 20,
        "price_monthly": 0,
        "price_annual": 0,
        "features": [
            "20 questions per month",
            "Test the AI quality",
            "All question formats",
            "All explanation styles",
            "Udemy CSV export",
            "Email support (48h response)"
        ]
    },
    "pro": {
        "name": "Pro",
        "questions_per_month": 2500,
        "max_questions_per_test": 250,
        "price_monthly": 9,
        "price_annual": 90,  # $7.50/month when billed annually
        "features": [
            "2,500 questions per month",
            "Create 3-5 complete courses",
            "Unlimited test downloads",
            "Up to 250 questions per test",
            "Email support (24h response)"
        ]
    },
    "business": {
        "name": "Business",
        "questions_per_month": 7500,
        "max_questions_per_test": 250,
        "price_monthly": 19,
        "price_annual": 190,  # $15.83/month when billed annually
        "features": [
            "7,500 questions per month",
            "Create 10-15 courses per month",
            "Priority generation (faster)",
            "Perfect for agencies & teams",
            "Bulk test creation",
            "Priority email support"
        ]
    }
}

# Helper function to get tier limits
def get_tier_limit(tier: str, key: str, default: Any = None) -> Any:
    """Get a specific limit for a tier"""
    return TIER_LIMITS.get(tier, {}).get(key, default)

def get_monthly_question_limit(tier: str) -> int:
    """Get monthly question limit for a tier"""
    return get_tier_limit(tier, "questions_per_month", 20)

def get_max_questions_per_test(tier: str) -> int:
    """Get max questions per test for a tier"""
    return get_tier_limit(tier, "max_questions_per_test", 20)


# ==================== STRIPE CONFIGURATION ====================

STRIPE_PRICE_IDS = {
    "pro_monthly": "price_xxx",  # Replace with actual Stripe price ID
    "pro_annual": "price_xxx",   # Replace with actual Stripe price ID
    "business_monthly": "price_xxx",  # Replace with actual Stripe price ID
    "business_annual": "price_xxx"    # Replace with actual Stripe price ID
}


# ==================== COURSE CATEGORIES ====================

COURSE_CATEGORIES = [
    "Development",
    "Business",
    "Finance & Accounting",
    "IT & Software",
    "Office Productivity",
    "Personal Development",
    "Design",
    "Marketing",
    "Health & Fitness",
    "Music",
    "Teaching & Academics",
    "Photography & Video",
    "Lifestyle"
]


# ==================== QUESTION TYPES ====================

QUESTION_TYPES = {
    "single-choice": {
        "name": "Single Choice (Multiple Choice)",
        "description": "One correct answer from 4 options",
        "udemy_type": "multiple_choice"
    },
    "multiple-select": {
        "name": "Multiple Select",
        "description": "Multiple correct answers from 4-6 options",
        "udemy_type": "multiple_select"
    },
    "true-false": {
        "name": "True/False",
        "description": "Binary true or false questions",
        "udemy_type": "true_false"
    },
    "scenario-based": {
        "name": "Scenario-Based",
        "description": "Real-world scenario questions",
        "udemy_type": "multiple_choice"  # Scenarios are multiple choice
    }
}


# ==================== DIFFICULTY LEVELS ====================

DIFFICULTY_LEVELS = {
    "beginner": "Beginner - Fundamental concepts and basic terminology",
    "intermediate": "Intermediate - Practical application and problem-solving",
    "advanced": "Advanced - Complex scenarios and edge cases",
    "mixed": "Mixed - Balanced mix of all levels (30% beginner, 50% intermediate, 20% advanced)"
}


# ==================== EXPLANATION STYLES ====================

EXPLANATION_STYLES = {
    "beginner-friendly": "Beginner-Friendly - Simple language, step-by-step explanations",
    "technical": "Technical - Precise terminology, assumes domain knowledge",
    "very-detailed": "Very Detailed - Comprehensive with multiple examples",
    "short-concise": "Short & Concise - Brief, 1-2 sentences maximum",
    "fun-casual": "Fun & Casual - Conversational tone with humor",
    "academic": "Academic - Formal language with best practices"
}


# ==================== API CONFIGURATION ====================

# AI Provider Selection (options: "claude", "deepseek")
AI_PROVIDER = "deepseek"

# Claude Model Configuration
CLAUDE_MODEL = "claude-3-5-sonnet-20241022"
CLAUDE_MAX_TOKENS = 16000

# DeepSeek Model Configuration
DEEPSEEK_MODEL = "deepseek-chat"
DEEPSEEK_MAX_TOKENS = 8000
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# Shared AI Configuration
AI_TEMPERATURE = 0.7

# Dynamic configuration based on provider
AI_MODEL = DEEPSEEK_MODEL if AI_PROVIDER == "deepseek" else CLAUDE_MODEL
AI_MAX_TOKENS = DEEPSEEK_MAX_TOKENS if AI_PROVIDER == "deepseek" else CLAUDE_MAX_TOKENS

# Rate Limiting
RATE_LIMIT_REQUESTS_PER_MINUTE = {
    "free": 5,
    "pro": 20,
    "business": 50
}


# ==================== VALIDATION CONSTRAINTS ====================

VALIDATION = {
    "min_learning_objectives": 4,
    "max_learning_objectives": 10,
    "learning_objective_max_length": 160,
    "working_title_max_length": 100,
    "min_questions": 1,
    "max_questions": 100  # Overall maximum, can be limited by tier
}


# ==================== APPLICATION METADATA ====================

APP_NAME = "PracticeTestBulk"
APP_DESCRIPTION = "Generate professional Udemy practice tests in bulk with AI"
APP_VERSION = "1.0.0"
COMPANY_NAME = "PracticeTestBulk"
POWERED_BY = "DeepSeek AI" if AI_PROVIDER == "deepseek" else "Claude AI"


# ==================== ERROR MESSAGES ====================

ERROR_MESSAGES = {
    "auth_required": "Authentication required. Please log in.",
    "invalid_credentials": "Invalid email or password.",
    "email_not_verified": "Please verify your email before logging in.",
    "usage_limit_reached": "You've reached your monthly question limit. Please upgrade your plan.",
    "invalid_tier": "Invalid subscription tier.",
    "payment_failed": "Payment processing failed. Please try again.",
    "generation_failed": "Question generation failed. Please try again.",
    "insufficient_objectives": f"Please provide at least {VALIDATION['min_learning_objectives']} learning objectives.",
    "invalid_question_format": "Invalid question format selected."
}


# ==================== SUCCESS MESSAGES ====================

SUCCESS_MESSAGES = {
    "registration_success": "Registration successful! Please check your email to verify your account.",
    "login_success": "Login successful! Redirecting...",
    "generation_success": "Questions generated successfully!",
    "download_success": "CSV file downloaded successfully!",
    "upgrade_success": "Subscription upgraded successfully!",
    "email_verified": "Email verified successfully! You can now log in."
}
