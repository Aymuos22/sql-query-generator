from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

# Replace 'your-openai-api-key' with your actual OpenAI API key
openai.api_key = ''

def generate_sql_query(description):
    prompt = f"Generate an SQL query for the following description: {description}"
    response = openai.completions.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    sql_query = response.choices[0].text.strip()
    return sql_query

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_sql', methods=['POST'])
def generate_sql():
    data = request.get_json()
    description = data.get('description')
    if not description:
        return jsonify({"error": "Description is required"}), 400

    try:
        sql_query = generate_sql_query(description)
        return jsonify({"sql_query": sql_query}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

