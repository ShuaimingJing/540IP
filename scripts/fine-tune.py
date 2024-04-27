from openai import OpenAI

def data_converter(train_data):
    system_prompt = """
    You are a clever mathematician. 
    Please give me the answer of the given questions. 
    """
    user_prompt = train_data['question']
    answer = train_data['answer']

    return {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": answer}
        ]
    }


def main():
    # Load your training data
    train_data = pd.read_csv('path_to_your_train_data.csv')
    train_json = train_data.apply(data_converter, axis=1)

    # Save data_json to a jsonl file
    output_dir = '/Users/shuai/Desktop/train_data.jsonl'
    train_json.to_json(output_dir, orient='records', lines=True)

    # Set up the API key and create a client
    api_key = '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'
    client = OpenAI(api_key=api_key)

    # Upload the file for fine-tuning
    client.files.create(
      file=open(output_dir, "rb"),
      purpose="fine-tune"
    )

if __name__ == "__main__":
    main()
