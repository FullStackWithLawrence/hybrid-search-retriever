# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods
"""Sales Support Model (SSM) for the LangChain project."""

import os
from typing import ClassVar, List

import pinecone
from dotenv import find_dotenv, load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage  # AIMessage (not used)
from langchain.text_splitter import Document, RecursiveCharacterTextSplitter
from langchain.vectorstores.pinecone import Pinecone
from pydantic import BaseModel, ConfigDict, Field  # ValidationError


# pylint: disable=duplicate-code
dotenv_path = find_dotenv()
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path, verbose=True)
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
    OPENAI_API_ORGANIZATION = os.environ["OPENAI_API_ORGANIZATION"]
    PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
    PINECONE_ENVIRONMENT = os.environ["PINECONE_ENVIRONMENT"]
    PINECONE_INDEX_NAME = os.environ["PINECONE_INDEX_NAME"]
else:
    raise FileNotFoundError("No .env file found in root directory of repository")

DEFAULT_MODEL_NAME = "text-davinci-003"
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)


class NetecPromptTemplates:
    """Netec Prompt Templates."""

    sales_role: str = """You are a helpful sales assistant at Netec who sells
        specialized training and exam preparation services to existing customers.
        You provide concise explanations of the services that Netec offers in 100
        words or less."""

    @classmethod
    def get_properties(cls):
        """return a list of properties of this class."""
        return [attr for attr in dir(cls) if isinstance(getattr(cls, attr), property)]

    @property
    def training_services(self) -> PromptTemplate:
        """Get prompt."""
        template = (
            self.sales_role
            + """
        Explain the training services that Netec offers about {concept}
        """
        )
        return PromptTemplate(input_variables=["concept"], template=template)

    @property
    def oracle_training_services(self) -> PromptTemplate:
        """Get prompt."""
        template = (
            self.sales_role
            + """
        Note that Netec is the exclusive provide of Oracle training services
        for the 6 levels of Oracle Certification credentials: Oracle Certified Junior Associate (OCJA),
        Oracle Certified Associate (OCA), Oracle Certified Professional (OCP),
        Oracle Certified Master (OCM), Oracle Certified Expert (OCE) and
        Oracle Certified Specialist (OCS).
        Summarize their programs for {concept}
        """
        )
        return PromptTemplate(input_variables=["concept"], template=template)


class SalesSupportModel(BaseModel):
    """Sales Support Model (SSM)."""

    Config: ClassVar = ConfigDict(arbitrary_types_allowed=True)

    # prompting wrapper
    chat: ChatOpenAI = Field(
        default_factory=lambda: ChatOpenAI(
            api_key=OPENAI_API_KEY,
            organization=OPENAI_API_ORGANIZATION,
            max_retries=3,
            model="gpt-3.5-turbo",
            temperature=0.3,
        )
    )

    # embeddings
    text_splitter: RecursiveCharacterTextSplitter = Field(
        default_factory=lambda: RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=0,
        )
    )

    texts_splitter_results: List[Document] = Field(None, description="Text splitter results")
    pinecone_search: Pinecone = Field(None, description="Pinecone search")
    pinecone_index_name: str = Field(default="netec-ssm", description="Pinecone index name")
    openai_embedding: OpenAIEmbeddings = Field(default_factory=lambda: OpenAIEmbeddings(model="ada"))
    query_result: List[float] = Field(None, description="Vector database query result")

    def cached_chat_request(self, system_message: str, human_message: str) -> SystemMessage:
        """Cached chat request."""
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=human_message),
        ]
        # pylint: disable=not-callable
        return self.chat(messages)

    def prompt_with_template(self, prompt: PromptTemplate, concept: str, model: str = DEFAULT_MODEL_NAME) -> str:
        """Prompt with template."""
        llm = OpenAI(model=model)
        retval = llm(prompt.format(concept=concept))
        return retval

    def split_text(self, text: str) -> List[Document]:
        """Split text."""
        # pylint: disable=no-member
        retval = self.text_splitter.create_documents([text])
        return retval

    def embed(self, text: str) -> List[float]:
        """Embed."""
        texts_splitter_results = self.split_text(text)
        embedding = texts_splitter_results[0].page_content
        # pylint: disable=no-member
        self.openai_embedding.embed_query(embedding)

        self.pinecone_search = Pinecone.from_documents(
            texts_splitter_results,
            embedding=self.openai_embedding,
            index_name=self.pinecone_index_name,
        )

    def embedded_prompt(self, prompt: str) -> List[Document]:
        """Embedded prompt."""
        result = self.pinecone_search.similarity_search(prompt)
        return result
