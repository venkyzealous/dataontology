""" Sure, let's consider a more complex example related to medical diagnosis. Suppose we have an ontology that includes information about diseases, symptoms, and patients. We could use an OWL reasoner to infer potential diagnoses for patients based on their symptoms.

Here's a simplified version of how you might set this up using Owlready2: """

#```python
from owlready2 import *
import owlready2 as owl

from rdflib import OWL, RDF, URIRef
owlready2.JAVA_EXE = "C:\\java\\Oracle_JDK-22\\bin\\java.exe"


# Create a new ontology
onto = get_ontology("http://test.org/onto.owl")

# Define classes and properties in the ontology
with onto:
    class Disease(Thing):
        pass

    class Symptom(Thing):
        pass

    class Patient(Thing):
        pass

    class has_symptom(ObjectProperty):
        domain = [Patient]
        range = [Symptom]

    class indicates(Symptom >> Disease, ObjectProperty):
        pass

    # Define some diseases and symptoms
    class Flu(Disease):
        pass

    class Fever(Symptom):
        pass
    class SustainedFever(Fever):
        pass
    
    class Drug(Thing):
        def take(self): print("I took a drug")

    class ActivePrinciple(Thing):
        pass

    class has_for_active_principle(Drug >> ActivePrinciple):
        python_name = "active_principles"

    class Placebo(Drug):
        equivalent_to = [Drug & Not(has_for_active_principle.some(ActivePrinciple))]
        def take(self): print("I took a placebo")

    class SingleActivePrincipleDrug(Drug):
        equivalent_to = [Drug & has_for_active_principle.exactly(1, ActivePrinciple)]
        def take(self): print("I took a drug with a single active principle")

    class DrugAssociation(Drug):
        equivalent_to = [Drug & has_for_active_principle.min(2, ActivePrinciple)]
        def take(self): print("I took a drug with %s active principles" % len(self.active_principles))



    fever = Fever("fever")
    flu = Flu("flu")
    sustained_fever = SustainedFever("sustained_fever")
    fever.indicates.append(flu)

    # State that fever indicates flu
    #Fever.indicates.append(Flu)

    # Define a patient with a fever
    john = Patient("John")
#    john.has_symptom.append(Fever)
    john.has_symptom.append(fever)
    john.has_symptom.append(sustained_fever)


    acetaminophen   = ActivePrinciple("acetaminophen")
    amoxicillin     = ActivePrinciple("amoxicillin")
    clavulanic_acid = ActivePrinciple("clavulanic_acid")

    AllDifferent([acetaminophen, amoxicillin, clavulanic_acid]) #Being an open world, needs to be explicitly told their equivalence is false

    drug1 = Drug(active_principles = [acetaminophen])
    drug2 = Drug(active_principles = [amoxicillin, clavulanic_acid])
    drug3 = Drug(active_principles = [])

    close_world(Drug)


    # Manually state that 'indicates' is a transitive property using RDFlib
    #graph = onto.world.as_rdflib_graph()
    #graph.add((URIRef(onto.base_iri + "indicates"), RDF.type, OWL.TransitiveProperty))

# Save the ontology to a file
onto.save(file = "onto.owl", format = "rdfxml")

# Load the ontology with the reasoner
onto = get_ontology("onto.owl").load()


# Replace 'path_to_Hermit' with the actual path of the HermiT .jar file
#default_world.set_reasoner(hermit="path_to_Hermit")
# Perform reasoning
sync_reasoner()

#
# SELECT ?disease WHERE {
#    :John :has_symptom/:indicates ?disease .
#  }


# Now we can query the ontology and the reasoner will infer potential diagnoses for John
#print(list(onto.query("""
# SELECT ?disease WHERE {
#   :John :has_symptom/:indicates ?disease .
# }
#""", initNs = { "": onto })))
#```


#Reasoning - Automatic Classification
print("drug1 Class:", drug1.__class__)
print("drug2 Class:", drug2.__class__)
print("drug3 Class:", drug3.__class__)



print(john)


'''
In this code, we define a `has_symptom` property that relates `Patient` to `Symptom`, and an `indicates` property that relates `Symptom` to `Disease`. We state that `Fever` indicates `Flu`, and that a patient `John` has a `Fever`. We then use the reasoner to infer potential diseases that John might have based on his symptoms.

The output of the query will be a list of potential diseases for John, inferred from his symptoms:

```python
[[onto.Flu]]
```

This indicates that John might have the flu, based on the fact that he has a fever and that fever is a symptom of the flu.

This is a very simplified example, but it gives you an idea of the power of reasoning with OWL and RDF. In a real-world medical ontology, you might have hundreds or thousands of diseases and symptoms, and complex relationships between them. A reasoner could help doctors make diagnoses, suggest tests, identify potential risks, and more.'''



with onto:
    class Person(owl.Thing):
        pass

    class has_brother(owl.ObjectProperty, owl.SymmetricProperty, owl.IrreflexiveProperty):
        domain = [Person]
        range = [Person]
    
    class has_child(Person >> Person):
        pass
    
    class has_uncle(Person >> Person):
        pass

    rule1 = owl.Imp()
    rule1.set_as_rule(
        "has_brother(?p, ?b), has_child(?p, ?c) -> has_uncle(?c, ?b)"
    )

    # This rule gives "irreflexive transitivity",
    # i.e. transitivity, as long it does not lead to has_brother(?a, ?a)"
    rule2 = owl.Imp()
    rule2.set_as_rule(
        "has_brother(?a, ?b), has_brother(?b, ?c), differentFrom(?a, ?c) -> has_brother(?a, ?c)"
    )
    
david = Person("David")
john = Person("John")
pete = Person("Pete")
anna = Person("Anna")
simon = Person("Simon")

owl.AllDifferent([david, john, pete, anna, simon])

david.has_brother.extend([john, pete])

john.has_child.append(anna)
pete.has_child.append(simon)

print("Uncles of Anna:", anna.has_uncle) # -> []
print("Uncles of Simon:", simon.has_uncle) # -> []
owl.sync_reasoner(infer_property_values=True, debug=False)
print("Uncles of Anna:", anna.has_uncle) # -> [onto.Pete, onto.David]
print("Uncles of Simon:", simon.has_uncle) # -> [onto.John, onto.David]
print ("David has brother:", david.has_brother)
print("Pete has brother:",pete.has_brother)
print("John has brother:",john.has_brother)

# Save the ontology to a file
onto.save(file = "onto.owl", format = "rdfxml")

# Load the ontology with the reasoner
onto = get_ontology("onto.owl").load()



# applications , challenges that lead to this, what other things we can do with this soln
# various audiences