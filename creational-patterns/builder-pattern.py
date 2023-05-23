# Used when construction gets a little bit too complicated
# Some objects are simple and can be created in a single initializer call
# Other objects require a lot of ceremony to create
# Having an object with 10 different initializer arguments is not productive. Instead, we can opt for
# Piece-wise construction (step-by-step construction of objects)

# A Builder class is used as a seperate component for building an object of another Class. You can
# either use the Builder class directly using its initializer (constructor), or expose it
# through a class method. You can create chainable builder methods (by returning the object being
# built in each method) to make the builder fluent. Different facets of an object can be built with
# different builders working in tandem via a base class.

# Builder - when piecewise object construction is complicated, the Builder provides an API for
# doing it succinctly.

# Construct a paragraph out of a chunk of text
text = 'hello'
parts = ['<p>', text, '</p>']
print(''.join(parts))

words = ['hello', 'world']
parts = ['<ul>']
for w in words:
    parts.append(f' <li>{w}</li>')
parts.append('</ul>')
print('\n'.join(parts))


# Class to construct HTML content
class HtmlElement:
    indent_size = 2

    def __init__(self, name='', text=''):
        self.text = text  # tag text content
        self.name = name  # tag name
        self.elements = []  # other internal elements

    def __str(self, indent):  # Note that this is not __str__()

        lines = []
        i = ' ' * (indent * self.indent_size)  # indentation spacing
        lines.append(f'{i}<{self.name}>')  # opening tag of current element

        if self.text:
            i1 = ' ' * ((indent + 1) * self.indent_size)
            lines.append(f'{i1}{self.text}')

        # Recursively call for other elements within the opening and closing tags
        for e in self.elements:
            lines.append(e.__str(indent + 1))

        lines.append(f'{i}</{self.name}>')  # closing tag of current element
        return '\n'.join(lines)  # return the built HTML content

    def __str__(self):
        # The indentation starts with 0 spaces for the top level tag by default
        return self.__str(0)

    # The 'staticmethod' decorator is used to declare class methods in python
    @staticmethod
    def create(name):
        return HtmlBuilder(name)


# Take an HtmlElement instance and build it up
class HtmlBuilder:
    # root_name is the name of the top-level tag of the HtmlElement instance
    def __init__(self, root_name):
        self.root_name = root_name
        self.__root = HtmlElement(name=root_name)

    def add_child(self, child_name, child_text):
        self.__root.elements.append(
            HtmlElement(name=child_name, text=child_text))

    # Creating a chainable, fluent, Interface
    def add_child_fluent(self, child_name, child_text):
        self.__root.elements.append(
            HtmlElement(name=child_name, text=child_text))
        return self

    def __str__(self):
        return str(self.__root)

    # We can also expose the HtmlBuilder class using a class method
    # The 'staticmethod' decorator is used to declare class methods in python
    # However, keep in mind that since the HtmlElement and HtmlBuilder classes are entangled (connected),
    # we cannot expose the HtmlBuilder like this when the HtmlElement implementation is in another
    # seperate python file for example (or split physically into seperate applications).
    @staticmethod
    def create(name):
        return HtmlElement(name=name)


# builder = HtmlElement.create('ul')
builder = HtmlBuilder('ul')
# builder.add_child('li', 'hello')
# builder.add_child('li', 'world')
builder.add_child_fluent('li', 'hello').add_child_fluent(
    'li', 'world')  # using chaining
print('Ordinary Builder:')
print(builder)  # calls the __str__() in the builder object


# SOMETIMES, OBJECTS GET SO COMPLICATED THAT YOU WOULD NEED SEVERAL BUILDERS TO BUILD IT
# IN SUCH CASES, HOW CAN YOU BUILD A FLUENT INTERFACE TO JUMP FROM ONE BUILDER TO ANOTHER ?

# ONE APPROACH IS AS FOLLOWS (THIS APPROACH BREAKS THE OPEN-CLOSED PRINCIPLE!)

class Person:
    def __init__(self):
        # address
        self.street_address = None
        self.postcode = None
        self.city = None
        # employment
        self.company_name = None
        self.position = None
        self.annual_income = None

    def __str__(self):
        return f'Address: {self.street_address}, {self.postcode}, {self.city}' + \
            f'Employed at {self.company_name} as a {self.position} earning {self.annual_income}'


# base class
class PersonBuilder:
    # 'person' is a new instance of 'Person' class by default
    def __init__(self, person=Person()):
        # This creates a blank slate to work with when the builder is first constructed
        # This allows the sub-builders to work on already constructed instances
        self.person = person
        # instead of creating a new 'Person' class instance

    # These properties allow jumping between the two sub-builders
    @property
    def works(self):
        # return an instance of 'Person' class that is combined with the 'PersonJobBuilder' class
        # to allow for self-contained building utilities
        return PersonJobBuilder(self.person)

    @property
    def lives(self):
        # return an instance of 'Person' class that is combined with the 'PersonAddressBuilder' class
        # to allow for self-contained building utilities
        return PersonAddressBuilder(self.person)

    # method to return the current state of the 'Person' class instance used in this class
    def build(self):
        return self.person


class PersonJobBuilder(PersonBuilder):
    def __init__(self, person):
        # This breaks the open-close principle as this allows the sub class methods to
        # modify the base class
        super().__init__(person)  # calling the constructor of parent class (PersonBuilder)

    def at(self, company_name):
        self.person.company_name = company_name
        return self  # making a chainable fluent interface

    def as_a(self, position):
        self.person.position = position
        return self  # making a chainable fluent interface

    def earning(self, annual_income):
        self.person.annual_income = annual_income
        return self  # making a chainable fluent interface


class PersonAddressBuilder(PersonBuilder):
    def __init__(self, person):
        # This breaks the open-close principle as this allows the sub class methods to
        # modify the base class
        super().__init__(person)  # calling the constructor of parent class (PersonBuilder)

    def at(self, street_address):
        self.person.street_address = street_address
        return self  # making a chainable fluent interface

    def with_postcode(self, postcode):
        self.person.postcode = postcode
        return self  # making a chainable fluent interface

    def in_city(self, city):
        self.person.city = city
        return self  # making a chainable fluent interface


# You can also use a class method in the 'Person' class to expose the 'PersonBuilder' construction
pb = PersonBuilder()
# Now you can chain the properties 'lives' and 'works' to move from one sub-builder to another
person = pb\
    .lives\
    .at('123, London Road')\
    .in_city('London')\
    .with_postcode('SW12BC')\
    .works\
    .at('Fabrikam')\
    .as_a('Engineer')\
    .earning(123000)\
    .build()

print(person)  # invokes the '__str__()' method of the 'Person' class instance!


# NORE: AS MENTIONED EARLIER, THE APPROACH USED ABOVE BREAKS THE OPEN-CLOSED PRINCIPLE BECAUSE
# WE MODIFY THE BASE CLASS FUNCTIONALITY THROUGH SUB CLASSES THAT INHERIT IT.
# THERE IS A DIFFERENT APPROACH WHICH DOES NOT CAUSE THIS ISSUE BY USING MULTI-LEVEL INHERITANCE:


class PersonNew:
    def __init__(self):
        self.name = None
        self.position = None
        self.date_of_birth = None

    def __str__(self):
        return f'{self.name} born on {self.date_of_birth} ' +\
            f'works as {self.position}'

    @staticmethod
    def new():
        return PersonBuilderNew()


class PersonBuilderNew:
    def __init__(self):
        self.person = PersonNew()

    def build(self):
        return self.person


class PersonInfoBuilder(PersonBuilderNew):
    def called(self, name):
        self.person.name = name
        return self  # making a chainable fluent interface


class PersonJobBuilderNew(PersonInfoBuilder):
    def works(self, position):
        self.person.position = position
        return self  # making a chainable fluent interface


class PersonBirthDateBuilder(PersonJobBuilderNew):
    def born(self, date_of_birth):
        self.person.date_of_birth = date_of_birth
        return self  # making a chainable fluent interface


pb = PersonBirthDateBuilder()
me = pb\
    .called('Dimitri')\
    .works('Quant')\
    .born('1/1/1980')\
    .build()

print(me)


# EXERCISE:


from unittest import TestCase

class Class:
    def __init__(self, name):
        self.name = name
        self.fields = []

    def __str__(self):
        result = []
        result.append('class {}:'.format(self.name))
        if (len(self.fields) == 0):
            result.append('  pass')
        else:
            result.append('  def __init__(self):')
            for (name, type) in self.fields:
                result.append('    self.{} = {}'.format(name, type))
        return '\n'.join(result)


class CodeBuilder:
    def __init__(self, root_name):
        self.__class = Class(root_name)

    def add_field(self, type, name):
        self.__class.fields.append((type, name))
        return self
    
    def __str__(self):
        return self.__class.__str__()

class Evaluate(TestCase):
    @staticmethod
    def preprocess(s=''):
        return s.strip().replace('\r\n', '\n')

    def test_empty(self):
        cb = CodeBuilder('Foo')
        self.assertEqual(
            self.preprocess(str(cb)),
            'class Foo:\n  pass'
        )

    def test_person(self):
        cb = CodeBuilder('Person').add_field('name', '""') \
            .add_field('age', 0)
        self.assertEqual(self.preprocess(str(cb)),
                         """class Person:
  def __init__(self):
    self.name = \"\"
    self.age = 0""")
        

e = Evaluate()
e.test_empty()
e.test_person()
