# Model Card: Mood Machine

This model card covers **both** versions of the Mood Machine classifier:

1. A **rule-based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit-learn

---

## 1. Model Overview

**Model type:**
Both models were built and compared. The rule-based model was the primary implementation; the ML model was trained on the same dataset to observe differences in behavior on tricky examples.

**Intended purpose:**
Classify short social media-style text posts into one of four mood labels: `positive`, `negative`, `neutral`, or `mixed`. The system is designed for informal, modern internet language including slang, emojis, and mixed emotions.

**How it works (brief):**
- *Rule-based:* Each token in a post is matched against two hardcoded word lists (`POSITIVE_WORDS`, `NEGATIVE_WORDS`). Matches contribute `+1` or `-1` to a running score. A negation check flips the score if the immediately preceding token is `not`, `no`, or `never`. The final score maps to a label.
- *ML model:* Posts are converted to bag-of-words vectors using `CountVectorizer`, then a `LogisticRegression` classifier is trained on those vectors paired with `TRUE_LABELS`. The model learns word-to-label associations from data rather than following explicit rules.

---

## 2. Data

**Dataset description:**
`SAMPLE_POSTS` contains 17 labeled posts total. The original 6 starter posts used simple, unambiguous language. We added 11 new posts in two rounds to stress-test both models:

- Round 1 (7 posts): Modern slang (`bussin`, `mid`, `lowkey`, `no cap`), emojis (🎉💀🔥🙃😬), mixed emotions, sarcasm, and humor-masked negativity (e.g., `"just got ghosted lol why am I even surprised 💀"`).
- Round 2 (4 posts): Targeted edge cases — ironic use of a positive word (`"oh great, another Monday 🙄"`), double negation (`"not gonna say it was bad but I definitely didn't have fun"`), softened negativity (`"it's not the worst thing ever I guess"`), and pure out-of-vocabulary slang (`"that presentation slapped fr fr 🔥"`).

**Labeling process:**
Labels were assigned by human judgment based on the overall emotional tone of each post, not the literal sentiment of individual words. Posts like `"I'm so exhausted but I finally got it done! 🎉"` were labeled `mixed` because the exhaustion and the accomplishment carry roughly equal emotional weight. Posts using sarcasm were labeled by intended meaning rather than surface words.

**Important characteristics of the dataset:**

- Contains modern internet slang: `bussin`, `mid`, `slapped`, `fr fr`, `no cap`, `lowkey`
- Includes emojis used as emotional signals: 🔥 (enthusiasm), 💀 (dark humor/resignation), 🙃 (sarcasm/forced acceptance), 🎉 (joy)
- Includes sarcasm where a positive word expresses a negative sentiment
- Several posts express genuinely mixed feelings that resist a single label
- Some posts are intentionally ambiguous — reasonable people could disagree on the label

**Possible issues with the dataset:**

- Only 17 examples — far too small for a model to generalize reliably
- `mixed` and `neutral` labels are underrepresented compared to `positive` and `negative`
- All posts are written in one cultural register (young, English-speaking, internet-native). The model has never seen formal English, non-English text, or other cultural dialects.
- The ML model trains and evaluates on the same data, so its "accuracy" reflects memorization, not generalization

---

## 3. How the Rule-Based Model Works

**Scoring rules:**

- `preprocess`: lowercases the text, strips all punctuation via `str.maketrans`, and splits on whitespace into a list of string tokens.
- `score_text`: iterates over tokens. For each token:
  - If it is in `POSITIVE_WORDS` (a set of 10 words): `score += 1`
  - If it is in `NEGATIVE_WORDS` (a set of 10 words): `score -= 1`
  - Negation enhancement: if the immediately preceding token is `"not"`, `"no"`, or `"never"`, the score contribution is flipped (e.g., `"not happy"` scores `-1` instead of `+1`)
- `predict_label`: maps `score > 0` → `"positive"`, `score < 0` → `"negative"`, `score == 0` → `"neutral"`

**Strengths:**

- Fully transparent and inspectable — you can trace every scoring decision token by token
- Handles basic explicit negation correctly (e.g., `"I am not happy about this"` → `negative`)
- Deterministic: same input always produces the same output
- No training data required

**Weaknesses:**

- Vocabulary-blind to any word not in the 10+10 hardcoded lists. Slang like `bussin`, `mid`, `slapped`, `ghosted` all score 0 regardless of how emotionally charged they are.
- Cannot detect sarcasm. See the specific failure case in Section 5 below.
- Negation only looks one token back — it cannot handle chained or embedded negation like `"not gonna say it was bad but I definitely didn't have fun"`.
- Emojis stripped by punctuation removal and never scored.
- No concept of context, emphasis, or sentence structure.

---

## 4. How the ML Model Works

**Features used:**
Bag-of-words representation via scikit-learn's `CountVectorizer`. Each post becomes a sparse vector where each dimension corresponds to a word in the training vocabulary and the value is the word's count in that post.

**Training data:**
Trained directly on `SAMPLE_POSTS` and `TRUE_LABELS` from `dataset.py` (17 examples across 4 label classes).

**Training behavior:**
Because the model trains and evaluates on the same 17 posts, it achieves near-perfect training accuracy — but this is memorization, not learning. The model associates entire word co-occurrence patterns with labels rather than individual sentiment words. This means it can "learn" that `"slapped fr fr"` → `positive` if that exact phrase appears in training, but it will fail on any unseen phrasing.

**Strengths and weaknesses:**
- *Strength:* Can pick up multi-word patterns and co-occurrences that the rule-based model ignores entirely. If `"bussin"` and `"slapped"` appear in labeled training examples, the model learns to use them as signals.
- *Strength:* Adapts to whatever labels are provided — no hardcoded word list needed.
- *Weakness:* With only 17 training examples, the model severely overfits. It effectively memorizes posts rather than learning generalizable sentiment.
- *Weakness:* `CountVectorizer` discards word order, so it still cannot detect sarcasm from context the way a human would.
- *Weakness:* Logistic regression with a bag-of-words input cannot model sentence structure or intent.

---

## 5. Evaluation

**How we evaluated:**
Both models were evaluated on the same `SAMPLE_POSTS` with `TRUE_LABELS` used for training. Rule-based accuracy was measured via `main.py`; ML accuracy via `ml_experiments.py`. Note this is training accuracy for the ML model, not a held-out test set.

**Observed accuracy:**
- Rule-based model: **38%** on the 13-post dataset at time of measurement
- ML model: near-perfect on training data due to overfitting (not a reliable signal)

**Examples of correct rule-based predictions:**

- `"I love this class so much"` → `positive` — `love` is in `POSITIVE_WORDS`, no negation, score = +1. ✓
- `"Today was a terrible day"` → `negative` — `terrible` is in `NEGATIVE_WORDS`, score = -1. ✓
- `"I am not happy about this"` → `negative` — `not` precedes `happy`, negation flips to -1. ✓ This is the negation enhancement working as intended.

**Examples of incorrect rule-based predictions (failures):**

1. **Sarcasm failure:** `"I absolutely love sitting in traffic for two hours 🙃"` → predicted `positive`, true label `negative`.
   - Step-by-step: `preprocess` produces tokens `["i", "absolutely", "love", "sitting", "in", "traffic", "for", "two", "hours"]`. The loop hits `love` at index 2; the preceding token is `"absolutely"`, which is not in `{"not", "no", "never"}`, so no negation fires. Score = `+1`. `predict_label` returns `"positive"`.
   - Why it fails: The engine is purely lexical. It finds `love` and scores it positive with no awareness that the surrounding context (`"in traffic for two hours"`) signals frustration. Sarcasm inverts the intended meaning of a word — a mechanism the rule system has no model for. Negation handling only catches explicit negator words one position back; sarcasm is a completely different linguistic phenomenon.

2. **Out-of-vocabulary slang:** `"okay the food was actually bussin no cap 🔥"` → predicted `neutral`, true label `positive`.
   - `bussin` is not in `POSITIVE_WORDS`. Score = 0. The model has no way to know this is enthusiastic praise.

3. **Mixed emotion collapse:** `"Feeling tired but kind of hopeful"` → predicted `negative`, true label `mixed`.
   - `tired` scores -1; `hopeful` is not in any word list, so it contributes 0. Final score = -1 → `negative`. The positive half of the emotion is completely invisible.

---

## 6. Limitations

- **Tiny dataset:** 17 examples across 4 label classes is insufficient for any reliable generalization. Both models are essentially operating on toy data.
- **No test/train split:** The ML model trains and is evaluated on identical data — its accuracy number is meaningless as a measure of real-world performance.
- **Sarcasm is undetectable:** Neither model can detect irony or sarcasm. Any text where the surface words mean the opposite of the intended meaning will be mislabeled.
- **Slang vocabulary gap:** The rule-based model's 20 hardcoded words miss the vast majority of modern emotional language. Words like `bussin`, `mid`, `slapped`, `ghosted`, `lowkey`, `fr fr` are all invisible to it.
- **Bias toward internet English:** The entire dataset is written in a single cultural register — young, English-speaking, internet-native. The model is heavily optimized for this style and would likely perform very poorly on formal writing, academic text, regional dialects, code-switching, or non-English phrases. A sentence like "I find this arrangement most disagreeable" would score `neutral` despite clear negative intent.
- **Emoji blindness:** Emojis are stripped during preprocessing and contribute nothing to the score, even though they often carry the primary emotional signal in short posts (e.g., 💀 almost always signals dark humor or defeat).
- **No sentence structure awareness:** Both models treat text as an unordered bag of tokens. Word order, emphasis, contrast words (`"but"`, `"although"`), and grammatical structure are all ignored.

---

## 7. Ethical Considerations

- **Misclassifying distress:** A post like `"not gonna lie I don't hate this 😅"` could mask genuine distress behind casual language. A rule-based system labeling it `neutral` or `positive` in a mental health context could have serious consequences.
- **Cultural and linguistic bias:** The model is tuned for one narrow dialect of internet English. Deploying it on text from other communities — older adults, non-native English speakers, speakers of African American Vernacular English, regional slang communities — could produce systematically wrong results, amplifying existing inequities if the system is used to make decisions about people.
- **Privacy:** Analyzing personal messages or social media posts for mood without explicit consent is a privacy concern, even for a toy classifier.
- **Overconfidence of output:** The model always returns a label — it never says "I don't know." This false confidence can mislead users into trusting a prediction that is essentially a guess.

---

## 8. Ideas for Improvement

- **Expand the word lists:** Add slang, emoji mappings, and intensifiers (`"extremely"`, `"kinda"`, `"literally"`) to the rule-based model's vocabulary.
- **Emoji scoring:** Map common emojis to sentiment scores instead of stripping them (🔥 → +1, 💀 → -1, 🎉 → +1, 🙃 → -1).
- **TF-IDF instead of raw counts:** Replace `CountVectorizer` with `TfidfVectorizer` to down-weight very common words and up-weight distinctive ones.
- **Larger, balanced dataset:** Collect hundreds of labeled examples with balanced representation across all four label classes and across different language registers.
- **Real train/test split:** Hold out 20-30% of data for evaluation so accuracy reflects generalization, not memorization.
- **Sarcasm detection:** Add a small set of sarcasm-marker rules (e.g., if a clearly positive word follows a clearly negative context phrase, flag as sarcasm).
- **Transformer-based model:** A small pre-trained model like `distilbert-base-uncased` fine-tuned on sentiment data would handle slang, context, and sarcasm far better than either current approach.
- **"mixed" threshold in rule-based model:** Instead of mapping score == 0 to `neutral`, map small absolute scores (e.g., -1 ≤ score ≤ 1 with both positive and negative hits) to `mixed`.
