from .bias_detection import get_bias_score
from .bias_correction import correct_bias

BIAS_SCORE_CUTOFF = 10.0

def segment_paragraphs(text):
    """
    Segments article text into Paragraph objects.
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
            paragraphs.append(Paragraph(para_text))
    
    return paragraphs

class Paragraph:
    text = ""
    bias_score = 0.0
    unbiased_replacement = ""
    reason_biased = ""
    def __init__(self, text):
        self.text = text
    def test_for_bias(self):
        bias_score = get_bias_score(self.text)
        if bias_score > BIAS_SCORE_CUTOFF:
            self.unbiased_replacement, self.reason_biased = correct_bias(self.text)