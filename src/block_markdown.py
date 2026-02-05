def markdown_to_blocks(markdown):
    # Split by double newlines to separate blocks
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        # Strip leading/trailing whitespace
        block = block.strip()
        # Skip empty strings (this handles cases with 3+ newlines)
        if block == "":
            continue
        filtered_blocks.append(block)
    return filtered_blocks