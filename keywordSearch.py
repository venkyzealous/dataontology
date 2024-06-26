from rdflib.plugins.sparql import prepareQuery

# Define a function for finding books by a given author
def find_books_by_author(author_name):
    # Define a SPARQL query
    query = prepareQuery(
        """
        SELECT ?book WHERE {
            ?book rdf:type ns:Book .
            ?book ns:hasAuthor ?author .
            ?author ns:hasName ?name .
            FILTER (str(?name) = "%s")
        }
        """ % author_name,
        initNs={"rdf": RDF, "ns": n}
    )

    # Execute the query and print out the results
    for row in g.query(query):
        print("Found book: %s" % row[0])

# Test the function
find_books_by_author("F. Scott Fitzgerald")

#In this code, we first define a function find_books_by_author that takes an author's name as input. Inside this function, we define a SPARQL query that finds all books whose author has the given name. We then execute this query on our graph g and print out the results.

#Note that the prepareQuery function takes a SPARQL query string and a dictionary of namespace prefixes. In our query, we use the rdf:type property to find all resources of type Book, and the hasAuthor and hasName properties to find the author's name. We use the FILTER function to restrict the results to books whose author's name matches the input.

#Finally, we test our function by finding all books by "F. Scott Fitzgerald". This should print out the URI of the book "The Great Gatsby" that we added to our graph earlier.