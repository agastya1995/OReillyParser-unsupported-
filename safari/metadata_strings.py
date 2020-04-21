def toc_start():
    return  '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">
<head>
    <title>Table of Contents</title>
</head>
<body>
<nav epub:type="toc" id="toc" role="doc-toc">
<ol>'''

def toc_end():
    return '''</nav>
	</body>
</html>'''

def opf_start(title, author, isbn, publisher, language):
    return f'''<?xml version="1.0"  encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/" unique-identifier="bookid" version="3.0">
<metadata>
    <dc:title>{title}</dc:title>
    <dc:creator xmlns:ns0="http://www.idpf.org/2007/opf" ns0:role="aut" ns0:file-as="{author}">{author}</dc:creator>
    <dc:identifier id="bookid">urn:isbn:{isbn}</dc:identifier>
    <dc:publisher>{publisher}</dc:publisher>
    <dc:language>{language}</dc:language>
</metadata>'''

def html_start():
    return '''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"
xmlns:epub="http://www.idpf.org/2007/ops">
<script type="text/javascript" id="MathJax-script" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.0.0/es5/latest?tex-mml-chtml.js">
</script>
<body>'''

def html_end():
    return'''</body>
</html>'''
