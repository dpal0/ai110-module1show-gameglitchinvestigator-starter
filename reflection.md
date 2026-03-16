# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
The Hints given after submitting the number were never right.
The new game button did not work properly
The history isn't being updated properly, it counts a empty entry as valid entry and counts it in history
Number of attempts left displayed is different that what is actually allowed
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---
I used Claude code for this project. For this most of the suggestions were good and not misleading. It was very conservative and asked me many questions, I didn't allow it to write changes automatically and also I ran my own bash commands.

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---
I mainly tested by running the website manually, but I somethings chaged the values in the tests writtien. For example I put 586 which is greater than 100 which was wrong so I saw the test for it, there wasn't any, so I told AI to add that and refactor the code to validate input so that are in only place.

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Its like npm run dev but for python based code. So used it when you don't have a frontend file. Your front and backend both can be in python
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
Testing habit:
I really like agile testing and unit testing altough I am quite unfamiliar with python workflows, I will try to implement that in pyton workflows using AI after some research of my own. I think that going forward I will have to spend most of my time thinking of code and structuring my code.