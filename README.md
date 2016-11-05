# How-was-your-day-
Hack NJIT 2016 Project

### TODO

I added `.md` files for the folders I made and comments for everything.

- [ ] make the thing
- [ ] remove / edit the random md files when everything works.

### How HTML forms are handled in flask

The HTML:

```HTML
<form action="path" method="METH">
  <input ... name="some_name"></input>
  <input ... name="some_other_name"></input>
</form>
```

The python:

```python
from howWasYourDay import app #maybe a bit different

@app.route("path", methods=['METH'])
def form_handle():
  thing_user_inputted_for_the_first_thing = request.form['some_name']
  thing_user_inputted_for_the_second_thing = request.form['some_other_name']
