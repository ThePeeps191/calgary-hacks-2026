from .bias_correction import *
from .bias_detection import *
from .text_replacement import *

para = input()

paragraph = Paragraph(para)
paragraph.test_for_bias()

print(paragraph.is_text_biased_enough)
print(paragraph.unbiased_replacement)
print(paragraph.reason_biased)