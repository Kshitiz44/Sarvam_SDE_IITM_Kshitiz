# Project Dependencies

This project requires the following dependencies:

- **Python**: Version 3.1
- **Flask**: A micro web framework for Python
- **Tesseract**: An OCR (Optical Character Recognition) library
- **Sarvam API**: Subscription key required for accessing the Sarvam API

Make sure to install these dependencies before running the program.

## Frontend

- The frontend accepts requests from the user in the form of an image containing English text and the target language.
- Using the Flask framework, the backend method to convert the image into audio is invoked.

## Backend

-  The code makes use of teserract open source library to extract english text from the image
-  This text is forwarded to the Sarvam's text translation API call to get the text in desired language
-  This translated text is now converted to .wav audio file using Sarvam's text to speech API call

## Setup instructions
- The backend needs to be locally hosted in order to recieve requests, which hasn't been implemented to completion yet