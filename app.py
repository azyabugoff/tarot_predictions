import os
import traceback
import random
from huggingface_hub import InferenceClient
from flask import Flask, render_template, jsonify
from meanings import CARD_MEANINGS
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient("HuggingFaceH4/zephyr-7b-alpha", token=HF_TOKEN)

app = Flask(__name__)

CARDS_FOLDER = 'static/cards'
RANDOM_IMAGES_FOLDER = 'static/random_images'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/draw_cards', methods=['GET'])
def draw_cards():
    card_files = [f for f in os.listdir(CARDS_FOLDER) if f.endswith('.jpg')]
    if len(card_files) < 3:
        return jsonify({'error': 'Not enough cards in the folder!'}), 500

    selected_cards = random.sample(card_files, 3)

    result = {'cards': []}
    prompt_cards = []
    for card_file in selected_cards:
        card_key = card_file.replace('.jpg', '')
        card_name = card_key.replace('_', ' ').title()
        meaning = CARD_MEANINGS.get(card_key, "Unknown meaning")
        result['cards'].append({
            'image': f'/{CARDS_FOLDER}/{card_file}',
            'name': card_name,
            'meaning': meaning
        })
        prompt_cards.append(f"{card_name}: {meaning}")

    random_images = [f for f in os.listdir(RANDOM_IMAGES_FOLDER) if f.endswith('.jpg')]
    selected_image = random.choice(random_images) if random_images else ''
    result['random_image'] = f'/static/random_images/{selected_image}'

    prophecy = generate_ai_prophecy(prompt_cards)
    result['prophecy'] = prophecy

    return jsonify(result)


def generate_ai_prophecy(card_infos):
    prompt = (
        "You are a mystical political oracle. Based on the following three tarot cards and their meanings, "
        "generate a short political prophecy (3-5 sentences) that describes possible future global or geopolitical events. "
        "Do not mention the cards directly in the text. "
        "Use simple english speech with easy-reading constructions. "
        "Here are the cards:\n\n" +
        "\n".join(card_infos) +
        "\n\nProphecy:"
    )

    try:
        response = client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            # max_new_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        print(f"Error generating prophecy: {e}")
        traceback.print_exc()
        return "The oracle is silent... (AI error)"


if __name__ == '__main__':
    app.run(debug=True)
