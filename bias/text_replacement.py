from .bias_detection import is_text_biased_enough
from .bias_correction import correct_bias
import diff

def segment_paragraphs(text):
    """
    Segments article text into Paragraph objects, then tests each for bias.
    Splits by newlines (paragraph breaks).
    """
    paragraphs = []
    
    # Split by double newlines to get paragraphs
    raw_paragraphs = text.split('\n')
    
    for para_text in raw_paragraphs:
        # Strip whitespace from each paragraph
        para_text = para_text.strip()
        
        # Skip empty paragraphs
        if para_text:
            paragraph = Paragraph(para_text)
            paragraph.test_for_bias()
            paragraphs.append(paragraph)
    
    return paragraphs

class Paragraph:
    def __init__(self, text):
        self.text = text
        self.is_text_biased_enough = False
        self.unbiased_replacement = ""
        self.reason_biased = ""
        self.html_diff = ""
    def test_for_bias(self):
        if is_text_biased_enough(self.text):
            self.is_text_biased_enough = True
            self.unbiased_replacement, self.reason_biased = correct_bias(self.text)
            self.html_diff = diff.html_diff(self.text, self.unbiased_replacement)
    def json(self):
        return {
            "text": self.text,
            "is_text_biased_enough": self.is_text_biased_enough,
            "unbiased_replacement": self.unbiased_replacement,
            "reason_biased": self.reason_biased,
            "html_diff": self.html_diff
        }