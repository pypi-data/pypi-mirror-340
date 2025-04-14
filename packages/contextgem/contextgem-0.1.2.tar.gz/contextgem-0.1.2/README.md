![ContextGem](https://contextgem.dev/_static/contextgem_poster.png "ContextGem - Easier and faster way to build LLM extraction workflows through powerful abstractions")

# ContextGem: Easier and faster way to build LLM extraction workflows

[![tests](https://github.com/shcherbak-ai/contextgem/actions/workflows/ci-tests.yml/badge.svg?branch=main)](https://github.com/shcherbak-ai/contextgem/actions/workflows/ci-tests.yml)
[![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/SergiiShcherbak/daaee00e1dfff7a29ca10a922ec3becd/raw/coverage.json)](https://github.com/shcherbak-ai/contextgem/actions)
[![docs](https://github.com/shcherbak-ai/contextgem/actions/workflows/docs.yml/badge.svg?branch=main)](https://github.com/shcherbak-ai/contextgem/actions/workflows/docs.yml)
[![documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://shcherbak-ai.github.io/contextgem/)
[![License](https://img.shields.io/badge/License-Apache_2.0-bright.svg)](https://opensource.org/licenses/Apache-2.0)
![PyPI](https://img.shields.io/pypi/v/contextgem)
[![Python Versions](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/downloads/)
[![Code Security](https://github.com/shcherbak-ai/contextgem/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/shcherbak-ai/contextgem/actions/workflows/codeql.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat)](https://pycqa.github.io/isort/)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-blue?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)

ContextGem is a free, open-source LLM framework for easier, faster extraction of structured data and insights from documents through powerful abstractions.


## 💎 Why ContextGem?

Most popular LLM frameworks for extracting structured data from documents require extensive boilerplate code to extract even basic information. This significantly increases development time and complexity.

ContextGem addresses this challenge by providing a flexible, intuitive framework that extracts structured data and insights from documents with minimal effort. Complex, most time-consuming parts are handled with **powerful abstractions**, eliminating boilerplate code and reducing development overhead.

Read more on the project [motivation](https://contextgem.dev/motivation.html) in the documentation.


## 💡 With ContextGem, you can:

- **Extract structured data** from documents (text, images) with minimal code
- **Identify and analyze key aspects** (topics, themes, categories) within documents
- **Extract specific concepts** (entities, facts, conclusions, assessments) from documents
- **Build complex extraction workflows** through a simple, intuitive API
- **Create multi-level extraction pipelines** (aspects containing concepts, hierarchical aspects)

![ContextGem extraction example](https://contextgem.dev/_static/readme_code_snippet.png "ContextGem extraction example")


## ⭐ Key features

<table>
    <thead>
        <tr style="text-align: left; opacity: 0.8;">
            <th style="width: 75%">Built-in abstractions</th>
            <th style="width: 10%"><strong>ContextGem</strong></th>
            <th style="width: 15%">Other LLM frameworks*</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>
                Automated dynamic prompts
            </td>
            <td>✅</td>
            <td>❌</td>
        </tr>
        <tr>
            <td>
                Automated data modelling and validators
            </td>
            <td>✅</td>
            <td>❌</td>
        </tr>
        <tr>
            <td>
                Precise granular reference mapping (paragraphs & sentences)
            </td>
            <td>✅</td>
            <td>❌</td>
        </tr>
        <tr>
            <td>
                Justifications (reasoning backing the extraction)
            </td>
            <td>✅</td>
            <td>❌</td>
        </tr>
        <tr>
            <td>
                Neural segmentation (SaT)
            </td>
            <td>✅</td>
            <td>❌</td>
        </tr>
        <tr>
            <td>
                Multilingual support (I/O without prompting)
            </td>
            <td>✅</td>
            <td>❌</td>
        </tr>
        <tr>
            <td>
                Single, unified extraction pipeline (declarative, reusable, fully serializable)
            </td>
            <td>✅</td>
            <td>⚠️</td>
        </tr>
        <tr>
            <td>
                Grouped LLMs with role-specific tasks
            </td>
            <td>✅</td>
            <td>⚠️</td>
        </tr>
        <tr>
            <td>
                Nested context extraction
            </td>
            <td>✅</td>
            <td>⚠️</td>
        </tr>
        <tr>
            <td>
                Unified, fully serializable results storage model (document)
            </td>
            <td>✅</td>
            <td>⚠️</td>
        </tr>
        <tr>
            <td>
                Extraction task calibration with examples
            </td>
            <td>✅</td>
            <td>⚠️</td>
        </tr>
        <tr>
            <td>
                Built-in concurrent I/O processing
            </td>
            <td>✅</td>
            <td>⚠️</td>
        </tr>
        <tr>
            <td>
                Automated usage & costs tracking
            </td>
            <td>✅</td>
            <td>⚠️</td>
        </tr>
        <tr>
            <td>
                Fallback and retry logic
            </td>
            <td>✅</td>
            <td>✅</td>
        </tr>
        <tr>
            <td>
                Multiple LLM providers
            </td>
            <td>✅</td>
            <td>✅</td>
        </tr>
    </tbody>
</table>

✅ - fully supported - no additional setup required<br>
⚠️ - partially supported - requires additional setup<br>
❌ - not supported - requires custom logic

\* See [descriptions](https://contextgem.dev/motivation.html#the-contextgem-solution) of ContextGem abstractions and [comparisons](https://contextgem.dev/vs_other_frameworks.html) of specific implementation examples using ContextGem and other popular open-source LLM frameworks.


## 🧩 Core components

ContextGem's document-specific LLM extraction is built upon the following core components:

- 📄 **Document** model contains text and/or visual content representing a specific document. Examples:

    - _legal documents_: contracts, policies, terms of service
    - _financial documents_: invoices, receipts, bank statements, financial reports
    - _business documents_: proposals, business plans, marketing materials, presentations

- 📚 **Aspect** model contains text representing a defined area or topic within a document. Examples:

    - _contract aspects_: payment terms, termination clauses
    - _invoice aspects_: line-item breakdowns, tax details
    - _CV aspects_: work experience, education, skills


- 🧠 **Concept** model contains a unit of information or an entity, derived from an aspect or the broader document context. Examples:

    - _factual extractions_: a termination date in a contract, a total amount due in an invoice, or a certification in a CV
    - _analytical insights_: risk assessments, compliance evaluations
    - _reasoned conclusions_: determining whether a document meets specific criteria or answers particular questions

See other industry-specific examples in the table below:

![ContextGem component examples](https://contextgem.dev/_static/contextgem_component_examples.png "ContextGem component examples")

Read more on [how it works](https://contextgem.dev/how_it_works.html) in the documentation.


## 📦 Installation

```bash
pip install -U contextgem
```


## 🚀 Quick start

### Aspect extraction

```python
# Quick Start Example - Extracting payment terms from a document

import os

from contextgem import Aspect, Document, DocumentLLM

# Sample document text (shortened for brevity)
doc = Document(
    raw_text=(
        "SERVICE AGREEMENT\n"
        "SERVICES. Provider agrees to provide the following services to Client: "
        "Cloud-based data analytics platform access and maintenance...\n"
        "PAYMENT. Client agrees to pay $5,000 per month for the services. "
        "Payment is due on the 1st of each month. Late payments will incur a 2% fee per month...\n"
        "CONFIDENTIALITY. Both parties agree to keep all proprietary information confidential "
        "for a period of 5 years following termination of this Agreement..."
    ),
)

# Define the aspects to extract
doc.aspects = [
    Aspect(
        name="Payment Terms",
        description="Payment terms and conditions in the contract",
        # see the docs for more configuration options, e.g. sub-aspects, concepts, etc.
    ),
    # Add more aspects as needed
]
# Or use `doc.add_aspects([...])`

# Define an LLM for extracting information from the document
llm = DocumentLLM(
    model="openai/gpt-4o-mini",  # or another provider/LLM
    api_key=os.environ.get(
        "CONTEXTGEM_OPENAI_API_KEY"
    ),  # your API key for the LLM provider
    # see the docs for more configuration options
)

# Extract information from the document
doc = llm.extract_all(doc)  # or use async version `await llm.extract_all_async(doc)`

# Access extracted information in the document object
for item in doc.aspects[0].extracted_items:
    print(f"• {item.value}")
# or `doc.get_aspect_by_name("Payment Terms").extracted_items`

# Output (exact paragraphs from the document):
# • PAYMENT. Client agrees to pay $5,000 per month for the services. Payment is due on the 1st of each month. Late payments will incur a 2% fee per month...

```
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shcherbak-ai/contextgem/blob/main/dev/notebooks/readme/quickstart_aspect.ipynb)


### Concept extraction

```python
# Quick Start Example - Extracting anomalies from a document, with source references and justifications

import os

from contextgem import Document, DocumentLLM, StringConcept

# Sample document text (shortened for brevity)
doc = Document(
    raw_text=(
        "Consultancy Agreement\n"
        "This agreement between Company A (Supplier) and Company B (Customer)...\n"
        "The term of the agreement is 1 year from the Effective Date...\n"
        "The Supplier shall provide consultancy services as described in Annex 2...\n"
        "The Customer shall pay the Supplier within 30 calendar days of receiving an invoice...\n"
        "The purple elephant danced gracefully on the moon while eating ice cream.\n"  # 💎 anomaly
        "This agreement is governed by the laws of Norway...\n"
    ),
)

# Attach a document-level concept
doc.concepts = [
    StringConcept(
        name="Anomalies",  # in longer contexts, this concept is hard to capture with RAG
        description="Anomalies in the document",
        add_references=True,
        reference_depth="sentences",
        add_justifications=True,
        justification_depth="brief",
        # see the docs for more configuration options
    )
    # add more concepts to the document, if needed
    # see the docs for available concepts: StringConcept, JsonObjectConcept, etc.
]
# Or use `doc.add_concepts([...])`

# Define an LLM for extracting information from the document
llm = DocumentLLM(
    model="openai/gpt-4o-mini",  # or another provider/LLM
    api_key=os.environ.get(
        "CONTEXTGEM_OPENAI_API_KEY"
    ),  # your API key for the LLM provider
    # see the docs for more configuration options
)

# Extract information from the document
doc = llm.extract_all(doc)  # or use async version `await llm.extract_all_async(doc)`

# Access extracted information in the document object
print(
    doc.concepts[0].extracted_items
)  # extracted items with references & justifications
# or `doc.get_concept_by_name("Anomalies").extracted_items`

```
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shcherbak-ai/contextgem/blob/main/dev/notebooks/readme/quickstart_concept.ipynb)

---

See more examples in the documentation:

### Basic usage examples
- [Aspect Extraction from Document](https://contextgem.dev/quickstart.html#aspect-extraction-from-document)
- [Extracting Aspect with Sub-Aspects](https://contextgem.dev/quickstart.html#extracting-aspect-with-sub-aspects)
- [Concept Extraction from Aspect](https://contextgem.dev/quickstart.html#concept-extraction-from-aspect)
- [Concept Extraction from Document (text)](https://contextgem.dev/quickstart.html#concept-extraction-from-document-text)
- [Concept Extraction from Document (vision)](https://contextgem.dev/quickstart.html#concept-extraction-from-document-vision)
- [LLM chat interface](https://contextgem.dev/quickstart.html#lightweight-llm-chat-interface)

### Advanced usage examples
- [Extracting Aspects Containing Concepts](https://contextgem.dev/advanced_usage.html#extracting-aspects-with-concepts)
- [Extracting Aspects and Concepts from a Document](https://contextgem.dev/advanced_usage.html#extracting-aspects-and-concepts-from-a-document)
- [Using a Multi-LLM Pipeline to Extract Data from Several Documents](https://contextgem.dev/advanced_usage.html#using-a-multi-llm-pipeline-to-extract-data-from-several-documents)


## 🎯 Focused document analysis

ContextGem leverages LLMs' long context windows to deliver superior extraction accuracy from individual documents. Unlike RAG approaches that often [struggle with complex concepts and nuanced insights](https://www.linkedin.com/pulse/raging-contracts-pitfalls-rag-contract-review-shcherbak-ai-ptg3f), ContextGem capitalizes on [continuously expanding context capacity](https://arxiv.org/abs/2502.12962), evolving LLM capabilities, and decreasing costs. This focused approach enables direct information extraction from complete documents, eliminating retrieval inconsistencies while optimizing for in-depth single-document analysis. While this delivers higher accuracy for individual documents, ContextGem does not currently support cross-document querying or corpus-wide retrieval - for these use cases, modern RAG systems (e.g., LlamaIndex, Haystack) remain more appropriate.


## 🤖 Supported LLMs

ContextGem supports both cloud-based and local LLMs through [LiteLLM](https://github.com/BerriAI/litellm) integration:
- **Cloud LLMs**: OpenAI, Anthropic, Google, Azure OpenAI, and more
- **Local LLMs**: Run models locally using providers like Ollama, LM Studio, etc.
- **Simple API**: Unified interface for all LLMs with easy provider switching


## ⚡ Optimizations

ContextGem documentation offers guidance on optimization strategies to maximize performance, minimize costs, and enhance extraction accuracy:

- [Optimizing for Accuracy](https://contextgem.dev/optimizations/optimization_accuracy.html)
- [Optimizing for Speed](https://contextgem.dev/optimizations/optimization_speed.html)
- [Optimizing for Cost](https://contextgem.dev/optimizations/optimization_cost.html)
- [Dealing with Long Documents](https://contextgem.dev/optimizations/optimization_long_docs.html)
- [Choosing the Right LLM(s)](https://contextgem.dev/optimizations/optimization_choosing_llm.html)


## 📚 Documentation

Full documentation is available at [contextgem.dev](https://contextgem.dev).

A raw text version of the full documentation is available at [`docs/docs-raw-for-llm.txt`](https://github.com/shcherbak-ai/contextgem/blob/main/docs/docs-raw-for-llm.txt). This file is automatically generated and contains all documentation in a format optimized for LLM ingestion (e.g. for Q&A).


## 🗨️ Community

If you have a feature request or a bug report, feel free to [open an issue](https://github.com/shcherbak-ai/contextgem/issues/new) on GitHub. If you'd like to discuss a topic or get general advice on using ContextGem for your project, start a thread in [GitHub Discussions](https://github.com/shcherbak-ai/contextgem/discussions/new/).


## 🤝 Contributing

We welcome contributions from the community - whether it's fixing a typo or developing a completely new feature! To get started, please check out our [Contributor Guidelines](https://github.com/shcherbak-ai/contextgem/blob/main/CONTRIBUTING.md).


## 🗺️ Roadmap

ContextGem is at an early stage. Our development roadmap includes:

- **Enhanced Analytical Abstractions**: Building more sophisticated analytical layers on top of the core extraction workflow to enable deeper insights and more complex document understanding
- **API Simplification**: Continuing to refine and streamline the API surface to make document analysis more intuitive and accessible
- **Terminology Refinement**: Improving consistency and clarity of terminology throughout the framework to enhance developer experience

We are committed to making ContextGem the most effective tool for extracting structured information from documents.


## 🔐 Security

This project is automatically scanned for security vulnerabilities using [CodeQL](https://codeql.github.com/). We also use [Snyk](https://snyk.io) as needed for supplementary dependency checks.

See [SECURITY](https://github.com/shcherbak-ai/contextgem/blob/main/SECURITY.md) file for details.


## 🙏 Acknowledgements

ContextGem relies on these excellent open-source packages:

- [pydantic](https://github.com/pydantic/pydantic): The gold standard for data validation
- [Jinja2](https://github.com/pallets/jinja): Fast, expressive template engine that powers our dynamic prompt rendering
- [litellm](https://github.com/BerriAI/litellm): Unified interface to multiple LLM providers with seamless provider switching
- [wtpsplit](https://github.com/segment-any-text/wtpsplit): State-of-the-art text segmentation tool
- [loguru](https://github.com/Delgan/loguru): Simple yet powerful logging that enhances debugging and observability
- [python-ulid](https://github.com/mdomke/python-ulid): Efficient ULID generation
- [PyTorch](https://github.com/pytorch/pytorch): Industry-standard machine learning framework
- [aiolimiter](https://github.com/mjpieters/aiolimiter): Powerful rate limiting for async operations


## 📄 License & Contact

This project is licensed under the Apache 2.0 License - see the [LICENSE](https://github.com/shcherbak-ai/contextgem/blob/main/LICENSE) and [NOTICE](https://github.com/shcherbak-ai/contextgem/blob/main/NOTICE) files for details.

Copyright © 2025 [Shcherbak AI AS](https://shcherbak.ai), an AI engineering company building tools for AI/ML/NLP developers.

Shcherbak AI is now part of Microsoft for Startups.

[Connect with us on LinkedIn](https://www.linkedin.com/in/sergii-shcherbak-10068866/) for questions or collaboration ideas.

Built with ❤️ in Oslo, Norway.
