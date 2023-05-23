# SRP / SOC (Single Responsibility Principle / Seperation of Concerns)

# A class to hold personal Journal entries
class Journal:
    # constructor
    def __init__(self):
        self.entries = [] # List to hold journal entries
        self.count = 0 # Count of number of entries in the journal
    def add_entry(self, text): # method to add an entry to the journal
        self.count += 1 
        self.entries.append(f'{self.count}: {text}')
    def remove_entry(self, pos): # method to delete an entry at given position from the joirnal
        del self.entries[pos]
    def __str__(self): # string representation of journal entries
        return '\n'.join(self.entries)
    # THE METHODS BELOW ADD ADDITIONAL FUNCTIONALITY OF DATA PERSISTANCE TO THE CLASS FOR CREATING AND LOADING
    # THE JOURNAL FROM PARTICULAR RESOURCES. THIS IS A BAD IDEA BECAUSE YOU COULD HAVE AN APPLICATION WHERE
    # YOU HAVE DATA HOLDING CLASSES LIKE THIS JOURNAL CLASS. WHEN ALL THEESE CLASS TYPES HAVE TO BE PERSISTED, IT
    # MIGHT BE BETTER TO HAVE A SEPERATE CLASS THAT HANDLES SAVING AND LOADING SUCH DATA OBJECTS INSTEAD OF 
    # HAVING SAVE AND LOAD METHODS FOR EACH DATA CLASS WHICH WILL NEED MODIFICATION EVERYTIME SOME PRE/POST-SAVING
    # OR PRE/POST LOADING ACTION NEEDS TO BE TAKEN.
    # Now we break the SRP/SOC rule by giving the Journal class additional responsibilities that it never
    # really asked for.
    # def save(self, filename): # method to write the Journal entries to a file which breaks the SRP / SOC rule
    #     with open(filename, 'w') as fh:
    #         fh.write(str(self)) # write the string representation of journal entries to file
    # # method to load journal entries from an external file, this method also breaks SRP/SOC
    # def load(self, filename):
    #     fh = open(filename, 'w')
    #     content = fh.read()
    #     fh.close()
    # def load_from_url(self, uri): # method to load journal entries from a url
    #     pass

# BETTER WAY TO HANDLE THE PERSISTENCE OF DATA CLASSES IS TO HAVE A SEPERATE CLASS THAT HANDLES THAT 
# RESPONSIBILITY
class PersistenceManager:
    @staticmethod # class method
    def save_to_file(journal, filename):
        with open(filename, 'w') as fh:
            fh.write(str(journal))

# Create an instance of the class, populate it and use it
j = Journal()
j.add_entry("I cried today.")
j.add_entry("I ate a bug today.")
print(f'Journal Entries:\n{j}')

filename = r'/home/vavish/journal.txt'
PersistenceManager.save_to_file(j, filename); # Use the class method to save the Journal content to a file

with open(filename, 'r') as fh:
    print(fh.read())

# A COMMON ANTI-PATTERN (BAD PRACTICE) IS TO ADD EVERY FUNCTIONALITY INTO A SINGLE CLASS CREATING WHAT IS
# CALLED A GOD OBJECT. THE SINGLE RESPONSIBILITY PRINCIPLE PREVENTS THE CREATION OF SUCH LARGE GOD OBJECTS.