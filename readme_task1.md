# readme_task1.md

# Yelp Review Sentiment Analysis with LLM Prompting Strategies

This project implements an experimental framework to evaluate different Large Language Model (LLM) prompting strategies for sentiment analysis. Specifically, it uses Google's Gemini model to predict star ratings (1-5) based on the text of Yelp reviews.

The code is designed to measure not just accuracy, but also the **reliability** and **JSON formatting adherence** of the model across different prompting techniques.

---

## ⚠️ Important: Execution Environment

**This notebook was built and optimized for [Google Colab](https://colab.research.google.com/).**

It utilizes Colab-specific libraries (like `google.colab.files` for uploading datasets) and form widgets. It is highly recommended to run this file specifically on Google Colab.

---

## 🚀 How to Run

1.  **Open Google Colab:**
    Go to [colab.research.google.com](https://colab.research.google.com/).

2.  **Upload the Notebook:**
    Upload the `fynd_task1.ipynb` file to your session.

3.  **Get a Google Gemini API Key:**
    *   Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to generate a free API key.
    *   You will need this key to run the experiments.

4.  **Dataset Preparation (Two Options):**
    *   **Option A (Automatic):** If you have a Kaggle API token (`kaggle.json`), the script can auto-download the `omkarsabnis/yelp-reviews-dataset`.
    *   **Option B (Manual):** Download `yelp.csv` from Kaggle manually. When you run the script, it will check the working directory. If missing, it will prompt you to upload the file using a file picker widget.

5.  **Run the Cells:**
    *   Execute the cells in order.
    *   When the script asks for your **Gemini API Key**, paste it into the secure input box (the input will be hidden).

---

## 🧠 Prompting Strategies Used

This experiment compares three distinct styles of prompting to determine which yields the most accurate and valid JSON output.

### 1. Direct Prompting (Zero-Shot)
*   **Concept:** The model is given a strict instruction ("You are a strict JSON-only API") and the task description without any examples.
*   **Goal:** To test the model's baseline ability to follow schema constraints and perform sentiment analysis based solely on its pre-training.
*   **Prompt Structure:** Instruction + Rules + Review + Output Schema.

### 2. Few-Shot Prompting
*   **Concept:** The prompt includes the instruction *plus* three specific examples (input review mapped to the correct output JSON).
*   **Goal:** To use "In-Context Learning." By showing the model examples of a negative (1-star), neutral (3-star), and positive (5-star) review, we aim to calibrate its scoring logic and reinforce the JSON structure.

### 3. Chain-of-Thought (CoT) Prompting
*   **Concept:** The model is asked to generate a "reasoning" or "explanation" field *before* or alongside the final prediction.
*   **Goal:** To encourage the model to "think" step-by-step. Analyzing the sentiment textually before assigning a number often reduces hallucination and improves accuracy on complex/nuanced reviews.

---

## 📂 Code Structure & Function Definitions

The notebook is organized into several distinct blocks. Below is a breakdown of the key functions and their purposes:

### Configuration & Utilities
*   **`configure_gemini()`**
    *   **Purpose:** Securely handles authentication. It checks for environment variables or prompts the user via a password input field to obtain the Google Gemini API key.
    *   **Output:** Configures the `google.generativeai` library.

*   **`call_model(prompt: str)`**
    *   **Purpose:** The interface to the LLM. It sends the prompt to the `gemini-2.5-flash-lite` model.
    *   **Key Feature:** It enforces `response_mime_type: "application/json"`, which forces the model to output valid JSON, significantly reducing parsing errors.
    *   **Reliability:** Implements a retry mechanism (up to 3 times) with exponential backoff if the API fails.

*   **`extract_json_object(text: str)`**
    *   **Purpose:** Cleaning and parsing. Even when asked for JSON, models sometimes include Markdown fences (e.g., ` ```json ... ``` `). This function strips those fences and safely parses the string into a Python dictionary.

### Data Loading
*   **`load_kaggle_dataset(sample_size: int)`**
    *   **Purpose:** Data ingestion. It attempts to find `yelp.csv` locally, download it via the Kaggle API, or prompt the user to upload it via the Colab interface. It returns a sampled, clean pandas DataFrame.

### Evaluation Metrics
*   **`evaluate_predictions(y_true, y_pred)`**
    *   **Purpose:** Calculates standard machine learning metrics:
        *   **Accuracy:** Percentage of exact matches.
        *   **MAE (Mean Absolute Error):** How far off the star ratings are on average (e.g., predicting 4 when the truth is 5).

*   **`compute_json_validity_rate(parsed_results)`**
    *   **Purpose:** Measures technical compliance. It calculates the percentage of model responses that were successfully parsed as valid JSON.

*   **`reliability_score(preds_per_run)`**
    *   **Purpose:** Measures determinism. It checks what fraction of reviews received the *exact same rating* across multiple independent runs of the same prompt.

### Orchestration
*   **`run_experiments(sample_size)`**
    *   **Purpose:** The main loop.
    *   **Workflow:**
        1.  Loads data.
        2.  Iterates through all 3 Prompt Strategies.
        3.  Runs each prompt multiple times (defined by `RUNS_PER_PROMPT`) to test consistency.
        4.  Aggregates results and computes metrics.
        5.  Saves a summary CSV and detailed prediction logs.
        6.  Prints a comparison table and a brief discussion of results.

---

## 📊 Outputs

After running the notebook, two CSV files will be generated in your Colab file explorer:

1.  **`comparison_summary.csv`**: A high-level table comparing Accuracy, MAE, JSON Validity, and Agreement scores for Direct, Few-Shot, and CoT strategies.
2.  **`predictions_[StrategyName].csv`**: Detailed logs showing the specific text, true rating, and predicted rating for every review processed.

## 📦 Dependencies

While the notebook is designed to install missing packages automatically using `!pip install`, it relies on the following Python libraries:

*   `google-generativeai` (for the LLM)
*   `pandas` (for data manipulation)
*   `numpy` (for math operations)
*   `scikit-learn` (for accuracy/metrics)
*   `matplotlib` & `seaborn` (for plotting/visualization)
*   `tqdm` (for progress bars)
*   `kaggle` (optional, for dataset downloading)