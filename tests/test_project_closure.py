from helper import process
import json


CONTENT = """
PM (Sarah): Good morning, everyone. Thanks for joining this meeting. Today, we’re officially wrapping up the GreenTech project. I want to first thank all of you for your hard work and dedication. Let’s go over the reasons for closing this project and ensure we document everything properly.

TL (James): Thanks, Sarah. It’s great to see this project reach its conclusion. What are the primary reasons we’re wrapping it up now?

PM (Sarah): There are three main reasons. First, we’ve achieved all the project objectives outlined at the beginning. The GreenTech platform is fully operational, and the client is thrilled with the results.

QA (Priya): That’s true. Our final testing report showed a 98% success rate across all use cases, and the client signed off on the last round of UAT last week.

PM (Sarah): Exactly. The second reason is resource optimization. Now that this project is complete, we can reallocate team members to the next priority initiatives, like the BlueSky project.

Dev (Michael): Makes sense. We’ve been discussing how the features we built here could be adapted for BlueSky, so the timing works well.

PM (Sarah): Absolutely. The third reason is cost efficiency. Extending the project would increase maintenance costs, but the handover plan ensures the client can manage the system independently.

TL (James): Good point. We’ve provided detailed documentation and trained their internal IT team, so they’re ready to take over.

QA (Priya): That’s true. And the feedback from the training sessions was positive. They feel confident managing the platform.

PM (Sarah): Great work, everyone. Before we close, are there any final tasks or loose ends we need to address?

Dev (Michael): I think we’re all set. The code repository has been transferred, and the servers are running smoothly.

QA (Priya): No issues from my side. Everything is documented and archived.

TL (James): Same here. All deliverables are complete.

PM (Sarah): Perfect. Then let’s officially close the project. I’ll send out the closure report later today and notify the stakeholders. Thanks again, everyone. On to the next challenge!

All: Thanks, Sarah!

"""


model = "gemini-1.5-pro"


def test_process_request():
    response = process(model, CONTENT)
    print(json.dumps(response, indent=2))


test_process_request()
