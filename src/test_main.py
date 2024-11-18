from main import process
from pprint import pprint
import json

class Request:
    def __init__(self, json):
        self.json = json
    def get_json(self):
        return self.json
    
    
CONTENT = """
Interviewer (Alex):
Good afternoon, Sarah, and thank you for joining me today. Let’s start with something fundamental. In your experience, how do you approach evaluating machine learning models, especially when comparing classical machine learning techniques to large language models (LLMs)?

Candidate (Sarah):
Good afternoon, Alex. Thank you for having me. Uh, so, when it comes to evaluating machine learning models, I think it’s really about, uh, understanding the use case first. For classical models, the evaluation is more, uh, straightforward? Metrics like accuracy, precision, recall, and F1 score are, uh, commonly used because they, uh, directly reflect how well the model is performing on structured data.

But, uh, when we shift to LLMs, the evaluation gets a lot more nuanced. For example, with LLMs, the output is often unstructured text, so using metrics like BLEU, ROUGE, or even METEOR, uh, makes sense for text generation tasks. But, um, those don’t always tell you if the text is actually useful or relevant to the user. So, uh, in those cases, human evaluation or task-specific metrics are, uh, crucial. Sorry, I’m still working on getting a deeper understanding of these, but I hope that makes sense?

Alex:
That does, thank you. You touched on human evaluation there. Could you elaborate on how you would design or oversee an effective human evaluation process for an LLM?

Sarah:
Oh, uh, sure. So, um, human evaluation is definitely an important part of assessing LLMs, especially for subjective tasks. I think the key is to have a very clear and detailed guideline for evaluators. Like, uh, they need to know exactly what they’re looking for—whether it’s relevance, factual accuracy, fluency, or even ethical considerations.

One thing I’ve read about, uh, is inter-annotator agreement. Ensuring that multiple annotators are consistent with each other helps reduce bias. I guess you could use something like Cohen’s kappa or Krippendorff’s alpha to measure that agreement?

Another thing is, uh, balancing the evaluators’ subjective judgment with, uh, objective measures. For example, you might use automated metrics for speed and scale but rely on human evaluation for deeper insights, like whether the response aligns with cultural or contextual norms in a specific domain. Uh, I haven’t implemented this myself, but that’s, uh, how I’d approach it.

Alex:
That’s a solid start. Let’s switch gears a bit. With classical machine learning, how do you determine when a simpler model, like linear regression or logistic regression, is more suitable than a more complex model, like a deep neural network?

Sarah:
Um, yeah, that’s a great question. So, in my understanding, simpler models tend to work better when the data is, uh, relatively small or when the relationships in the data are, uh, linear or straightforward. For example, if you’re working with tabular data that has clear trends or correlations, logistic regression might be a good fit.

Complex models like neural networks, on the other hand, are, uh, great for handling non-linear relationships or large, unstructured datasets, like images or text. But they come at a cost—they require more data, computational power, and, uh, careful tuning to avoid overfitting.

I think, um, it also depends on interpretability. Simpler models are easier to explain to stakeholders. For example, in industries like healthcare or finance, where transparency is critical, a logistic regression model might be preferable over a deep learning model, even if the latter performs slightly better.

One time, I worked on a classification problem where the dataset was small, and we tried a random forest and a logistic regression. The simpler model actually performed almost as well but was much easier to explain. Uh, so, I’ve seen this trade-off firsthand.

Alex:
Good point on interpretability. Now, moving back to LLMs, how do you balance computational cost with performance, especially when deploying these models in production?

Sarah:
Oh, um, that’s a tough one. Balancing cost and performance is definitely challenging with LLMs, especially given how resource-intensive they can be. I think, first, it’s about understanding the end-user requirements. For instance, if the model doesn’t need to generate super-detailed responses but still needs to be fast, techniques like model quantization or pruning can be helpful.

Another approach might be, uh, model distillation. You take a large model and train a smaller one to mimic its behavior. That way, you can deploy the smaller model, which is faster and cheaper, but still retains much of the large model’s capability.

There’s also the option of caching frequently used responses, especially for queries or tasks that are repetitive. And, uh, leveraging cloud providers with elastic scaling can help manage costs dynamically.

I admit I’m not super experienced with deploying LLMs yet, but I’ve been reading a lot about these strategies and trying to get up to speed.

Alex:
You’re on the right track. For my final question, if you had to design an evaluation framework for an LLM in a domain like healthcare, what key components would you include?

Sarah:
Hmm, okay, that’s a big question. I think in a domain like healthcare, accuracy and safety would have to come first. So, I’d start with a focus on factual correctness—using benchmarks or expert-verified datasets to ensure the model’s responses are reliable.

I’d also include domain-specific evaluations, where medical professionals review the output to ensure it aligns with clinical standards. For example, does the model provide evidence-based recommendations? Or does it produce responses that could be potentially harmful?

Explainability is another key factor. If the model makes a suggestion, it should be able to provide some reasoning or cite sources, so the users—whether they’re doctors or patients—can trust its output.

Finally, ethical considerations would be huge. We’d need to evaluate for bias, ensuring the model treats all demographics fairly and doesn’t perpetuate any harmful stereotypes. Uh, I’d probably also include usability testing to make sure the model’s responses are easy to understand and actionable for its intended audience.

I’m sure there are other factors I’m missing, but, uh, those would be my starting points.

Alex:
Those are some thoughtful insights, Sarah. Thanks for your responses today. Do you have any questions for me about the role or the team?

Sarah:
Uh, thank you, Alex. Yeah, I’d love to know more about how your team is currently approaching model evaluation and, uh, any resources or best practices you’d recommend for someone who wants to grow in this area.

Alex:
Absolutely. I’ll share some insights and resources after this session. Thanks again for your time and effort today.

Sarah:
Thank you, Alex. I really appreciate the opportunity to learn from this.
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