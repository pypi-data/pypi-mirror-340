# Ai Package Wrapper

This is a wrapper package for multiple ai tools

It contains 4 total modules:
1. OCR Module
2. Augmentation Module
3. Sentiment Analysis Module
4. Explainable AI Module

___________________

## OCR MODULE (made by @Madhavseekri)

This is a simple and efficient OCR (Optical Character Recognition) module written in Python. It allows you to extract text from images using `pytesseract` and `Pillow`.

---

## What It Does

- Extracts readable text from image files.
- Supports PNG, JPEG, and other image formats.
- Can be extended for use in document scanning, data entry automation, and AI projects.

## How It Works
1. <b>extract_text(image_path)</b>

> Opens an image file and extracts text from it using pytesseract. Returns the extracted text.

---

# Augmentation Module (made by @Ayushi-000)

*augmentation* is a Python package built for learning how to deploy real-world Python projects using Pip and Poetry. It includes simple examples of data augmentation for image, text, and audio files.

This package was created and deployed as part of a *Prodigal's first task* on Python package deployment using *Poetry, **PyPI, **GitHub, and **CI/CD pipelines*.

---

## How It Works

1. <u><b>init()</b></u>

> > Sets up three augmentation pipelines:

> Audio Augmentation: Applies Gaussian noise, time stretching, and pitch shifting.

> Image Augmentation: Uses horizontal flipping, random brightness/contrast, and rotation.

> Text Augmentation: Performs synonym replacement using nlpaug.



2. <u><b>augment_audio(input_path, output_path)</b></u>

> Reads an audio file, applies the audio augmentation pipeline, writes the augmented audio to a file, and returns the output path.


3. <u><b>augment_image(input_path, output_path)</b></u>

> Loads an image, applies image augmentation, writes the augmented image back to disk, and returns the output path.


4. <u><b>augment_text(text)</b></u>

> Processes a given text string through the text augmentation pipeline and returns the augmented text (a list of augmented strings).


---

# Sentiment Analyzer (made by @abhay-cerberus)

A simple sentiment analysis package that leverages [TextBlob](https://textblob.readthedocs.io/) to determine whether a piece of text expresses positive, negative, or neutral sentiment. It provides an easy-to-use interface for analyzing both single texts and batches of texts.

## How It Works
1. <u><b>analyze_text(text)</u></b>

> Processes a single text string by converting it to lowercase, calculating its sentiment polarity using TextBlob, and returning a sentiment label ("positive", "negative", or "neutral").

<br>

2. <u><b>analyze_batch(texts)</u></b>

> Takes a list of text strings, analyzes each one using analyze_text, and then returns both the raw counts and percentages for each sentiment category.


__________________________


# ExplainableAi (made by @priyanshibindal)

## How It Works

1. explain_model(model, data, method='shap')
> Loads a pre-saved model and dataset (from churn_model.pkl), creates a SHAP explainer for the model, and generates visual explanations:

> Produces a waterfall plot for the first prediction.

> Produces a beeswarm plot summarizing feature importance.

