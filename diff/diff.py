import difflib

def html_diff(original, edited):
    orig_words = original.split()
    edit_words = edited.split()
    
    matcher = difflib.SequenceMatcher(None, orig_words, edit_words)
    output = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            output.append(" ".join(edit_words[j1:j2]))
        elif tag == 'insert':
            output.append(f"<span class='inserted'>{' '.join(edit_words[j1:j2])}</span>")
        elif tag == 'replace':
            removed = f"<span class='deleted'>{' '.join(orig_words[i1:i2])}</span>"
            added = f"<span class='inserted'>{' '.join(edit_words[j1:j2])}</span>"
            output.append(f"{removed} {added}")
        elif tag == 'delete':
            output.append(f"<span class='deleted'>{' '.join(orig_words[i1:i2])}</span>")

    return " ".join(output)

if __name__ == "__main__":
    old_text = "The dog sat on the mat."
    new_text = "The big dog sat on the red rug."

    print(html_diff(old_text, new_text))