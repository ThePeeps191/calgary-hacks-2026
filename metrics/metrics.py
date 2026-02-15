import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification

print("metrics.py imports finished")

# Load pretrained emotion model
MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, use_safetensors=True)
model.eval()

EMOTIONS = ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]
EMOTION_WEIGHTS = {
    "anger": 2,
    "disgust": 1.6,
    "fear": 1.5,
    "sadness": 1.2,
    "surprise": 1.1,
    "joy": 0.6,
    "neutral": 0.0
}
POWER_WORDS = {
    "crisis","collapse","destroy","disaster","radical","chaos",
    "emergency","war","threat","ruin","breakdown","catastrophe",
    "devastating","apocalypse","terror","violent","extreme",
    "corrupt","evil","outrage","attack","invasion","fuck","bad","horrendous","terrible","unjustified"
}
ABSOLUTIST = {"everything","nothing","always","never","all","none","everyone","nobody","everytime","rarely"}

def _emotion_probs(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )
    with torch.no_grad():
        logits = model(**inputs).logits
    probs = torch.softmax(logits, dim=-1).cpu().numpy()[0]
    return dict(zip(EMOTIONS, probs))

def narrative_intensity(text): # 0-1
    words = text.lower().split()
    n = max(1, len(words))

    power = sum(1 for w in words if w.strip(".,!?") in POWER_WORDS)
    absolute = sum(1 for w in words if w.strip(".,!?") in ABSOLUTIST)

    score = 2 * (power * 2 + absolute) / n
    return min(1.0, score * 4)

def get_drama_index(text):
    """
    Returns Drama Index from 1 to 100 for any article or speech
    Higher = more emotionally intense or manipulative
    """
    emotions = _emotion_probs(text)
    emotions100 = {}
    for k in emotions:
        emotions100[k] = int(emotions[k] * 100)
    emotional = sum(emotions[e] * EMOTION_WEIGHTS[e] for e in emotions) / sum(EMOTION_WEIGHTS.values())

    base = emotional ** 0.6 * 70
    narrative = narrative_intensity(text)
    boosted = base * (1 + narrative)
    capped = min(50, boosted)
    final = int(round(capped * 2))

    return [min(100, max(1, min(100, final)) * 2), emotions100]

if __name__ == "__main__":
    tests = [
        "The economy is collapsing and families are in crisis as radical policies destroy everything.",
        "The inflation rate increased by 0.3% in the last quarter.",
        """
For Ashley Garley, the past year has been “messy, challenging and heartbreaking.”

Garley, a former contractor and malaria expert with the US Agency for International Development, was among the first people impacted by the Department of Government Efficiency’s massive shrinking of the federal workforce last year, led by billionaire Elon Musk, which began almost immediately after President Donald Trump returned to the White House.

Garley, who lost her job after the US froze all foreign aid in late January 2025, is struggling to find a full-time job with benefits more than a year later. To contribute to the bills, she has returned to a job she held in her teens and 20s: swim instructor.

Going from a jet-setting job with global impact, to teaching part-time at her county pool in Maryland has been “pretty emotional,” Garley told CNN.

Like Garley, hundreds of thousands of federal workers and contractors have had their lives upended by Trump’s quest to clamp down on the federal workforce, whom he sees as a threat to his ability to execute his priorities.

More than 350,000 workers have left the federal government’s payroll since the president started his second term on January 20, 2025, according to the Office of Personnel Management.

After accounting for new hires, the federal workforce shrunk by 242,000 people – or just over 10% – between his inauguration day and December. Nearly 2.1 million federal civilian employees remain.

Trump said last month that he doesn’t feel bad about the downsizing, claiming without evidence that former federal workers are now making more money in the private sector.

But that’s not been everyone’s experience. CNN spoke with several former federal workers who were laid off or accepted buyouts amid DOGE’s aggressive and controversial cuts last year. Some of them, like Garley, have struggled to find a job and pay the bills. Meanwhile, others have pivoted careers, moved across the country for new jobs or are dedicating their time to volunteer work – and finding a silver lining in their new lives.

Here are some of their stories:

Emotional toll

The stress of losing her dream job at the Centers for Disease Control and Prevention landed Morgan Hall in the hospital.

A few months after she received her final paycheck in August, Hall told CNN that she had been in bed for days without eating or answering the phone. Her son ultimately found her, and she was hospitalized in October for 10 days with severe depression, anxiety, and physical complications tied to a preexisting medical condition that can be worsened by stress.

Hall – who worked as an analyst for CDC’s violence prevention division – was initially placed on administrative leave on February 14, 2025, and later terminated as part of the sweeping layoffs known as a “reduction in force,” or RIFs. She is among the 10,500 people across agencies who were affected by RIFs.

Hall says she has fallen behind on bills, which includes roughly $57,000 in hospital costs. For two months, she relied on food stamps to buy groceries, sought state assistance for utilities, and a relative helped cover her mortgage so she would not lose her home.

In January, Hall began a temporary 12-week stint that placed her back at CDC, working through a contractor. However, she says she is still unable to meet her expenses. She is also continuing to apply for jobs, submitting at least five applications on most days.

“My hope and prayer is that one day I can go back and continue to complete my mission at CDC,” Hall told CNN, adding “I feel like a part of me is gone.”

Grueling job search

When Casey Hollowell decided to take the second buyout offer, known as the deferred resignation program, from the US Department of Agriculture in April, he figured he’d have no trouble finding a job by the time his federal paychecks would stop at the end of September.

An Army veteran who served in Iraq, Hollowell hadn’t wanted to leave his post as an investigative analyst but felt he had no job security after being laid off in the administration’s purge of probationary workers last February and then reinstated by a federal judge.

Initially, he thought he could be picky, looking for remote jobs so he could stay in Biloxi, Mississippi, close to his teenage son. But Hollowell, 40, grew concerned after applying for multiple positions and not getting any responses. So he widened his search, applying to as many as 30 jobs a day, including ones that were in-person or part-time or entry level.

Though his grandparents helped him cover his bills, the fruitless job hunt weighed on him. He stopped hanging out with his friends because he felt he couldn’t afford it.

“I became a hermit,” said Hollowell. “I just stayed at home, like, all the time.”

Then in December, he got a big break. Hollowell applied for a data analyst position at an insurance claims management company, and less than a week later, he was asked to interview. He started on February 2, nearly one year to the day after his initial layoff from USDA.

Now Hollowell is making some other big changes. He just put an offer on a house, which was accepted. And the whole ordeal prompted him to switch from being Republican to an independent.

Similarly, Kit Rees, a former investigator at the Department of Justice’s Civil Rights Division, also accepted the administration’s second deferred resignation offer and ended their tenure in the federal government in September.

Rees’ journey to securing a full-time job in their field has been difficult and tiring, they told CNN.

Before their federal paychecks stopped, Rees began piecing together whatever work they could find. They picked up a job at an ACE Hardware store in May 2025 and found part-time work with a restoration construction company, filling in on job sites when it needed additional help.

The jobs didn’t pay nearly as much as their federal government salary but it gave Rees the mental break they said they needed.

“It was healing, lifting mulch, helping people match screws and working through house projects,” Rees said. The customer service job allowed them to talk “to dozens of people,” and those conversations reminded them “that tragedies don’t happen to everybody.”

However, struggling to pay the bills, Rees took out a $15,000 loan.

Just weeks away from asking their family for financial help, Rees secured a job in their field earlier this month.

“It’s more than a $30,000 pay cut. But it’s still the best offer that I’ve gotten,” they told CNN.

Rees said they are cautious about feeling relieved after securing the job.

Changing careers

After accepting a deferred resignation offer, Steve Leibman says he was lucky to be at the point of his career where he didn’t feel immediate pressure to take a new job right away. He took some consulting work and helped a non-profit, but it was his trek on Mount Kilimanjaro in Tanzania that changed his perspective on his next real move.

Leibman – who worked remotely from the Boston area at the US Digital Service, which later formally turned into DOGE – is now enrolled in a teacher license program at Harvard University. The program is a one-year master’s degree, after which he hopes to teach high school math.

“A big part of it was just interacting with people whose perspective of the world are just different and gives a different view of how can you have impact in the world,” Liebman told CNN about his trip.

Meanwhile, David Schwark began looking for another job when a court order brought him back to the Department of Education’s Office for Civil Rights in Cleveland after he had been laid off in March 2025. He was uncertain when he would be formally let go.

The Department of Education was the second hardest hit agency in the federal government overhaul, losing 49% of its staff, according to OPM. Meanwhile, agencies that are a higher priority for Trump were shielded. For instance, staffing at the Department of Homeland Security only dipped 11%.

Schwark, who was a prosecutor before he joined the Department of Education, is now a magistrate in a local municipal court in Lakewood, Ohio.

“It’s a lot different. I loved my job with Ed,” Schwark told CNN. “It’s been a big shift to go back to dealing with criminal law and being in the court room for a long time.”

When Cameron Hilaker was laid off as an emergency manager at USAID, his wife was six-months pregnant with their first born. Their son is now eight months old and Hilaker still has not found work. He has defaulted to being a stay-at-home-dad.

“I’m very happy to be a stay-at-home dad, don’t get me wrong by any means, but this was never anywhere in our sketch of what our life would look like.”

Hilaker says his family is really starting to feel the crunch financially and are considering moving out of Washington, DC, for a better cost-of-living.

“I feel burned by Elon Musk and DOGE,” Hilaker, a member of AFGE Local 1534 union, told CNN. “They came in, they said they were going to slash and burn the federal government, they were going to reduce the deficit.”

For Vi Le, a former behavioral scientist and violence prevention researcher at the CDC, finding a new role has become its own full-time job.

She has a small contract related to violence prevention, but it is not enough to replace her previous salary. Until she finds a job in her field, Le told CNN that she is trying to expand a hobby business designing floral arrangements for events.

“For now, flowers might be the full-time job, and my career might be the hobby,” Le said.

Cross-country moves

After losing his DC-based contractor job at USAID, Nathan Karrel said he “went straight into survival mode.” He found a new role with the city of Tucson, Arizona, where he knew nobody – and moved there “sight unseen.”

“I’m not in international development anymore, which was my plan,” said Karrel, 42. “But I really love Tucson, except for the heat. It’s a whole different culture than DC. The food scene is amazing. The people are kind, and the mountains are great. Now I know all about mesquite trees and cacti.”

He is one of several federal employees who told CNN that the Trump-era cuts were so disruptive to their lives that they moved across the country – highlighting the nationwide impact of DOGE, which affected communities far beyond DC where the bulk of federal workers live.

CivicMatch, a jobs platform that connected nearly 190 former federal workers to new jobs last year at state and local governments, said roughly 33% of those people moved to a new state, and 10% did cross-country moves.

One of these people moved all the way from DC to Honolulu, Hawaii. An employee from the Department of Interior moved from Pennsylvania to Oregon. A federal health official moved from Texas to Richmond, Virginia.

“As the federal government retrenches, the work obviously does not disappear. It shifts to cities and states,” CivicMatch founder Caitlin Lewis said. “This has become a talent redistribution engine, to the benefit of local governments. Federal workers were desperate to continue serving.”

Heading back home

Lucas King, 36, who was also a USAID contractor, relocated from DC to Idaho, where he grew up. He previously managed some of USAID’s largest projects in Africa, including initiatives from Trump’s first term. Now he oversees permits and inspections for Ketchum, Idaho, a ski town with 3,600 residents.

“I wasn’t getting traction in DC, so we moved back to Idaho,” King said. “My new boss was clear that this was kind of a step down, given my experience. It was traumatic, but it worked out. I feel lucky that I found a place to live, a good employer, with good benefits, and I’m back with family and friends.”

The DOGE layoffs also sent Nathaniel Haight on a path closer to family.

He started as an intern at USAID in 2015, and worked his way up over 10 years, handling grants and contracts. But after getting swept up in the dismantling of USAID, he cast a wide net during his job search, looking far beyond DC, so he could start providing again for his wife and four children.

He landed a new role handling grants for the city of Indianapolis, which came as a relief. His parents and four siblings live in Indiana. His kids had to switch to new schools, but they now have much deeper bonds with their cousins, he said.

“I found a new job in public service, much closer to my parents and siblings,” Haight said. “I’m seeing a lot of positives that have come out of it.”

Continuing the mission

After being placed on administrative leave from USAID, Julianne Weis began going to Capitol Hill to stress the impacts of the agency’s funding cuts and advocate for foreign aid to be restored. She co-founded Aid on the Hill, a volunteer advocacy organization.

Weis worked in USAID’s global health bureau, particularly in the areas of family planning and reproductive health. She eventually was formally terminated from the agency as part of reduction in force efforts.

These days, Weis spends most of her week meeting with congressional staffers — sometimes virtually and other times, taking her kids along to Capitol Hill.

Weis will be starting a full-time job soon, and she shared with CNN that she plans on having “a side role in helping” Aid on the Hill in her own time.

Similarly, as Deborah Kaliel – who worked at USAID’s Office of HIV/AIDS – searches for a job, she is dedicating her time as a volunteer for Crisis in Care, a fundraising effort she co-founded to provide support for HIV services in other countries.

“That has kind of taken over my life,” Kaliel told CNN. She added: “It’s been really rewarding and, and a really wonderful way for me to stay engaged with the topic and the people and the communities that I’m most passionate about.”
"""
    ]

    for t in tests:
        print("\nTEXT:", t)
        print("Drama Index:", get_drama_index(t))