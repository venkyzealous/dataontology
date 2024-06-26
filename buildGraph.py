from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import OWL, XSD, RDFS

# Create a namespace for our resources
n = Namespace("http://example.org/library/")

# Create a Graph
g = Graph()

# Define Class: Book
Book = URIRef(n + "Book")
g.add((Book, RDF.type, OWL.Class))

# Define Class: Author
Author = URIRef(n + "Author")
g.add((Author, RDF.type, OWL.Class))

# Define Property: hasAuthor
hasAuthor = URIRef(n + "hasAuthor")
g.add((hasAuthor, RDF.type, OWL.ObjectProperty))
g.add((hasAuthor, RDFS.domain, Book))
g.add((hasAuthor, RDFS.range, Author))

# Define Property: hasTitle
hasTitle = URIRef(n + "hasTitle")
g.add((hasTitle, RDF.type, OWL.DatatypeProperty))
g.add((hasTitle, RDFS.domain, Book))
g.add((hasTitle, RDFS.range, XSD.string))

# Define Property: hasName
hasName = URIRef(n + "hasName")
g.add((hasName, RDF.type, OWL.DatatypeProperty))
g.add((hasName, RDFS.domain, Author))
g.add((hasName, RDFS.range, XSD.string))

# Define Property: hasName
hasGenre = URIRef(n + "hasGenre")
g.add((hasGenre, RDF.type, OWL.DatatypeProperty))
g.add((hasGenre, RDFS.domain, Book))
g.add((hasGenre, RDFS.range, XSD.string))

# Create a Book instance
book1 = BNode()
g.add((book1, RDF.type, Book))
g.add((book1, hasTitle, Literal("The Great Gatsby")))
g.add((book1, hasGenre, Literal("Novel")))

# Create an Author instance
author1 = BNode()
g.add((author1, RDF.type, Author))
g.add((author1, hasName, Literal("F. Scott Fitzgerald")))

# Link the Book and Author instance
g.add((book1, hasAuthor, author1))

# Bind the OWL namespace
g.bind("owl", OWL)

# Print out the graph in RDF/XML format
print(g.serialize(format='xml'))

# Save the graph in RDF/XML format
g.serialize(destination='output.rdf', format='xml')


g.close
#This example creates an ontology for a library system with classes for Book and Author, and properties
# for hasAuthor, hasTitle, and hasName. It then creates instances of these classes and links them
# together. The output is a RDF/XML file that represents this data and the relationships between them.