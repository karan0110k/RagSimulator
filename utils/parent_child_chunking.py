def create_parent_child_chunks(text, parent_size=2000, child_size=500, overlap=100):

    parents = []
    children = []
    mapping = {}

    start = 0
    parent_id = 0

    while start < len(text):

        parent_text = text[start:start+parent_size]
        parents.append(parent_text)

        child_start = 0
        child_id = 0

        while child_start < len(parent_text):
            child_text = parent_text[child_start:child_start+child_size]

            children.append(child_text)
            mapping[len(children)-1] = parent_id

            child_start += child_size - overlap
            child_id += 1

        start += parent_size
        parent_id += 1

    return parents, children, mapping