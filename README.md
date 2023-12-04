[![OpenAI](https://a11ybadges.com/badge?logo=openai)](https://platform.openai.com/)
[![LangChain](https://a11ybadges.com/badge?text=LangChain&badgeColor=0834ac)](https://www.langchain.com/)
[![Pinecone](https://a11ybadges.com/badge?text=Pinecone&badgeColor=000000)](https://www.pinecone.io/)
[![Python](https://a11ybadges.com/badge?logo=python)](https://www.python.org/)
[![FullStackWithLawrence](https://a11ybadges.com/badge?text=FullStackWithLawrence&badgeColor=orange&logo=youtube&logoColor=282828)](https://www.youtube.com/@FullStackWithLawrence)

![GHA pushMain Status](https://img.shields.io/github/actions/workflow/status/FullStackWithLawrence/openai-embeddings/pushMain.yml?branch=main)
[![AGPL License](https://img.shields.io/github/license/overhangio/tutor.svg?style=flat-square)](https://www.gnu.org/licenses/agpl-3.0.en.html)
[![hack.d Lawrence McDaniel](https://img.shields.io/badge/hack.d-Lawrence%20McDaniel-orange.svg)](https://lawrencemcdaniel.com)

# OpenAI Embeddings Example

A Hybrid Search and Augmented Generation prompting solution using Python [OpenAI](https://openai.com/) API embeddings sourced from [Pinecone](https://docs.pinecone.io/docs/python-client) vector database indexes and managed by [LangChain](https://www.langchain.com/). Implements the following:

- **PDF Loader**. a command-line pdf loader program that extracts text, vectorizes, and
  loads into a Pinecone dot product vector database that is dimensioned to match OpenAI embeddings.
- **Retrieval Augments Generation**. A chatGPT prompt based on a hybrid search retriever that locates relevant documents from the vector database and includes these in OpenAI prompts.

## Installation

```console
git clone https://github.com/FullStackWithLawrence/openai-embeddings.git
cd openai-embeddings
make init
source venv/bin/activate
```

You'll also need to add your api keys to the .env file in the root of the repo.

- Get your [OpenAI API key](https://platform.openai.com/api-keys)
- Get your [Pinecone API Key](https://app.pinecone.io/)

```console
OPENAI_API_ORGANIZATION=PLEASE-ADD-ME
OPENAI_API_KEY=PLEASE-ADD-ME
PINECONE_API_KEY=PLEASE-ADD-ME
```

## Usage

```console
# example 1 - generic assistant
python3 -m models.examples.prompt "your are a helpful assistant" "What analytics and accounting courses does Wharton offer?"

# example 2 - assistant with improved system prompting
python3 -m models.examples.prompt "You are a student advisor at University of Pennsylvania. You provide concise answers of 100 words or less." "What analytics and accounting courses does Wharton offer?"

# example 3 - templated assistant: Online courses
python3 -m models.examples.online_courses "analytics and accounting"

# example 4 - templated assistant: Certification programs
python3 -m models.examples.certification_programs "analytics and accounting"

# example 5 - Retrieval Augmented Generation
python3 -m models.examples.load "/path/to/your/pdf/documents"
python3 -m models.examples.rag "What analytics and accounting courses does Wharton offer?"
```

### Retrieval Augmented Generation

For the question, _"What analytics and accounting courses does Wharton offer?"_ , an
embedding can potentially dramatically alter the response generated by chatGPT. To illustrate, I uploaded a batch of 21 sets of lecture notes in PDF format for an online analytics course taught by Wharton professor [Brian Bushee](https://accounting.wharton.upenn.edu/profile/bushee/). You can download these from https://cdn.lawrencemcdaniel.com/fswl/openai-embeddings-data.zip to test whether your results are consistent.

#### The control set

Example 1 above, a generic chatGPT prompt with no additional guidance provided by a system prompt nor an embedding, generates the following response:

```console
Wharton offers a variety of analytics and accounting courses. Some of the analytics courses include:

1. Introduction to Business Analytics: This course provides an overview of the fundamentals of business analytics, including data analysis, statistical modeling, and decision-making.

2. Data Visualization and Communication: This course focuses on the effective presentation and communication of data through visualizations and storytelling techniques.

3. Predictive Analytics: This course explores the use of statistical models and machine learning algorithms to predict future outcomes and make data-driven decisions.

4. Big Data Analytics: This course covers the analysis of large and complex datasets using advanced techniques and tools, such as Hadoop and Spark.

In terms of accounting courses, Wharton offers:

1. Financial Accounting: This course provides an introduction to the principles and concepts of financial accounting, including the preparation and analysis of financial statements.

2. Managerial Accounting: This course focuses on the use of accounting information for internal decision-making and planning, including cost analysis and budgeting.

3. Advanced Financial Accounting: This course delves into more complex accounting topics, such as consolidations, partnerships, and international accounting standards.

4. Auditing and Assurance Services: This course covers the principles and practices of auditing, including risk assessment, internal controls, and audit procedures.

These are just a few examples of the analytics and accounting courses offered at Wharton. The school offers a wide range of courses to cater to different interests and skill levels in these fields.
(venv) (base) mcdaniel@MacBookAir-Lawrence openai-embeddings % python3 -m models.examples.online_courses "analytics and accounting"
```

#### Same prompt but with an embedding

After creating an embedding from the sample set of pdf documents, you can prompt models.examples.rag with the same question, and it should provide a quite different response compared to the control from example 1. It should resemble the following:

```console
Wharton offers a variety of analytics and accounting courses. Some of the courses offered include:

1. Accounting-Based Valuation: This course, taught by Professor Brian Bushee, focuses on using accounting information to value companies and make investment decisions.

2. Review of Financial Statements: Also taught by Professor Brian Bushee, this course provides an in-depth understanding of financial statements and how to analyze them for decision-making purposes.

3. Discretionary Accruals Model: Another course taught by Professor Brian Bushee, this course explores the concept of discretionary accruals and their impact on financial statements and financial analysis.

4. Discretionary Accruals Cases: This course, also taught by Professor Brian Bushee, provides practical applications of the discretionary accruals model through case studies and real-world examples.

These are just a few examples of the analytics and accounting courses offered at Wharton. The school offers a wide range of courses in these areas to provide students with a comprehensive understanding of financial analysis and decision-making.
```

## Configuration defaults

Set these as environment variables on the command line, or in a .env file that should be located in the root of the repo.

```console
# OpenAI API
OPENAI_API_ORGANIZATION=PLEASE-ADD-ME
OPENAI_API_KEY=PLEASE-ADD-ME
OPENAI_CHAT_MAX_RETRIES=3
OPENAI_CHAT_MODEL_NAME=gpt-3.5-turbo
OPENAI_CHAT_TEMPERATURE=0.0
OPENAI_PROMPT_MODEL_NAME=text-davinci-003

# Pinecone API
PINECONE_API_KEY=PLEASE-ADD-ME
PINECONE_DIMENSIONS=1536
PINECONE_ENVIRONMENT=gcp-starter
PINECONE_INDEX_NAME=rag
PINECONE_METRIC=dotproduct
PINECONE_VECTORSTORE_TEXT_KEY=lc_id

# This package
DEBUG_MODE=False
```

## Contributing

This project uses a mostly automated pull request and unit testing process. See the resources in .github for additional details. You additionally should ensure that pre-commit is installed and working correctly on your dev machine by running the following command from the root of the repo.

```console
pre-commit run --all-files
```

Pull requests should pass these tests before being submitted:

```console
make test
```

### Developer setup

```console
git clone https://github.com/lpm0073/automatic-models.git
cd automatic-models
make init
make activate
```

### Github Actions

Actions requires the following secrets:

```console
PAT: {{ secrets.PAT }}  # a GitHub Personal Access Token
OPENAI_API_ORGANIZATION: {{ secrets.OPENAI_API_ORGANIZATION }}
OPENAI_API_KEY: {{ secrets.OPENAI_API_KEY }}
PINECONE_API_KEY: {{ secrets.PINECONE_API_KEY }}
PINECONE_ENVIRONMENT: {{ secrets.PINECONE_ENVIRONMENT }}
PINECONE_INDEX_NAME: {{ secrets.PINECONE_INDEX_NAME }}
```

## Additional reading

- [Youtube - Vector Embeddings Tutorial – Code Your Own AI Assistant with GPT-4 API + LangChain + NLP](https://www.youtube.com/watch?v=yfHHvmaMkcA)
- [Youtube - LangChain Explained in 13 Minutes | QuickStart Tutorial for Beginners](https://www.youtube.com/watch?v=aywZrzNaKjs)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings/what-are-embeddings)
- [What is a Vector Database?](https://www.pinecone.io/learn/vector-database/)
- [LangChain RAG](https://python.langchain.com/docs/use_cases/question_answering/)
- [LangChain Document Loaders](https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf)
- [LanchChain Caching](https://python.langchain.com/docs/modules/model_io/llms/llm_caching)
