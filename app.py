from flask import Flask, render_template, request
from helper import recipes, descriptions, ingredients, instructions, add_ingredients, add_instructions, comments
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecret"

class CommentForm(FlaskForm):
  comment = StringField('Comment',
                        validators=[DataRequired()])
  submit = SubmitField('Add Comment',
                        validators=[DataRequired()])

@app.route('/', methods=["GET", "POST"])
def index():
  new_id = len(recipes) + 1
  if len(request.form) > 0:
    recipes[new_id] = request.form["recipe"]
    descriptions[new_id] = request.form['description']
    new_ingredients = request.form['ingredients']
    new_instructions = request.form['instructions']

    add_ingredients(new_id, new_ingredients)
    add_instructions(new_id, new_instructions)
  

  return render_template("index.html",
                        template_recipes=recipes)

@app.route("/about")
def about():
  return render_template("about.html")


@app.route("/recipe/<int:id>", methods=["GET", "POST"])
def recipe(id):
  
  comment_form = CommentForm(csrf_enabled=False)
  if comment_form.validate_on_submit():
    new_comment = comment_form.comment.data
    comments[id].append(new_comment)

  return render_template("recipe.html", 
                        template_recipe=recipes[id], 
                        template_ingredients=ingredients[id],
                        template_description=descriptions[id],
                        template_instructions=instructions[id],
                        template_comments=comments[id],
                        template_form=comment_form)