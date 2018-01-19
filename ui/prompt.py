'''
A prompt-based user interface module.
'''

class Prompt:
    '''A prompt-based user interface that accepts a dictionary of commands'''


    def __init__(self, commands, title):
        '''Build a new prompt interface'''
        self.commands = commands
        self.title = title


    def get_command_function(self, command_tokens, commands=None):
        '''Recursive function that returns the function for a given prompt command'''
        if commands is None:
            commands = self.commands

        command_root = command_tokens
        if isinstance(command_tokens, list):
            command_root = command_tokens[0]

        if command_root in commands:
            command_data = commands[command_root]
            if isinstance(command_data, dict):
                return self.get_command_function(command_tokens[1:], command_data)
            else:
                return command_data


    def get_command_list(self, command_data):
        '''Recursive function that returns a list of commands from a given command data'''
        command_list = []

        for command_key in command_data:
            command_value = command_data[command_key]
            if isinstance(command_value, dict):
                sub_commands = self.get_command_list(command_value)
                for sub_command in sub_commands:
                    command_list.append('%s %s' % (command_key, sub_command))
            else:
                command_list.append(command_key)

        return command_list


    def run(self):
        '''Main execution function for the prompt'''
        print('Welcome to %s' % self.title)

        running = True
        while running:
            try:
                command = input('~> ')
                if command.find(' ') > -1:
                    command = command.split(' ')
                command_function = self.get_command_function(command)
                if command_function:
                    command_function()
                elif command == 'help':
                    self.usage()
                elif command == 'quit':
                    running = not running
                else:
                    print('Unknown command: %s' % command)
                    print('Use "help" for a list of commands.')
            except KeyboardInterrupt:
                print('')
        print('Shutting down %s' % self.title)


    def usage(self):
        '''Display a list of all possible commands'''
        command_list = self.get_command_list(self.commands)
        command_list.sort()

        print('Available commands:')
        for command in command_list:
            print('  %s' % command)
