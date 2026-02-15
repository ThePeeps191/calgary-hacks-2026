from .bias_correction import *
from .bias_detection import *
from .text_replacement import *

if __name__ == "__main__":
    test_text = "As everyone knows, the Country of Canada has treated the United States very unfairly for decades. Now, things are turning around for the U.S.A., and FAST! But imagine, Canada is building a massive bridge between Ontario and Michigan. They own both the Canada and the United States side and, of course, built it with virtually no U.S. content. President Barack Hussein Obama stupidly gave them a waiver so they could get around the BUY AMERICAN Act, and not use any American products, including our Steel. Now, the Canadian Government expects me, as President of the United States, to PERMIT them to just “take advantage of America!” What does the United States of America get — Absolutely NOTHING! Ontario won't even put U.S. spirits, beverages, and other alcoholic products, on their shelves, they are absolutely prohibited from doing so and now, on top of everything else, Prime Minister Carney wants to make a deal with China — which will eat Canada alive. We’ll just get the leftovers! I don't think so. The first thing China will do is terminate ALL Ice Hockey being played in Canada, and permanently eliminate The Stanley Cup. The Tariffs Canada charges us for our Dairy products have, for many years, been unacceptable, putting our Farmers at great financial risk. I will not allow this bridge to open until the United States is fully compensated for everything we have given them, and also, importantly, Canada treats the United States with the Fairness and Respect that we deserve. We will start negotiations, IMMEDIATELY. With all that we have given them, we should own, perhaps, at least one half of this asset. The revenues generated because of the U.S. Market will be astronomical. Thank you for your attention to this matter!"
    print("Testing bias detection:")
    print(is_text_biased_enough(test_text))
    print("Testing bias correction:")
    unbiased, reason = correct_bias(test_text)
    print("Unbiased replacement:", unbiased)
    print("Reason for bias:", reason)