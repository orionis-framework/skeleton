from orionis.luminate.console.base.command import BaseCommand

class WelcomeCommand(BaseCommand):
    """
    A command class for Orionis that demonstrates basic functionality.

    This class defines a custom console command that can be executed
    from the command line interface (CLI) of a Orionis application. The
    command `app:example` will display a greeting message.

    Attributes
    ----------
    signature : str
        The unique command signature used to register the command with the CLI.
    description : str
        A short description of what the command does.

    Methods
    -------
    arguments() -> list
        Defines the arguments that the command accepts, with type and help information.
    handle(**kwargs) -> None
        Executes the logic of the command. In this case, it prints a greeting message.
    """

    signature = 'app:example'
    """
    str : The command signature.

    This is the unique string that represents the command when invoking it from the CLI.
    It is used for registering the command in the Orionis framework.
    """

    description = 'Greets from the console'
    """
    str : A brief description of the command's functionality.

    This description provides a short explanation of what the command does, and
    is shown in the CLI help for the command.
    """

    def arguments(self):
        """
        Defines the command-line arguments for the command.

        The `arguments` method returns a list of tuples, where each tuple consists
        of the argument's name and a dictionary that defines its properties (type,
        whether it's required, and its help description).

        Returns
        -------
        list
            A list of tuples, each containing an argument's name and associated
            metadata (type, required status, and help description).
        """
        return [
            # ('--argument', {'type': str, 'required': True, 'help': 'Description of the argument'}),
        ]

    def handle(self, **kwargs) -> None:
        """
        Executes the command's logic.

        The `handle` method is called when the command is executed. In this case,
        it simply prints a greeting message to the console.

        Parameters
        ----------
        **kwargs : dict
            A dictionary of keyword arguments passed to the command. These arguments
            correspond to the arguments defined in the `arguments()` method.

        Returns
        -------
        None
            This method does not return any value, but performs side effects such as
            printing a message to the console.
        """
        self.info(f'Welcome to Orionis Framework!')

