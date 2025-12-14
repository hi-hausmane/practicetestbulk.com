# Udemy Practice Test Generator - Deployment Guide

## Overview

Your Udemy Practice Test Generator is now complete! This SaaS app generates high-quality practice test questions for Udemy courses using AI, and exports them in Udemy's official CSV format.

---

## App Structure

```
.
├── main.py                      # FastAPI application entry point
├── generator/                   # Question generation module
│   ├── __init__.py
│   └── routes.py               # AI generation & CSV export logic
├── auth/                        # User authentication
│   ├── __init__.py
│   └── routes.py
├── billing/                     # Stripe billing integration
│   ├── __init__.py
│   └── routes.py
├── templates/
│   ├── index.html              # Landing page
│   ├── app.html                # Main generator interface
│   ├── login.html
│   ├── register.html
│   └── ...
├── static/                      # CSS, JS, images
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create this)
└── .env.example                 # Environment template
```

---

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI & Uvicorn (web framework)
- Anthropic SDK (AI question generation)
- Supabase (authentication & database)
- Stripe (billing)
- Other utilities

### 2. Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Then edit `.env` and add your credentials:

**Required for the generator:**
```env
ANTHROPIC_API_KEY=sk-ant-your_actual_api_key_here
```

Get your Anthropic API key from: https://console.anthropic.com/

**Required for authentication:**
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_service_role_key
SUPABASE_JWT_SECRET=your_jwt_secret
```

**Optional - for billing:**
```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PRICE_ID_PRO=price_...
STRIPE_PRICE_ID_BUSINESS=price_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### 3. Run the Application

**Development mode:**
```bash
uvicorn main:app --reload
```

**Production mode:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The app will be available at: `http://localhost:8000`

---

## How It Works

### User Flow

1. User visits `/app` (requires authentication)
2. Fills out the course metadata form:
   - Course title
   - Category
   - 4+ learning objectives (max 160 chars each)
   - Prerequisites
   - Target audience
   - Difficulty level
   - Number of questions (1-100)
   - Question formats (single/multiple choice, true/false, scenarios)
   - Explanation style
3. Clicks "Generate & Download CSV" or "Preview"
4. AI generates questions based on inputs
5. CSV file downloads automatically in Udemy's format

### Technical Flow

1. **Frontend** (`templates/app.html`):
   - Collects user inputs
   - Validates form data
   - Sends POST request to `/api/generator/generate`

2. **Backend** (`generator/routes.py`):
   - Receives request
   - Builds detailed AI prompt based on inputs
   - Calls Claude AI (Anthropic) to generate questions
   - Parses JSON response from AI
   - Converts to Udemy CSV format
   - Returns CSV file for download

3. **AI Generation**:
   - Uses `claude-3-5-sonnet` model
   - Generates contextually relevant questions
   - Ensures variety across learning objectives
   - Applies selected difficulty and explanation style
   - Returns structured JSON

4. **CSV Export**:
   - Converts questions to Udemy's format
   - Proper escaping and formatting
   - Pipe-separated answer options
   - Ready for bulk import to Udemy

---

## CSV Output Format

The generated CSV follows Udemy's official bulk exam import specification:

### Headers
```
question_title,question_type,question_text,possible_answers,correct_answer,explanation
```

### Example Output

```csv
"question_title","question_type","question_text","possible_answers","correct_answer","explanation"
"Python Variables Basics","multiple_choice","What is the correct way to create a variable in Python?","x = 5|var x = 5|int x = 5|x := 5","x = 5","In Python, you create a variable by simply assigning a value to a name using the equals sign. No type declaration is needed because Python is dynamically typed."
"Data Types Understanding","multiple_select","Which of the following are valid Python data types?","int|float|character|string|boolean","int|float|string|boolean","Python has int, float, string, and boolean as basic data types. There is no 'character' type in Python - single characters are just strings of length 1."
"Function Return Value","true_false","A Python function must always return a value.","True|False","False","Python functions can return values using the 'return' statement, but it's not mandatory. If no return statement is used, the function returns None by default."
"List Operations Scenario","multiple_choice","You need to add an element to the end of a list. Which method should you use?","append()|insert()|extend()|push()","append()","The append() method adds a single element to the end of a list. insert() adds at a specific position, extend() adds multiple elements, and push() is not a Python list method."
```

### Field Descriptions

| Field | Description |
|-------|-------------|
| `question_title` | Short title (5-10 words) |
| `question_type` | One of: `multiple_choice`, `multiple_select`, `true_false` |
| `question_text` | The full question text |
| `possible_answers` | Answer options separated by `\|` pipe character |
| `correct_answer` | Exact text of correct answer(s), multiple separated by `\|` |
| `explanation` | Why the answer is correct (uses selected tone) |

---

## API Endpoints

### Generator Endpoints

**POST /api/generator/generate**
- Generates questions and returns CSV file
- Request body: `GenerateTestRequest` (see below)
- Response: CSV file download

**POST /api/generator/preview**
- Generates up to 5 questions for preview
- Request body: `GenerateTestRequest`
- Response: JSON with questions array

### Request Body Example

```json
{
  "working_title": "Complete Python Programming",
  "category": "IT & Software",
  "learning_objectives": [
    "Understand Python variables and data types",
    "Write functions and use control structures",
    "Work with lists, dictionaries, and sets",
    "Handle errors and exceptions properly"
  ],
  "requirements": "Basic computer skills",
  "target_audience": "Beginner programmers",
  "difficulty_level": "beginner",
  "num_questions": 10,
  "question_formats": ["single-choice", "multiple-select", "true-false"],
  "explanation_style": "beginner-friendly"
}
```

---

## Deployment Options

### Option 1: Local Development
- Run with `uvicorn main:app --reload`
- Access at `localhost:8000`
- Good for testing and development

### Option 2: Cloud Hosting (Recommended for Production)

**Railway.app** (Easiest):
1. Push code to GitHub
2. Connect Railway to your repo
3. Add environment variables in Railway dashboard
4. Deploy automatically

**Vercel** (Serverless):
1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in project directory
3. Add environment variables in Vercel dashboard
4. Deploy

**DigitalOcean / AWS / GCP** (Traditional VPS):
1. Create a server instance
2. Install Python 3.11+
3. Clone repo and install dependencies
4. Configure nginx as reverse proxy
5. Use systemd to run as service

### Environment Variables for Production

Make sure to set these in your hosting platform:
- `ANTHROPIC_API_KEY` (required)
- `SUPABASE_URL` (for auth)
- `SUPABASE_KEY` (for auth)
- `SUPABASE_JWT_SECRET` (for auth)
- `STRIPE_SECRET_KEY` (for billing, optional)

---

## Video Asset Instructions

You mentioned potentially including a video. Here are your options:

### Option 1: YouTube Embed (Recommended)
- Upload your demo/tutorial video to YouTube
- Embed in landing page or app page using:
  ```html
  <iframe
    width="560"
    height="315"
    src="https://www.youtube.com/embed/YOUR_VIDEO_ID"
    frameborder="0"
    allowfullscreen>
  </iframe>
  ```

### Option 2: Local MP4 File
- Place video file in `static/videos/demo.mp4`
- Reference in HTML:
  ```html
  <video controls width="100%">
    <source src="/static/videos/demo.mp4" type="video/mp4">
  </video>
  ```
- **Note:** Large video files increase hosting costs and slow page load

**Recommendation:** Use YouTube for better performance and SEO.

---

## Content Generation Rules

The AI follows these rules when generating questions:

✅ **Quality Standards:**
- Questions directly relate to learning objectives
- Good variety across all objectives
- Clear, unambiguous wording
- Professional tone
- No hallucinated or absurd facts

✅ **Question Format:**
- **Multiple Choice:** 4 options, 1 correct
- **Multiple Select:** 4-6 options, 2-3 correct
- **True/False:** Clear statement with explanation for both cases
- **Scenario-based:** Real-world application questions

✅ **Difficulty Matching:**
- Beginner: Fundamental concepts, basic terminology
- Intermediate: Practical application, common use cases
- Advanced: Complex scenarios, edge cases, optimization
- Mixed: 30% beginner, 50% intermediate, 20% advanced

✅ **Explanation Styles:**
- Beginner-friendly: Simple language, no jargon
- Technical: Precise terminology, domain-specific
- Very detailed: In-depth with examples
- Short/concise: 1-2 sentences
- Fun/casual: Conversational with humor
- Academic: Formal with best practices

---

## Testing the App

### 1. Test Question Generation

Fill out the form with sample data:
- Title: "Python for Beginners"
- Category: IT & Software
- Learning objectives:
  - "Understand Python syntax"
  - "Work with variables and data types"
  - "Create functions"
  - "Handle errors"
- Number of questions: 5
- Format: Mix all
- Style: Beginner-friendly

Click "Preview" to see 5 sample questions without downloading.

### 2. Test CSV Download

Click "Generate & Download CSV" to get the full CSV file.

### 3. Verify CSV in Udemy

1. Go to your Udemy instructor dashboard
2. Navigate to Course > Practice Tests
3. Click "Bulk Import"
4. Upload the generated CSV
5. Verify all questions imported correctly

---

## Troubleshooting

### Common Issues

**"Failed to parse AI response"**
- The AI returned malformed JSON
- Usually self-resolves on retry
- Check Anthropic API status if persistent

**"Generation failed: API key invalid"**
- Check your `ANTHROPIC_API_KEY` in `.env`
- Ensure no extra spaces or quotes
- Verify key is active in Anthropic console

**"At least 4 learning objectives required"**
- Make sure you've filled in 4+ objectives
- Each must have content (not empty)

**CSV file won't open**
- Try a different CSV viewer (Excel, Google Sheets, VSCode)
- Check for proper UTF-8 encoding

**Questions are low quality**
- Provide more detailed learning objectives
- Be specific about prerequisites and audience
- Try different explanation styles

---

## Cost Estimation

### Anthropic API Costs
- Model: Claude 3.5 Sonnet
- Cost: ~$3 per million input tokens, ~$15 per million output tokens
- Typical request: 10 questions ≈ $0.05-$0.10
- 1000 generations ≈ $50-$100

### Hosting Costs
- **Railway/Vercel:** $5-20/month (free tier available)
- **DigitalOcean:** $5-12/month
- **AWS/GCP:** Variable, $10-50/month typical

---

## Next Steps

1. ✅ Set up your `.env` file with Anthropic API key
2. ✅ Run `pip install -r requirements.txt`
3. ✅ Start the server with `uvicorn main:app --reload`
4. ✅ Test the generator at `http://localhost:8000/app`
5. ✅ Deploy to production hosting
6. ✅ (Optional) Add your demo video
7. ✅ (Optional) Configure Stripe billing for paid tiers

---

## Support

For questions or issues:
- Check the FastAPI docs: https://fastapi.tiangolo.com/
- Anthropic API docs: https://docs.anthropic.com/
- Udemy bulk import guide: https://support.udemy.com/

---

**Built with Claude Code** - Your AI pair programmer
