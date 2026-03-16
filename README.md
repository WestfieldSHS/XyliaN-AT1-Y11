# XyliaN-AT1-Y11: Vocabulary Flashcard App

A comprehensive vocabulary learning platform with flashcards, practice quizzes, daily challenges, streak tracking, and personalized learning features.

## Features

✨ **Vocabulary Flashcards** - Learn new words with definitions and examples
📝 **Practice Quizzes** - Test your knowledge with multiple-choice questions
📚 **Words in Categories** - Organized vocabulary by topics (Adjectives, Nouns, etc.)
🔄 **Daily Refresh** - New words everyday with consistent daily challenges
🔥 **Streak Tracking** - Build and maintain your learning streak
⭐ **Favorites** - Save words for later review and practice

## Project Structure

```
XyliaN-AT1-Y11/
├── Word.storage/           
├── requirements.txt              # Python dependencies
├── vocab.json                     # Vocabulary words database
├── users.json                    # User profiles and progress
└── README.md                     # This file
```

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Clone or navigate to the project directory:
```bash
cd XyliaN-AT1-Y11
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the FastAPI server:
```bash
python -m uvicorn Word.storage.word_storage:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### User Management
- **POST** `/users/{user_id}` - Create a new user
- **GET** `/users/{user_id}` - Get user profile and streak info
- **GET** `/stats/{user_id}` - Get detailed user statistics

### Vocabulary
- **GET** `/words` - Get all vocabulary words
- **GET** `/words/{word_id}` - Get a specific word
- **GET** `/words/category/{category}` - Get words by category
- **GET** `/categories` - Get all available categories

### Flashcards
- **GET** `/flashcards` - Get random flashcards
- **GET** `/flashcards/daily/{user_id}` - Get today's personalized flashcards

### Practice & Quiz
- **GET** `/practice/quiz` - Generate a multiple-choice quiz
- **POST** `/practice/answer` - Submit answer and update streak
  - Parameters: `user_id`, `word_id`, `correct` (boolean)

### Favorites
- **POST** `/favorites/{user_id}/{word_id}` - Add word to favorites
- **DELETE** `/favorites/{user_id}/{word_id}` - Remove from favorites
- **GET** `/favorites/{user_id}` - Get all favorite words

## Usage

### Web Interface

1. Open `index.html` in your browser
2. Enter a username to start
3. Choose from:
   - **Today's Words** - Practice daily flashcards
   - **Quiz Mode** - Take multiple-choice quizzes
   - **All Words** - Browse all vocabulary
   - **Favorites** - Review saved words
   - **Statistics** - View your progress

### Sample Vocabulary

The system comes with 10 sample words in diverse categories:
- **Ephemeral** - Lasting for a very short time
- **Ubiquitous** - Present everywhere
- **Serendipity** - Happy chance occurrence
- **Eloquent** - Persuasive speaking
- **Pragmatic** - Practical approach
- **Meticulous** - Very careful and precise
- **Ambiguous** - Unclear, multiple meanings
- **Nostalgia** - Longing for the past
- **Benevolent** - Kind and generous
- **Catalyst** - Something that causes change

## Features in Detail

### Daily Refresh 🔄
- Each user gets a unique set of words daily
- Based on user ID and current date
- Encourages consistent daily practice

### Streak Tracking 🔥
- Automatically tracks consecutive days of practice
- Resets if you miss a day
- Motivates consistent learning

### Favorites System ⭐
- Save words for later review
- Easy access to personalized learning list
- Build custom study sets

### Practice Quiz 📝
- Multiple-choice format
- Randomized options
- Tracks correct answers
- Immediate feedback

## Development Notes

### Adding New Words

Edit `data.json` or use the API to add new vocabulary. Each word should have:
```json
{
  "id": 11,
  "word": "Serendipitous",
  "definition": "Occurring by happy chance",
  "example": "A serendipitous meeting changed my life.",
  "category": "Adjectives",
  "difficulty": 4
}
```

### Customization

- Modify word difficulty levels (1-5 scale)
- Add custom categories
- Adjust daily word limits
- Customize quiz length

## Technologies


## Future Enhancements

- [ ] Database integration (SQLite/PostgreSQL)
- [ ] User authentication (JWT)
- [ ] Spaced repetition algorithm
- [ ] Audio pronunciation
- [ ] Mobile app
- [ ] Leaderboard system
- [ ] Achievement badges
- [ ] Import custom word lists

## License

Educational project for vocabulary learning.

## Support

For issues or feature requests, please refer to the project documentation.