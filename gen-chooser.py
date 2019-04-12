import json

with open("hxl-knowledge-base.json", "r") as input:
    base = json.load(input)

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;").replace("'", "&apos;")

def make_tagspec(hashtag, attributes):
    return " +".join(["#" + hashtag] + attributes)

def make_html_id(id, hashtag, attributes):
    if hashtag is None:
        return "_" + id
    elif not attributes:
        return hashtag
    else:
        return "_".join([hashtag] + attributes)

def display_question(id, hashtag=None, attributes=[]):
    question = base[id]

    # rendering
    print("    <section class=\"question\" id=\"{}\">".format(esc(make_html_id(id, hashtag, attributes))))
    print("      <h2>{}</h2>".format(esc(question["question"].capitalize())))
    if hashtag is not None:
        print("      <p class=\"tagspec\">{}</p>".format(esc(make_tagspec(hashtag, attributes))))
    print("      <ul>")
    if "pre-text" in question:
        print("        <p class=\"pre-text\">{}</p>".format(esc(question["pre-text"])))
    for option in question["options"]:
        display_option(option, hashtag, attributes)
    if "post-text" in question:
        print("        <p class=\"post-text\">{}</p>".format(esc(question["post-text"])))
    print("      </ul>")
    print("    </section>")

    # recursion
    if "options" in question:
        for option in question["options"]:
            opt_hashtag = hashtag
            opt_attributes = list(attributes)
            if "hashtag" in option:
                opt_hashtag = option["hashtag"]
            if "attribute" in option:
                opt_attributes.append(option["attribute"])

            if "dest" in option:
                display_question(option["dest"], opt_hashtag, opt_attributes)
            else:
                display_result(opt_hashtag, opt_attributes)

def display_option(option, hashtag, attributes):
    if "include" in option and hashtag not in option["include"]:
        return
    elif "exclude" in option and hashtag in option["exclude"]:
        return
    
    opt_hashtag = hashtag
    opt_attributes = list(attributes)
    if "hashtag" in option:
        opt_hashtag = option["hashtag"]
    if "attribute" in option:
        opt_attributes.append(option["attribute"])
    link = make_html_id(option.get("dest"), opt_hashtag, opt_attributes)
    if "dest" not in option:
        link = link + "_"
    print("        <li><a href=\"#{}\">{}</a></li>".format(
        esc(link),
        esc(option["text"])
    ))

def display_result(hashtag, attributes):
    print("    <section class=\"result\" id=\"{}_\">".format(esc(make_html_id(id, hashtag, attributes))))
    print("      <h2>Use this hashtag and attributes</h2>")
    print("      <p class=\"tagspec\">{}</p>".format(esc(make_tagspec(hashtag, attributes))))
    print("    </section>")

print("<!DOCTYPE html>")
print("<html>")
print("  <head>")
print("    <title>HXL hashtag chooser</title>")
print("    <link rel=\"stylesheet\" href=\"style.css\">HXL hashtag chooser</title>")
print("  </head>")
print("  <body>")
display_question("top")
print("  </body>")
print("</html>")
