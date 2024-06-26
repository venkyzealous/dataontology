
from owlready2 import *
owlready2.JAVA_EXE = "C:\\java\\Oracle_JDK-22\\bin\\java.exe"

# Create a new ontology
onto = get_ontology("http://test.org/onto.owl")

# Define classes and properties in the ontology
with onto:
    class Man(Thing):
        pass

    class Mortal(Thing):
        pass

    class is_mortal(ObjectProperty):
        domain = [Man]
        range = [Mortal]

    # Declare that Socrates is a man
    socrates = Man("Socrates")

# Save the ontology to a file
onto.save(file = "onto.owl", format = "rdfxml")

# Load the ontology with the reasoner
onto = get_ontology("onto.owl").load()

# Perform reasoning
sync_reasoner()

# Now we can query the ontology and the reasoner will infer that Socrates is mortal
print(socrates.is_a)


#In this example, we create an ontology with classes for `Man` and `Mortal`, and a property `is_mortal` that relates `Man` to `Mortal`. We declare that `Socrates` is a `Man`, and then use the reasoner to infer that `Socrates` is `Mortal`.

#This is a very simple example, but Owlready2 supports much more complex reasoning, and provides a Pythonic interface to OWL and the HermiT reasoner.