from . import name_generator


class BaseNPC:
    """
    The base class for NPCs.

    Class Attributes:
        people (str): The name of the people.
        name_templates (list): Language rules for syllable definitions and counts; refer to the name_generator module.

    Instance Attributes:
        name (str): The NPC's randomly-generated name.
    """

    people = None
    name_templates = []

    def __init__(self):
        self._name = None

    @property
    def name(self):
        """
        Return a cached, randomized full name for this NPC as a string.
        """
        if not self._name:
            generator = name_generator.Generator(people=self.people, validator=self.__class__.validate_name)
            names = []
            for (template, weights) in self.__class__.name_templates:
                names.append(generator.generate(template=template, weights=weights))
            self._name = self.__class__.full_name(names)
        return self._name

    @staticmethod
    def full_name(names):
        """
        Format the NPC's individual names for display as a single string.

        This method is used by the name() property to format the NPC's name for display. By default, names are joined by
        spaces and capitalized, but you can override this method in your people's subclass.

        Args:
            names (list): A list of name_generator.Name instances

        Returns:
            string: The NPC's full name as a single string.
        """
        return ' '.join([n.capitalize() for n in names])

    @staticmethod
    def validate_name(name):
        """
        Validate that a single name (not the NPC's full name) is valid. Used by the name generator to decide if a
        randomly-generated name is appropriate. You probably want to override this in your people's class.

        Args:
            name (name_generator.Name): The name to validate.

        Returns:
            bool: True if the name is valid, False otherwise.
        """
        return True

    def __repr__(self):
        return self.name
