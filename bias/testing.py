from .bias_correction import *
from .bias_detection import *
from .text_replacement import *

if __name__ == "__main__":
    test_text = "Repeat Violent Offender DeCarlos Brown Jr. was put on the streets by Radical Roy Cooper, and his soft-on-crime agenda. He then went on to BRUTALLY murder Iryna Zarutska aboard the Charlotte light rail."
    print("Testing bias detection:")
    print(is_text_biased_enough(test_text))
    print("Testing bias correction:")
    unbiased, reason = correct_bias(test_text)
    print("Unbiased replacement:", unbiased)
    print("Reason for bias:", reason)