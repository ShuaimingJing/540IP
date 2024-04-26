from openai import OpenAI

def reverse_math_solver(user_input):

    response = client.chat.completions.create(
    model="ft:gpt-3.5-turbo-0125:personal::9CBKKv54",
    messages=[
      {"role": "system", "content": "You are a math problem solver."},
      {"role": "user", "content": user_input}
    ]
    )
    return response.choices[0].message.content

def gpt_wo_cot(user_input):
    user_input = user_input + " Just give me the answer."

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a math problem solver."},
      {"role": "user", "content": user_input},
      {"role": "user", "content": "Just give me the answer."}  # Adding the follow-up request
    ]
    )
    return response.choices[0].message.content

def gpt_using_cot(user_input):

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a math problem solver."},
      {"role": "user", "content": user_input}
    ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    client = OpenAI(api_key = 'your_openai_key')