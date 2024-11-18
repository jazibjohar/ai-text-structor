from main import process
from pprint import pprint
import json

class Request:
    def __init__(self, json):
        self.json = json
    def get_json(self):
        return self.json
    
    
CONTENT = """
Emma (Product Manager):
Good morning, everyone! Let’s kick off today’s stand-up. Let’s start with quick updates on progress and any blockers. Keep it concise. Ryan, why don’t you go first?

Ryan (Developer 1):
Morning, everyone. So, yesterday, I finished implementing the API integration for the new recommendation feature. Today, I’m starting on the unit tests to ensure everything works as expected. No blockers for now.

Emma:
Great to hear, Ryan. Sophia, you’re up next.

Sophia (Developer 2):
Hi, team. I’ve been working on optimizing the backend performance for the search functionality. Yesterday, I identified a bottleneck in the query handling, and today I’ll work on refactoring that. One potential blocker is that I might need updated usage data to test the changes effectively.

Noah (Data Engineer):
Sophia, I can provide you with the latest data from the logs. Let me pull that after the meeting.

Sophia:
Thanks, Noah. That would be super helpful.

Emma:
Good collaboration! David, your turn.

David (Developer 3):
Morning, all. I’m still debugging the user login issue we’ve seen on the staging environment. I made some progress narrowing it down to a session handling problem. My goal today is to finalize the fix and deploy it to staging for testing. No blockers, but I might need Maya’s input later on the UI flow for error messages.

Maya (Designer):
Of course, David. Just ping me, and we’ll review it together.

Emma:
Thanks, David. Liam, let’s hear from you.

Liam (AI Researcher 1):
Morning, everyone. I’ve been refining the new model for sentiment analysis in user feedback. It’s showing good accuracy on most categories, but it struggles with mixed sentiments. Today, I’ll experiment with a few different loss functions to see if that improves the results. No blockers at the moment.

Emma:
Sounds like a good plan. Olivia, your update?

Olivia (AI Researcher 2):
Hi, team. I’ve been working on fine-tuning the chatbot model for customer support use cases. Yesterday, I ran into an issue with the response length control—it’s generating longer replies than intended. I’ll debug that today and also analyze the conversation logs to refine prompts. No blockers for now.

Emma:
Thanks, Olivia. Maya, let’s hear from you.

Maya (Designer):
Morning. I’m finalizing the design mockups for the onboarding flow. I made some tweaks based on feedback from last week. Today, I’ll focus on aligning the style guide with these changes and then hand off the assets to the devs. No blockers, but I’ll need some time with the team tomorrow to review the transitions.

Emma:
Got it. Noah, you’re up next.

Noah (Data Engineer):
Good morning. I’ve been preparing the dataset for the next round of A/B testing. Yesterday, I identified some inconsistencies in the data pipeline, but I managed to fix them. Today, I’ll focus on ensuring the data schema aligns with the AI team’s requirements. No blockers for now.

Emma:
Perfect. Thanks, Noah. Before we wrap up, just a few quick reminders:

Don’t forget the feature demo scheduled for Friday. Let’s aim to have everything ready by Thursday for internal testing.
Also, please update the project board with your progress by EOD.
Anything else from anyone before we close?

Sophia:
Just a quick one—are we still on track to discuss next sprint’s priorities in tomorrow’s planning session?

Emma:
Yes, that’s still on the agenda. Thanks for checking. Anything else?

(No response from the team.)

Emma:
Alright, thanks, everyone! Let’s have a productive day.

All:
Thanks, Emma!
"""

WORD_COUNT = 1000


file_paths = [
    'local_engine.json.json',
]
for file_path in file_paths:
    sample_request = Request({
        'model': 'gemini-1.5-pro',
        'content': CONTENT,
        'word_count': WORD_COUNT,
        "file_path": file_path
    })
    print(json.dumps(process(sample_request), indent=2))