from django.conf import settings
from myapp.models import Questions_stuff  # Replace `myapp` with the name of your app
from django.contrib.auth import get_user_model

User = get_user_model()

user_emails = [
    "peace@gmail.com",
    "pepe@gmail.com",
    "jim@gmail.com",
    "keke@gmail.com",
    "fifi@gmail.com",
    "byiringiroscar@gmail.com",
    "ntwarioscar12@gmail.com"
]

technical_questions = [
    ("How to implement a neural network in Python?", "I am looking for a detailed explanation on how to implement a simple neural network in Python. Any example code would be appreciated.", "python,ml,neural-network"),
    ("What are the latest advancements in AI?", "Can someone summarize the latest advancements in AI and their applications?", "ai,ml"),
    ("How to style a webpage using CSS?", "What are the best practices for styling a webpage using CSS?", "css,web-development"),
    ("How to create a RESTful API using Django?", "I need a guide on creating a RESTful API using Django. Any tips or code snippets would be helpful.", "django,python,api"),
    ("Best practices for using React hooks?", "What are the best practices for using React hooks in a project?", "react,web-development,js"),
    ("How to optimize performance in Next.js?", "What are the best techniques to optimize performance in a Next.js application?", "nextjs,web-development,performance"),
    ("Differences between Java and JavaScript?", "Can someone explain the key differences between Java and JavaScript?", "java,javascript,programming"),
    ("How to manage state in a React application?", "What are the best ways to manage state in a large React application?", "react,state-management,js"),
    ("Getting started with machine learning?", "I am new to machine learning. What are the first steps to get started with ML?", "ml,python,beginner"),
    ("Best resources to learn HTML and CSS?", "What are the best online resources to learn HTML and CSS from scratch?", "html,css,web-development")
]

def generate_questions_for_users():
    for email in user_emails:
        try:
            user = User.objects.get(email=email)
            for i in range(2):
                title, detail, tags = technical_questions.pop(0)
                question = Questions_stuff.objects.create(
                    title=title,
                    detail=detail,
                    body=detail,
                    owner=user,
                    viewed=0,
                    tag=tags,
                    email_notify=False,
                )
                question.save()
                print(f'Generated question for {user.username}: {title}')
        except User.DoesNotExist:
            print(f'User with email {email} does not exist')

generate_questions_for_users()
