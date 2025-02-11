# 1. Project description
This project aims to build a language learning platform where teachers can create and manage exercises (either fill-in-the-gap or multiple-choice), organize them into sets, and share those sets with learners via a simple access code. The platform uses FastAPI on the backend with Pydantic for data validation, and will eventually store data in PostgreSQL. Currently, authentication is limited to a single teacher role, but the system is designed to accommodate future roles (e.g., admin, additional content creators) without breaking the existing API.

**Key Features**
- **Teacher Role**: Can create exercises, group them into sets (lesson or exam), and generate access codes.
- **Exercises**: Each exercise is strictly one type—fill-in-the-gap or multiple-choice—and can contain multiple sentences/questions.
- **Exercise Sets**: A teacher can share an entire set of exercises with learners via a unique access code.
- **Learner Access**: Learners can anonymously view or solve exercises through the provided link + code.
- **Exam vs. Lesson**:
    - **Lesson**: Learners see correct answers for immediate feedback.
    - **Exam**: Learners submit their work, and the teacher reviews it later.
- **Future Expansion**: Flexible design allows easy addition of new exercise/question types, more user roles, and advanced features like AI-assisted content creation or analytics.

# 2. API Design
## 2.1. Authentication & User Management

#### POST `/api/v1/auth/register`
- **Registers a new user.**  
- **Request Body** includes:
  - `email`
  - `password`
  - `role` (default `"teacher"` for now, but extensible for future roles).
- **Returns**:
  - A user object (or minimal info)
  - Possibly an auth token if you want auto-login on registration.

---

#### POST `/api/v1/auth/login`
- **Authenticates a user**, returns a JWT (or session token).
- **Response** includes:
  - The user’s role
  - A token

---

#### (Optional) POST `/api/v1/auth/password-recovery`
- For future expansions like password resets or email confirmations.

> **Note**:  
> The `role` field (e.g., `"teacher"`, `"admin"`) will be stored in the `users` or `teacher` table in the database. All subsequent endpoints require the JWT to identify the user and role.

---

## 2.2. Exercises (Protected by Role Checks)

All endpoints under `/api/v1/exercises` are for creating and managing exercises. Under the hood, only teachers (or certain roles) can perform CRUD actions.

### 2.2.1 Create an Exercise

#### POST `/api/v1/exercises`

**Request Body** might look like (fill-in-gap example):
```json
{
  "exercise_type": "fill_in_gap",
  "title": "Irregular Verbs Practice",
  "fill_gap_sentences": [
    { "text": "I ___ a book.", "correct_answer": "read" }
  ]
}
```
or
```json
{
  "exercise_type": "multiple_choice",
  "title": "Vocabulary Test",
  "multiple_choice_questions": [
    {
      "question_text": "Pick the correct word",
      "choices": ["read", "red", "rode"],
      "correct_choice_index": 0
    }
  ]
}
```

**Behavior**:
- If `exercise_type = fill_in_gap`, create a row in `exercise` + rows in `fill_gap_sentence`.
- If `exercise_type = multiple_choice`, create a row in `exercise` + rows in `multiple_choice_question`.

**Authorization**: Only users with role="teacher" (or similar) can create exercises.

### 2.2.2 Get All Exercises (Owned by Current User)
#### GET `/api/v1/exercises`
- Returns a list of exercises belonging to the authenticated user (e.g., teacher_id).
- Optional: Could allow admin roles to see all exercises, etc.

### 2.2.3 Get a Single Exercise
#### GET `/api/v1/exercises/{exercise_id}`
- Returns the exercise record plus its fill-gap or multiple-choice details.

### 2.2.4 Update an Exercise
#### PUT `/api/v1/exercises/{exercise_id}`
- Body can include updates to the title, or add/remove sentences/questions.
- Authorization: Must match teacher_id or have an admin role.

### 2.2.5 Delete an Exercise
#### DELETE `/api/v1/exercises/{exercise_id}`
- Removes the exercise record and related rows in fill_gap_sentence or multiple_choice_question.

(If you prefer separate endpoints for fill-gap vs. multiple-choice, that’s fine. The key is they live under /api/v1/exercises rather than /teacher/exercises/….)

## 2.3. Exercise Sets (Lessons/Exams)
Teachers group exercises into sets that learners can access. Again, these endpoints are typically reserved for teachers or higher roles.

### 2.3.1 Create an Exercise Set
#### POST `/api/v1/exercise-sets`
- Body might include title, set_type ("lesson" or "exam"), and a list of exercise_ids.
- Generates an access_code.

### 2.3.2 List All Sets (for the Teacher)
#### GET `/api/v1/exercise-sets`
- Returns all sets belonging to the current user.

### 2.3.3 Get/Update/Delete a Single Set
#### GET `/api/v1/exercise-sets/{set_id}`
- Return the set + associated exercises.
#### PUT `/api/v1/exercise-sets/{set_id}`
- Update title, add/remove exercises, etc.
#### DELETE `/api/v1/exercise-sets/{set_id}`

### 2.3.4 View Submissions (if it’s an “exam” set)
#### GET `/api/v1/exercise-sets/{set_id}/submissions`
- Return a list of submissions from anonymous learners.
#### GET `/api/v1/exercise-sets/{set_id}/submissions/{submission_id}`
- Detailed view of a single submission (the user’s answers).


## 2.4 Anonymous (Learner) Endpoints

### 2.4.1 Fetch a Set by Access Code
#### GET `/api/v1/exercise-sets/{access_code}`
- No authentication needed (or a minimal check).
- The system looks up `exercise_set` by `access_code`.
- Returns exercises inside that set, including all fill-gap or multiple-choice data needed to solve them.
- If `set_type="lesson"`, you can choose to include correct answers (or reveal them upon submission).
- If `set_type="exam"`, omit correct answers.

### 2.4.2 Submit Answers
#### POST `/api/v1/exercise-sets/{access_code}/submit`
- Accepts a JSON body with an anonymous user ID or name, plus their answers.
- Stores a new row in `submission`.
- If it’s a `lesson`, you might return correct answers immediately.
- If it’s an `exam`, you might simply confirm success.

## 2.5 Role-Based Access (Under the Hood)
#### 1. `role` in JWT:
- When a user logs in, you embed `role="teacher"` (or `"admin"`) into the token payload.
- Each protected endpoint checks `role` to verify the user’s permissions.
- Non-privileged roles can’t call endpoints like `POST /api/v1/exercises`.

#### 2. Single or Multiple Roles:
- Even if you store a single role now (`"teacher"`), this approach scales to additional roles in the future.
- The endpoints don’t need to change, you’ll just adjust your permission checks.

## 2.6 Summary of the Revalidated API
### Auth
- `POST /api/v1/auth/register`

- `POST /api/v1/auth/login`

### Exercises (Requires role = Teacher or Admin, typically)
- `POST /api/v1/exercises` (create fill-gap or multiple-choice, based on `exercise_type`)

- `GET /api/v1/exercises (list my exercises)`

- `GET /api/v1/exercises/{exercise_id}`

- `PUT /api/v1/exercises/{exercise_id}`

- `DELETE /api/v1/exercises/{exercise_id}`

### Exercise Sets (Also teacher/admin only)
- `POST /api/v1/exercise-sets`

- `GET /api/v1/exercise-sets`

- `GET /api/v1/exercise-sets/{set_id}`

- `PUT /api/v1/exercise-sets/{set_id}`

- `DELETE /api/v1/exercise-sets/{set_id}`

- `GET /api/v1/exercise-sets/{set_id}/submissions`

- `GET /api/v1/exercise-sets/{set_id}/submissions/{submission_id}`

### Learner Access (Anonymous or minimal data)
- `GET /api/v1/exercise-sets/{access_code}` (view the set)

- `POST /api/v1/exercise-sets/{access_code}/submit`

**Result**:
- A consistent, resource-based API path structure.
- Flexible user model in the background that can handle future roles without changing the API path.
- Clear boundaries: teachers create/modify exercises and sets; learners use access codes to retrieve and submit.

# 3. Database Structure
```sql
                      +-------------+
                      |   teacher   |
                      |-------------|
                      | id (PK)     |
                      | email       |
                      | password_...|
                      | name        |
                      | created_at  |
                      | updated_at  |
                      +-------------+
                             | 1
                             | 
                             | N
                      +---------------+
                      |   exercise    |
                      |---------------|
                      | id (PK)       |
                      | teacher_id FK |
                      | exercise_type |
                      | title         |
                      | created_at    |
                      | updated_at    |
                      +---------------+
                         | 1       \
                         |          \  (Depending on exercise_type)
                         | N         \
     +------------------------+       +--------------------------------+
     |   fill_gap_sentence    |       | multiple_choice_question       |
     |------------------------|       |--------------------------------|
     | id (PK)                |       | id (PK)                        |
     | exercise_id (FK)       |       | exercise_id (FK)               |
     | text                   |       | question_text                  |
     | correct_answer         |       | choices (array or JSON)        |
     | created_at             |       | correct_choice_index           |
     +------------------------+       | created_at                     |
                                      +--------------------------------+


                      +---------------------+
                      |    exercise_set     |
                      |---------------------|
                      | id (PK)             |
                      | teacher_id (FK)     |
                      | title               |
                      | set_type ("lesson"  |
                      |    or "exam")       |
                      | access_code (uniq)  |
                      | created_at          |
                      +---------------------+
                               ^
                               | 1
                               | N
                   +---------------------------+
                   | exercise_set_exercise     |
                   |---------------------------|
                   | exercise_set_id (FK, PK)  |
                   | exercise_id (FK, PK)      |
                   +---------------------------+

                      +--------------+
                      | submission   |
                      |--------------|
                      | id (PK)      |
                      | exercise_set_id (FK) <-- Typically for "exam" sets
                      | anonymous_user_id    |
                      | responses (JSON)     |
                      | submitted_at         |
                      +----------------------+

```