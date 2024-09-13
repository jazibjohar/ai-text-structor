from main import process
from pprint import pprint
import json

class Request:
    def __init__(self, json):
        self.json = json
    def get_json(self):
        return self.json
    
    
CONTENT = """
Talk with Junaid/Baligh/Mashhood (2024-06-09 11:09 GMT-6) - Transcript
Attendees
Junaid Afzal, Mashhood Ahmed, Syed Mohammad Baligh
Transcript
This editable transcript was computer generated and might contain errors. People can also change the text after it was created.
Syed Mohammad Baligh: Tuning model that needs to be on you need to Define epochs. You need to Define its evaluation metrics, right? So…
Junaid Afzal: Okay, yeah.
Syed Mohammad Baligh: what are those things and how you coming up with those numbers?
Junaid Afzal: Okay, so I get it now. So basically to prepare the data set. I mostly use the hugging phase. So there is a hugging phase data set. We select the data set preprocess it and selected it decide format of that and then if we have organization we can upload our data set to our organization or profile to use that into future. And for the fine tuning if most of the time we have used the Google clap pro version and the gcp and also the awsage makeup sometimes so in the most of time we have found that the club and gcp platform is most suitable for our uses this is some pros and call based on that and then after the fine tuned when we get the model. We upload that into the hugging phase cause it is very easier to
Junaid Afzal: if I model from there because we didn't have to message about the saving loading downloading and everything else. So they have a Git Version like a functionality and we can save as much model as we want. and for the find hyper parameter tuning. So basically we do some research on the downstream task and the benchmarks they provided into their research So I've been checking papers with code. This is a platform where they just launch the updates and the paper related to the MLM so into the paper, we find the insights of what they are doing with the architecture and what we can do optimize that and there are the techniques like it all low rank and actually inversion and there is I think Booth I don't know dream about the sporting and I'm still
Junaid Afzal: For now because we are using that to find you. model which is a stable diffusion for the imagination and…
Syed Mohammad Baligh: cool
Junaid Afzal: the things
Syed Mohammad Baligh: and are you also Frank tuning a stable diffusion models as well?
Junaid Afzal: Yeah, I have worked with that. So we have a couple of products and the services build using them.
Syed Mohammad Baligh: Good one thing I forgot mentioning is how are you taking care of the embedding stuff?
Syed Mohammad Baligh: That something we're doing when you're fine tuning this is that part of your training job have you abstracted out because I'm betting needs to happen at the time of inference as well as well as during training.
Junaid Afzal: So most of the time we are using the inbuilt embedding model that the llms nothing special.
Syed Mohammad Baligh: So how you taking care of that?
Syed Mohammad Baligh: Okay. Okay. Yep you yeah.
Mashhood Ahmed: Okay, Yeah. So Junaid, let me just talk about what we are trying to do and what I'm interested and what we could offer and what could be the short term and the long term goal for this engagement, So I mean, you've been following me on LinkedIn. I'm not sure how actively you're following me on the LinkedIn, but we can't attack they are right. So I do a lot of talks in the area of project management. Okay, and I do have this. Application the system that I would like to build which is a PM ai. So the problem is when I go and talk to the project managers and I asked this question. Is it anyone in this room who loves to take meeting minutes and I haven't find a single person who actually take the meeting. There's a
Mashhood Ahmed: agreement among all project managers around the world that they hate this job the most. the question is, how can we leverage AI to do the dirty job for the project manager so that they can focus on the good job, So the idea is that what we would like to build is I would like to build. so basically in my vision what's going to happen is that Somebody will come to our website. They will subscribe they will, get the account access yet. I add up and then they will go and give the client access to their calendar. So for example, they're using Gmail flender or artwork lender, whatever cleaner and we can start with one or two and then kind of expand on that right? So we give access to them they give access to the calendar. And then PMS system will know what time they have the meeting.
00:05:00
Mashhood Ahmed: And the PM assistant will join every single meeting with them. and within that whenever they join the meeting the llm part of the tool would go and say hey, here's a summary of the meeting his action item table. Here's this right. And then what my vision is that I want to build.
Mashhood Ahmed: What I call a hierarchy of products. So when you're working a project if you're starting a project you do different things, if you're finishing the project you do different things and if you're in the project base execution, you do different things So depending on all the metadata about the meetings, we will collect what's needs to be done. And that's the hierarchy of front will do and that will help project manager to do this stuff. So this is the long term goal for my product and this is kind of a little confidential. I really do not share with everybody but, since something talking with you some time and I don't share this from publicly on LinkedIn special. What I want to build is I want to build autonomous project manager.
Mashhood Ahmed: Meaning instead of hiring a project manager you hire an autonomous project manager and that's something that we would provide and that's a product that I really want to build and that's what I'm really committed to invest my time and money. So here's what I'm thinking that what we can do if you are interested first the question is This is not going to be like a salary job or a salary sidekick where you can make a really good money in the So this is not that first. Let's be clear. This is more about we will give some money. Yes. Definitely. you're not looking for free for us from day one. We will be giving you some money. just to cover your basic expenses, but I want to hire a first employee of the PM and the goal is to have the first employee who knows what he's doing and kind of aligns with our vision and Mission.
Mashhood Ahmed: And in return what we would offer is as I said a little bit of a stipend in the beginning. And after three months or six months, we will do like a check and say hey, are you still interested? Do you like working with us? You like our vision? And everything's good. Then we'll talk about some Equity. I'm based in Canada and believe is based in California, San Francisco. So because my company is registered in Canada. I can responsor you on a work visa and Canada, So, after three to six months we can talk about that and we can try to bring you here within a year time, So that is something that I cannot promise in terms of if I can give you a day one a good salary, but this is something I want you to think about in terms of
Mashhood Ahmed: haven't you have an option you can continue as a job and do your job for time or do the site small contracts hitting there? Yes, you can make a really good money here and there but what the real money is an equity is in the building the future product. So with that I'm just gonna take a pause and maybe ask if you have any questions or you want some clarity. I mean you can take your time and discuss.
Junaid Afzal: Okay. Yeah, I understand that. So I like the idea so it's a very interesting thing. I think everyone is that course most of the project managers are joining meetings and listening to the one arts or…
Mashhood Ahmed: yeah, so believe it's belief and belief.
Junaid Afzal: meeting and then retaking about the reviews and…
Syed Mohammad Baligh: just So maybe…
Junaid Afzal: recordings and then taking notes and extracting points and…
Syed Mohammad Baligh: what I can do is I can talk about…
Junaid Afzal: the important things.
Syed Mohammad Baligh: how we are planning on doing it.
Junaid Afzal: So if we have I think that is the very beneficial for the project managers and…
Syed Mohammad Baligh: And what's again my should talked about what's the bigger vision and…
00:10:00
Junaid Afzal: also the developer or whoever working.
Syed Mohammad Baligh: where we are going to words and…
Junaid Afzal: So I like the idea for this so I have a couple of questions.
Syed Mohammad Baligh: I can talk about what? Baby steps we need to take in order to get there. so
Junaid Afzal: So if you're talking about what I get this is I think that the one person job course,…
Syed Mohammad Baligh: Mashhood that already talked to you about we are on low code platform,…
Junaid Afzal: we have a multiple things. we have handling the website back and…
Syed Mohammad Baligh: but we are still coding something.
Junaid Afzal: front end and…
Junaid Afzal: the AI so as the mini a person so I think I can handle AI part and…
Syed Mohammad Baligh: So a couple of things that we don't have a lot of data to build our own models.
Junaid Afzal: some of the back and work late that Building functionalities by API.
Junaid Afzal: 
Syed Mohammad Baligh: And I don't think we'll be able to generate enough data…
Syed Mohammad Baligh: until next two years to create our own models.
Junaid Afzal: So who else is working on that to create the web and…
Syed Mohammad Baligh: So I'm not sure…
Junaid Afzal: the clients that will connect the different parts of the platforms to your website.
Syed Mohammad Baligh: if you are aware of el Paka approach that Stanford had taken we are trying to follow that approach. What they do is they use bigger models to generate their data set and then fine-tune the smaller models on the generated that I said from the bigger models, so we are kind of following their footsteps right now. We are kind of doing a basic prompt engineering.
Syed Mohammad Baligh: Where we are generating data from users meeting transcripts and user questions, and we are saving all that data. and once we have sufficient data, we will be looking at fine tuning and building our own models. So that's where we will have The other area where we would be having a lot of AI work work is we are also looking at implementing drag. on top rag, so there could be project documentation. There could be different verticals. For example, there could be organizational policy or there could be a state policy. There will be separate models for both of them and on top of that rag model.
Syed Mohammad Baligh: And so I'm using the word Greg are you aware of wonderful, But yes,…
Junaid Afzal: Yep.
Syed Mohammad Baligh: retrieval augmented generation. So the company's documents will be living in a vector database and then we are querying large management model and providing context from VDB. so these things are going to be at baby steps in order to collect and generate enough data. Once we have that data. We would be basically finding our models so are first step.
Syed Mohammad Baligh: For rag is also going to be either we would be using open AI assistant which is like a quick API calling and that should be it or I am also inclined towards using Lama index but when we say llama index, we need to be maintaining that structure for it and the stage. are it I'm kind of like pushing back on that. so these are some of the things that we would be doing immediately.
Mashhood Ahmed: yeah.
Syed Mohammad Baligh: It's mostly going to be a prompt engineering thing.
Syed Mohammad Baligh: Odd back in the backend. We have written isn't Python and it uses line chain to basically run some prompts and…
Junaid Afzal: Med
Syed Mohammad Baligh: between models and the idea is to support available open source models we can quickly spin up and…
Mashhood Ahmed: Yeah.
Junaid Afzal: med
Syed Mohammad Baligh: open AI gemini or a llama instance. I plan on using growth for llama 3, I guess so initially we would be offering flexibility to switch between models and…
Junaid Afzal: med
Syed Mohammad Baligh: for all those instances. We will be generating data.
Junaid Afzal: med
Mashhood Ahmed: Yeah, we'll just to add to this Junaid. So I'm not technical believe is too much technical right? I'm very high level. I understand some technology but not a lot. my vision is that remember we're talking about two different products. One is a PM assistant other one is the Optimus project manager.
Syed Mohammad Baligh: So that's our immediate need in terms of air.
Mashhood Ahmed: For PM assistant my Approach is we need to go local no-code get it up and running quickly dirty. It's fine. if it does not work hundred percent all the time. It's okay, However, in the back end what I really want to focus on is to focus on the architecture of the Optimus project manager so that we can build that one. Right? So the PMS system is the front phase that we can showcase to the world saying hey, we are helping the project managers and in the back we want to build the Optimus project manager. something will make us real big money, So that is a really Cash The PMS system is not a cash cow PM assistant is local no-code directly fail fast approach to get the name out. So I do like a lot of talks of the PMI and PMI chapters and other stuff.
00:15:00
Mashhood Ahmed: And people do follow me and run some EA master class as well. which is I'm very successful in running those ones as well. So I do have a following that does follow me and I think I am at the right time to make this happen, but I do need a team of good people and again, I'm really
Mashhood Ahmed: We've been talking for six months now or a play right? But I'm really keen on having the right people with the right mindset and that's what I want to talk about is if you align with that type of mindset one mindset is I want to give my hours and make money. That's one minded other mindset is what I make enough money or I have enough money to pay my bills, but I want to build something big. I want to build something huge that would eventually make me Millions,…
Syed Mohammad Baligh: I would also like to share an anecdote.
Mashhood Ahmed: right and…
Syed Mohammad Baligh: So I work for a company called Kida.
Mashhood Ahmed: you will be the first employee that means you will have a big chunk of that at some point in future…
Syed Mohammad Baligh: and this is my story and…
Mashhood Ahmed: if all of us collectively are successful,…
Syed Mohammad Baligh: what you can tell me to shut up,…
Mashhood Ahmed: So you are the first one probably I will set up.
Syed Mohammad Baligh: but I think for I
Mashhood Ahmed: Million in a year or two. We might have to set up an office in Pakistan or…
Syed Mohammad Baligh: Yeah. I think it is going.
Mashhood Ahmed: maybe not right you will need to say but we will having more people bringing in…
Syed Mohammad Baligh: It should help them see where.
Mashhood Ahmed: but you and belief will be the core architect of this this time.
Syed Mohammad Baligh: It can take them. So I was the only engineer…
Mashhood Ahmed: So I want you to think from that perspective not from the hours and…
Syed Mohammad Baligh: who built the product for kiddom and…
Mashhood Ahmed: money perspective.
Syed Mohammad Baligh: I came up with the Prototype. I was involved in the funding and I'm still working for them. And I was working from Pakistan since 2012 kiddom got funding in 2015 and they moved me here in 2018. And since…
Mashhood Ahmed: Not good,…
Syed Mohammad Baligh: then I've been working in us.
Mashhood Ahmed: whatever. You're comfortable sharing.
Syed Mohammad Baligh: I'm a Staff engineer again.
Mashhood Ahmed: Go ahead.
Syed Mohammad Baligh: I'm an engineer at core so that I do have any routine the company as well get them is now valued at like 500 million dollars and…
Mashhood Ahmed: I'm not gonna say anything.
Syed Mohammad Baligh: I do have in terms of equity if you look at the number, I only get 5% of the company which is like if you look at 1.5% It's a very small
Syed Mohammad Baligh: Number but when you look at the valuation of the company it becomes a huge number so I would love to have you think along those Direct.
Syed Mohammad Baligh: 5% of half a million dollar would be like
Syed Mohammad Baligh: I 500 million dollars and 1.5% is 7.5 million.
Mashhood Ahmed: Look somebody what is 1.5% of half a billion dollars.
Mashhood Ahmed: No, no, what is the evolution of your company? And what is
Mashhood Ahmed: So by Junaid what believe is saying is that because he was a first employee he had a 1.5% of equity which translate today after 12 years of working here into 7.5 million dollars US dollars,…
Syed Mohammad Baligh: Sure.
Mashhood Ahmed: So Let's make so I want you to think big, If you think it's small, yeah, you can make money. But if you think big you're gonna go further far. Okay, so I think this is all good from our side. I'll be quiet and Junaid. Do you have any questions? I don't need to answer right now. I want you to think about it. Maybe we can have a college deal to you. if you want to have a technical discussion with belief. Feel free to have a call with him or we can discuss. So let me…
Junaid Afzal: Yeah, I think for now everything is good.
Mashhood Ahmed: if you have any questions for now. If not, we can catch up in few days.
Junaid Afzal: So I will think about that brains from my brainstorming on the idea and the process you just talk about and I will reach out on the LinkedIn. So overall I like the idea and the work style of totally get the steps how we are doing that. So one, let me set up my mind of what should be I doing because I had to manage the time accordingly. So a you talk about that this is the simple part-time. So I think I will be working or next four to five hours on this.
00:20:00
Mashhood Ahmed: Yeah, so think of It's a part-time to start with. However, I'm expecting by some time in six months from now.
Junaid Afzal: Yep.
Mashhood Ahmed: This could become full time. Okay.
Mashhood Ahmed: And again you can start slow. For example, you might say hey, what for the month of June. I'm just gonna give maybe 10 hours a week kind of a thing just to understand and kind of synced up with this few times. That's perfectly fine. end of June you make up your mind we can do the paperwork and then you start with us and kind of working with belief in the backend to help him feel the other things come Se October we get to the point where we like you and you like us. It's a boat. It's just two way street right and then we can say hey, what? Let's just make it formalize. Let's get you a full time and all that the numbers and the money thing we can talk about. we don't want to work for free for us. Right so don't think that, you have to work free for us from day one day one you'll get paid…
Junaid Afzal: Ahmed
Mashhood Ahmed: but not like a big money that Can you pay your Pakistan right? I mean companies can be crazy many Pakistan, but they don't give you
Junaid Afzal: Yep, I get the idea. So I have just one question. So for the start I think nothing is very true about really too…
Mashhood Ahmed: Equity they don't give you the opportunity to own the part of the company.
Junaid Afzal: What is the minimum and…
Mashhood Ahmed: Okay, what we are offering is first employee the part of the company and…
Junaid Afzal: the average what we will be getting so I can understand if I am managing my stuff.
Mashhood Ahmed: that could means I don't know how much right but we have to start and…
Junaid Afzal: So I think that we can to go with the thing.
Mashhood Ahmed: you have to see how it goes in after three months you might say hey, what? I don't like it. I have better things to do perfectly fine, but I just want you to have that open mind and…
Junaid Afzal: Yep, okay.
Mashhood Ahmed: the other thing that I mentioned was that because my company is registered in Canada. I do have an option to bring somebody on the work visa here to Canada, That means that will give you the Canadian hard kid is a ship down the road.
Junaid Afzal: Yeah.
Mashhood Ahmed: So that is kind of a thing that we can start hopefully by the end of the year as well. So it just need to make sure that you…
Syed Mohammad Baligh: Yeah, and I'm looking at making my first hundred million dollars with PM assistant.
Mashhood Ahmed: there's a right match right chemistry among all three of us.
Syed Mohammad Baligh: So yeah, I'm happy to share some of that with you as well.
Mashhood Ahmed: your question is about the money part or
Syed Mohammad Baligh: Yep,…
Mashhood Ahmed: Up we can talk about it.
Junaid Afzal: Hello. Okay. Okay.
Syed Mohammad Baligh: You got my email.
Mashhood Ahmed: Everything is open for now.
Syed Mohammad Baligh: I have message my email in case of any engineering or…
Mashhood Ahmed: Okay, so you tell us your number you tell us your number and…
Syed Mohammad Baligh: technical related questions or…
Mashhood Ahmed: we can talk about it.
Syed Mohammad Baligh: in case you want to understand…
Mashhood Ahmed: But have a realistic expectation,…
Syed Mohammad Baligh: how we are doing it right now. I'm happy to talk to you in I have shared my email we can talk we can meet again.
Mashhood Ahmed: So the expectation is that Having enough money to pay your bills and sustain your good life.
Syed Mohammad Baligh: I'm happy to answer any of your questions and…
Mashhood Ahmed: Okay, I don't want you. There's a life. However, keep in mind that this is …
Syed Mohammad Baligh: let me know if there is anything I can help you with.
Mashhood Ahmed: you'll probably and I'm honest right?
Junaid Afzal: Yep, I will approach.
Mashhood Ahmed: You will probably not make a real good money in the next one or two years with us, right, but if you stick to us and if you kind of help us build…
Syed Mohammad Baligh: the wonderful wonderful
Mashhood Ahmed: what we are trying to build. believe that 7.5 million dollars of his equity in that company.
00:25:00
Syed Mohammad Baligh: thank you so much, but love is
Mashhood Ahmed: Okay, you could be at more because the time of the AI is bringing so much cash and so much money. It's just a matter of bringing the right people to the team and build upon it.
Junaid Afzal: Yeah, so I will look into this brainstorm my idea and the thinking on the thing then I will reach back. Okay.
Junaid Afzal: Thank you. Angela I love this.
Mashhood Ahmed: Okay, so, let's just keep it open. Maybe in Deal two we can touch base. I can have a chat with you to not tomorrow, but day after tomorrow or Tuesday Wednesday and let me know what questions you may have and then we can go from there. Okay.
Mashhood Ahmed: excellent
Mashhood Ahmed: excellent Thank you for Junaid When shall I see your? so
Meeting ended after 00:25:12 👋
"""

WORD_COUNT = 1000


file_paths = [
    # 'example_1.json',
    # 'example_2.json',
    # 'example_3.json',
    # 'example_4.json',
    #'example_5.json',
    'example_6.json',
]
for file_path in file_paths:
    sample_request = Request({
        'model': 'gpt-4o',
        'content': CONTENT,
        'word_count': WORD_COUNT,
        "file_path": file_path
    })
    print(json.dumps(process(sample_request), indent=2))