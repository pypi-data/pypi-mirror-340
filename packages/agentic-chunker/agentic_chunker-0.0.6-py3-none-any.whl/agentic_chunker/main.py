from openai import OpenAI
import copy
import json
from tqdm import tqdm

from . import prompts

class AgenticChunker:
    def __init__(self, api_key: str, model: str, base_url = None):
        if base_url:
            self.client = OpenAI(base_url=base_url, api_key=api_key)
        else:
            self.client = OpenAI(api_key=api_key)
        self.model = model


    def validate_response(self, response: str) -> dict:
        try:
            data = json.loads(response)
            assert "output" in data, "Missing 'output' field"
            return data
        except (json.JSONDecodeError, AssertionError) as e:
            raise ValueError(f"Invalid JSON format: {str(e)}")

    def _rechunk(self, previous_chunk, current_chunk) -> str:
        prompt = prompts.AGENTIC_CHUNKER_PROMPT.format(
            previous_chunk=previous_chunk,
            current_chunk=current_chunk
        )
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        processed_response = self.validate_response(response.choices[0].message.content)
        if processed_response:
            processed_chunk = processed_response['output']
            return processed_chunk
        else:
            raise f"Error at chunk: {current_chunk[:40]}..."
    
    def agentic_chunking(self, text: str, seperator: str) -> list:
        chunks = []
        original_chunks = text.split(seperator)
        current_chunk = None
        previous_chunk = None
        for chunk in tqdm(original_chunks, desc="Processing Chunks", unit="chunk"):
            current_chunk = chunk
            if not previous_chunk:
                previous_chunk = current_chunk
                chunks.append(current_chunk)
            else:
                processed_chunk = self._rechunk(previous_chunk, current_chunk)
                if processed_chunk:
                    chunks.append(processed_chunk)
                    previous_chunk = processed_chunk
        return chunks 
    
    def rechunk_langchain_chunks(self, chunks: list, ) -> list:
        modified_chunks = copy.deepcopy(chunks)
        current_chunk = None
        previous_chunk = None
        for i, chunk in tqdm(enumerate(chunks), desc="Processing Chunks", unit="chunk", total=len(chunks)):
            current_chunk = chunk
            modified_chunk = modified_chunks[i]
            if not previous_chunk:
                previous_chunk = current_chunk
                modified_chunk.metadata['original_chunk'] = current_chunk.page_content
            else:
                processed_chunk = self._rechunk(
                    previous_chunk,
                    current_chunk.page_content
                )
                if processed_chunk:
                    modified_chunk.metadata['original_chunk'] = current_chunk.page_content
                    modified_chunk.page_content = processed_chunk
                    previous_chunk = processed_chunk
        return modified_chunks