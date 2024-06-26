from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import OWL, XSD, RDFS
from rdflib.plugins.sparql import prepareQuery

# Create a namespace for our resources
n = Namespace("http://example.org/library/")
g = Graph()

g.parse("output.rdf",format="xml")

def find_books_by_author_in_genre(author_name, genre):
    # Define a SPARQL query
    query = prepareQuery(
        """
        SELECT ?book WHERE {
            ?book rdf:type ns:Book .
            ?book ns:hasAuthor ?author .
            ?author ns:hasName ?name .
            ?book ns:hasGenre ?genre .
            FILTER (str(?name) = "%s" && str(?genre) = "%s")
        }
        """ % (author_name, genre),
        initNs={"rdf": RDF, "ns": n}
    )

    # Execute the query and print out the results
    for row in g.query(query):
        print("Found book: %s" % row[0])

def get_context():
    context_data = {"Genre":"Novel"}
    return context_data



def get_parameter_from_user():
    # Ask the user for an author and a genre
    author_name = input("Enter an author's name: ")
    return author_name

# Get the context from the user
author_name, genre = get_parameter_from_user(), get_context().get("Genre", "")

# Test the function
#find_books_by_author_in_genre("F. Scott Fitzgerald", "Novel")
# Use the context to find books
find_books_by_author_in_genre(author_name, genre)

