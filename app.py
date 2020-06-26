import os

from flask import Flask, redirect, render_template, request, url_for

from alphabets import Alphabets

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def home():
    techs = ['HTML', 'CSS', 'Flask', 'Python']
    name = '30 Days of Python Programming'
    return render_template('home.html', techs=techs, name = name, title= 'Home')


@app.route('/about')
def about():
    name = 'Coding For all'
    return render_template('about.html', name=name, title='About Us')


@app.route('/post', methods= ['GET', 'POST'])
def post():
    name = 'Text Analyzer'
    if request.method == 'POST':
        return redirect({{url_for('result')}})
    else:
        return render_template('post.html', name=name, title=name)

@app.route('/result.html', methods=['GET', 'POST'])
def result():
    name = 'Text Analysis Result'
    if request.method == 'POST':
        content = request.form['content']
        result = Alphabets(content)
        total_words, num_of_char, most_frequent_word, words, word_num = result.num_of_words(), result.num_of_chars(), result.most_frequent()[0], result.identify(), result.count().items()

        return render_template('result.html', name=name, title='Result', word_count=total_words, char_num = num_of_char, frequent = most_frequent_word, words = words, word_num = word_num)

if __name__ == '__main__':
    app.run(debug=True)
