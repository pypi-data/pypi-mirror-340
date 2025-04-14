AGENTIC_CHUNKER_PROMPT = """
    You are an advanced AI system designed to improve the quality and context of text chunks. Your task is to analyze two consecutive text chunks and enhance the current chunk by incorporating relevant context from the previous chunk. Follow these steps:

    1. Read and understand the previous chunk (Chunk A) and the current chunk (Chunk B).

    2. Identify prepositions in Chunk B that could benefit from additional context.

    3. Replace or expand these prepositions with relevant information from Chunk A to improve clarity and coherence.

    4. Look for other opportunities to enhance Chunk B by incorporating context from Chunk A, such as:
    - Resolving pronouns or ambiguous references
    - Adding relevant background information
    - Clarifying relationships between entities or concepts

    5. Ensure that the modified Chunk B remains coherent and doesn't become overly verbose.

    6. Maintain the original meaning and intent of Chunk B while improving its quality and context.

    7. If no improvements are necessary or possible, state that the chunk remains unchanged.

    Example input:
    Chunk A: "The old house on the hill had stood for centuries, weathering storms and time."
    Chunk B: "Inside, the floorboards creaked under his feet as he explored."

    Return JSON format:
    {{
        "output": enhanced_text,
    }}

    Example response:
    {{
        "output": "Inside the old house on the hill, the floorboards creaked under his feet as he explored the centuries-old structure.",
    }}

    Now, please process the following chunks:

    Chunk A: {previous_chunk}
    Chunk B: {current_chunk}

    Provide the enhanced version of Chunk B, incorporating relevant context from Chunk A.
"""