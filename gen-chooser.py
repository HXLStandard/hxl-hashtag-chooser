""" Generate a static HTML expert-system site based on hxl-knowledge-base.json 

Requires Python3.

Usage:

    python generate-tag-assist.py [lang] > docs/index.html

Started 2019-04-16 by David Megginson

"""

import json, re, sys

DEFAULT_LANG = "en"
""" Default language to generate """

# Requires Python3 or higher
if sys.version_info < (3, ):
    raise Exception("Requires Python3 or higher")

# TODO: specify file on command line
with open("hxl-knowledge-base.json", "r") as input:
    base = json.load(input)

with open("translations.json", "r") as input:
    translations = json.load(input)

if len(sys.argv) == 2:
    lang = sys.argv[1].lower()
else:
    lang = DEFAULT_LANG

print("Generating in {}".format(lang), file=sys.stderr)

def esc(s):
    """ Escape HTML special characters """
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;").replace("'", "&apos;")

def t(s):
    """ Return a translation if available """
    if s in translations and lang in translations[s]:
        return translations[s][lang]
    else:
        return s

def make_tagspec(hashtag, attributes):
    attributes = [attribute for attribute in attributes if attribute]
    return " +".join(["#" + hashtag] + attributes)

def make_html_id(id, hashtag, attributes):
    if hashtag is None:
        return "_" + id
    elif not attributes:
        return hashtag
    else:
        return "_".join([hashtag] + attributes)

def text (info):
    if lang in info:
        return esc(info[lang])
    elif DEFAULT_LANG in info:
        return esc(info[DEFAULT_LANG])
    else:
        raise Exception("No text in {}".format(DEFAULT_LANG))

def display_question(id, hashtag=None, attributes=[], previous_id=None):
    question = base[id]
    html_id = make_html_id(id, hashtag, attributes)

    # rendering
    print("    <section class=\"question\" id=\"{}\">".format(esc(html_id)))


    print("      <h2>{}</h2>".format(text(question["question"])))

    # progress so far
    if hashtag is not None:
        print("      <p class=\"progress\"><span class=\"tagspec\">{}</span></p>".format(esc(make_tagspec(hashtag, attributes))))

    if "pre-text" in question:
        print("        <p class=\"pre-text\">{}</p>".format(text(question["pre-text"])))

    # Display next options
    for option in question["options"]:
        display_option(option, hashtag, attributes)

    if "post-text" in question:
        print("        <p class=\"post-text\">{}</p>".format(text(question["post-text"])))

    # navigation
    print("      <div class=\"nav\">")
    if previous_id is not None:
        print("      <a href=\"#{}\">◀️ {}</a>".format(esc(previous_id), esc(t("Back"))))
    else:
        print("      <a>&nbsp</a>")
    if id == "top":
        print("          <a>{}</a>".format(esc(t("HXL Hashtag Chooser"))))
    else:
        print("          <a href=\"#_top\">{}</a>".format(esc(t("Restart"))))
    for link_lang in ("en", "fr", "es",):
        if lang != link_lang:
            print("          <a href=\"../{lang}/index.html\">{lang}</a>".format(lang=link_lang))
    print("          <a href=\"http://hxlstandard.org/standard/1_1final/dictionary\" target=\"_blank\">📖 {}</a>".format(esc(t("HXL Dictionary"))))
    print("        </div>")

    # end of question
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
            elif opt_hashtag is not None:
                opt_attributes.append(option.get("attribute", ""))

            if "dest" in option:
                display_question(option["dest"], opt_hashtag, opt_attributes, html_id)
            else:
                display_result(option, opt_hashtag, opt_attributes, html_id)

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
    elif opt_hashtag is not None:
        opt_attributes.append(option.get("attribute", ""))
        
    link = make_html_id(option.get("dest"), opt_hashtag, opt_attributes)
    if "dest" not in option:
        link = link + "_000"
    print("        <p class=\"option\"><a href=\"#{}\">{}</a></p>".format(
        esc(link),
        text(option["text"])
    ))

def display_result(option, hashtag, attributes, previous_id):
    print("    <section class=\"result\" id=\"{}_000\">".format(esc(make_html_id(id, hashtag, attributes))))
    print("      <h2>Finished!</h2>")
    print("      <div class=\"tagspec-container\">")
    print("        <p class=\"tagspec final-tagspec\">{}</p>".format(esc(make_tagspec(hashtag, attributes))))
    print("      </div>")
    for attribute in attributes:
        if re.match(r"[A-Z]", attribute):
            print("        <p>Don't forget to replace <b><code>+{}</code></b> with your own attribute.</p>".format(esc(attribute)))
    if "note" in option:
        print("       <p class=\"note\">{}</p>".format(text(option["note"])))
    print("      <p class=\"post-text\">You are free to add more attributes, or to make up your own, if you need to make further distinctions.</p>")
    print("      <div class=\"nav\">")
    print("        <a href=\"#{}\">◀️ {}</a>".format(esc(previous_id), esc(t("Back"))))
    print("        <a href=\"#_top\">{}</a>".format(esc(t("Restart"))))
    print("        <a href=\"http://hxlstandard.org/standard/1_1final/dictionary\" target=\"_blank\">📖 {}</a>".format(esc(t("HXL dictionary"))))
    print("      </div>")
    print("    </section>")

print("<!DOCTYPE html>")
print("<html>")
print("  <head>")
print("    <title>HXL hashtag chooser</title>")
print("    <link rel=\"stylesheet\" href=\"../style.css\"/>")
print("    <link rel=\"icon\" href=\"../icon.png\"/>")
print("    <link rel=\"manifest\" href=\"../manifest.webmanifest\"/>")
print("    <meta charset=\"utf-8\"/>")
print("    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"/>")
print("  </head>")
print("  <body>")
display_question("top")
print("  </body>")
print("  <script src=\"../script.js\"></script>")
print("</html>")
