import ast
import os
import random
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'change-me'

def load_words():
    """Extract list_of_words from wordle.py without importing pygame."""
    path = os.path.join(os.path.dirname(__file__), 'wordle.py')
    with open(path, 'r') as f:
        tree = ast.parse(f.read(), filename='wordle.py')
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], 'id', None) == 'list_of_words':
            return [elt.s for elt in node.value.elts]
    return []

WORDS = load_words()


def evaluate_guess(answer, guess):
    """Return list describing guess accuracy for each letter."""
    result = []
    answer_chars = list(answer)
    for i, ch in enumerate(guess):
        if i < len(answer_chars) and ch == answer_chars[i]:
            result.append('correct')
        elif ch in answer_chars:
            result.append('present')
        else:
            result.append('absent')
    return result


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'word' not in session:
        session['word'] = random.choice(WORDS)
        session['guesses'] = []
    message = None
    if request.method == 'POST':
        guess = request.form.get('guess', '').lower()
        if len(guess) == 5 and guess.isalpha():
            result = evaluate_guess(session['word'], guess)
            session['guesses'].append((guess, result))
            if guess == session['word']:
                message = 'Correct!'
        else:
            message = 'Enter a valid five-letter word.'
    return render_template('index.html', guesses=session.get('guesses', []), message=message)


@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
