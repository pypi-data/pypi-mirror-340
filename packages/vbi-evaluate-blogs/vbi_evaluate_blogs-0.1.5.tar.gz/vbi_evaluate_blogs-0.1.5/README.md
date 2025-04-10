# Evaluate Blogs

Evaluate Blogs is a Python package designed to evaluate the content of PDF documents comprehensively. It combines advanced text analysis, image evaluation, and fact-checking capabilities to ensure the quality, relevance, and credibility of the document. The package leverages Azure OpenAI and other state-of-the-art tools to provide accurate and insightful evaluations.

## Features

### 1. Text Content Evaluation
- Analyzes the grammar, structure, and coherence of the text.
- Provides feedback on the readability and relevance of the content.
- Detects potential issues such as redundancy or lack of clarity.

### 2. Image Relevance Analysis
- Evaluates the quality and relevance of images in the document.
- Ensures that images align with the context and purpose of the document.
- Detects low-quality or irrelevant images.

### 3. Fact-Checking
- Verifies the factual accuracy of the content using external sources.
- Highlights potential inaccuracies or unsupported claims.
- Ensures the credibility of the information presented.

### 4. Modular Design
- Each feature is implemented as a separate module, allowing for flexible usage.
- Users can choose to run specific evaluations or combine them as needed.

## Install

```bash
pip install vbi-evaluate-blogs
```

## Usage

### Basic Example

Here is an example of how to use the `vbi_evaluate_blogs` package to analyze a PDF:

```python
from evaluate_module import evaluate
from langchain_openai import AzureChatOpenAI

# Initialize the Azure OpenAI model
model = AzureChatOpenAI(api_key="your_api_key")

# Path to the PDF file
pdf_path = "path/to/your/pdf_file.pdf"

# Evaluate the PDF
result = evaluate(pdf_path, model=model)

# Print the evaluation result
print(result)
```

### Detailed Usage

#### 1. Text Evaluation
The text evaluation module analyzes the PDF's text content for grammar, structure, and relevance. It provides insights into the quality of the written content.

```python
from evaluate_module import evaluate_text

# Path to the PDF file
pdf_path = "path/to/your/pdf_file.pdf"

# Analyze text content
text_result = evaluate_text(pdf_path, model=model)
print("Text Evaluation Result:", text_result)
```

#### 2. Image Analysis
The image analysis module checks the relevance and quality of images in the PDF. It ensures that images align with the document's context.

```python
from evaluate_module import evaluate_images

# Path to the PDF file
pdf_path = "path/to/your/pdf_file.pdf"

# Analyze images in the PDF
image_result = evaluate_images(pdf_path)
print("Image Analysis Result:", image_result)
```

#### 3. Fact-Checking
The fact-checking module verifies the factual accuracy of the content using external sources. This ensures the credibility of the information presented.

```python
from evaluate_module import evaluate_facts

# Path to the PDF file
pdf_path = "path/to/your/pdf_file.pdf"

# Perform fact-checking
fact_result = evaluate_facts(pdf_path, model=model)
print("Fact-Checking Result:", fact_result)
```

### Command-Line Usage

You can also use the package via the command line for quick evaluations:

```bash
python -m evaluate_module --file path/to/your/pdf_file.pdf
```

#### Additional Options
- `--text`: Perform only text evaluation.
- `--images`: Perform only image analysis.
- `--facts`: Perform only fact-checking.

Example:
```bash
python -m evaluate_module --file path/to/your/pdf_file.pdf --text --images
```

## Advanced Usage

### Customizing the Model
You can customize the Azure OpenAI model by providing additional parameters during initialization:

```python
model = AzureChatOpenAI(api_key="your_api_key", temperature=0.7, max_tokens=1000)
```

### Combining Modules
You can combine multiple modules to perform a comprehensive evaluation:

```python
from evaluate_module import evaluate_text, evaluate_images, evaluate_facts

# Path to the PDF file
pdf_path = "path/to/your/pdf_file.pdf"

# Perform evaluations
text_result = evaluate_text(pdf_path, model=model)
image_result = evaluate_images(pdf_path)
fact_result = evaluate_facts(pdf_path, model=model)

# Combine results
combined_result = {
    "text": text_result,
    "images": image_result,
    "facts": fact_result
}

print("Combined Evaluation Result:", combined_result)
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.