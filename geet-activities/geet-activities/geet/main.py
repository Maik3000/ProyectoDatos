from utils.data_structures.linked_list import Node
import utils.status as status_utils
import utils.commit as commit_utils
import utils.init as init_utils
from pyfiglet import Figlet
import pickle
import click
import time
import sys
import os


@click.group()
def cli():
    pass


@cli.command()
def banner():

    figlet = Figlet(font='slant')
    print(figlet.renderText('geet'))


@cli.command()
def status():

    path = status_utils.get_current_path()
    new_files = status_utils.scan_for_new_files(path)
    deleted_files = status_utils.scan_for_deleted_files(path)
    modified_files = status_utils.scan_for_modified_files(path)

    status_message = '''
    On branch 'master'

    Uncommited changes:
        (use "geet commit -m <comment>..." to commit these changes)
    ''' 
    print(status_message)

    files_changed = False

    for file in deleted_files:
        files_changed = True
        print('             deleted:', file, end='\n')
    
    for file in modified_files:
        files_changed = True
        print('             modified:', file, end='\n')

    for file in new_files:
        files_changed = True
        print('             added:', file, end='\n')

    if not files_changed:
        print('        < There are no changes in the repository... >')


@cli.command()
def init():

    path = status_utils.get_current_path()
    initial_files = init_utils.get_init_files()
    repo_exists = init_utils.file_exists(path, '.geet')

    if repo_exists:
        print('Invalid operation: a geet repository already exists in this directory.')
        return None

    user_input = input('Creating geet repository in {} [press enter to continue]: '.format(path))
    
    if user_input != "":
        print('Canceling...')
        sys.exit(0)
 
    print('Initializing...')
    time.sleep(1)
    os.mkdir('.geet')
    os.mkdir('.geet/objects')

    for file in initial_files:
        init_utils.write_file(file, initial_files[file])

    # Creates master branch (linked list)
    branch_master = init_utils.create_branch(path) # NOTE: Activity no. 1 function invocation

    # Creates initial commit
    commit_tree = commit_utils.create_tree_object(path, 'Initial commit') # NOTE: Activity no. 2 main function call
    commit_utils.save_tree_object(path, commit_tree)
    branch_master.insert_last(Node(commit_tree.name, commit_tree.message, 'Angel Tortola', 'tortola@ufm.edu'))

    # Saves branch as pickle
    file_name = path + '.geet/branch'  

    '''
    TODO no. 3: Persist branch

    => Everytime we make a commit, we need to persist the latest version of the branch. In here, we'll persist for the first time our branch after making the initial commit.

        - Using the file_name provided above, persist the branch_master object in a pickle.

    ⬇ Your code starts here:
    '''
    with open(file_name, 'wb') as file:
        pickle.dump(branch_master, file) #sirve para guardar y serializar el objeto dentro del archivo
    '''
    ⬆ Your code ends here.
    '''

    print('Geet repository successfully created.')


@cli.command()
@click.option('-u', help='Author\'s name')
@click.option('-e', help='Author\'s email address')
def config(u, e):

    '''
    TODO no. 4: User config command

    => We'll use a simple python list in order to persist the author's name and email address.

        - We'll be able to update the authors data by using the following command: 
            geet config -u <username> -e <email>

        - Insert the parameters received into a list. The resulting list should look like this:
            [<username>, <email>]
    
        - Once you have the list, persist it into an object called 'user_config' in the hidden .geet folder.

        - Display in console the new user and email set.

    ⬇ Your code starts here:
    ''' 
def update_author_data(username, email):
        # Insertar los parámetros recibidos en una lista
        user_config = [username, email]
        
        # Guardar la lista en un archivo en la carpeta oculta .geet
        hidden_folder = ".geet"
        if not os.path.exists(hidden_folder):
            os.makedirs(hidden_folder)
        
        config_file = os.path.join(hidden_folder, "user_config.txt")
        with open(config_file, "w") as file:
            file.write(str(user_config))
        
        # Mostrar el nuevo nombre de usuario y correo electrónico configurados en la consola
        print("Username: ", username)
        print("Email: ", email)
# Ejemplo de uso

'''
    ⬆ Your code ends here.
'''


@cli.command()
@click.option('-m', help='Commit message')
def commit(m):


    path = status_utils.get_current_path()
    previous_hash_dict = status_utils.read_current_hash_dict(path)
    current_hash_dict = status_utils.get_hash_dict(path)

    if current_hash_dict == previous_hash_dict:
        print('\n     < No changes have been done, cannot commit. >')
        sys.exit(0)
    
    status_utils.save_hash_dict(path) 
    commit_tree = commit_utils.create_tree_object(path, m) # Creates commit tree object. NOTE: activity no. 2 call
    commit_utils.save_tree_object(path, commit_tree) # Saves commit in disk
    print('Creating commit with hash {}.'.format(commit_tree.name))
    print('Commit message: {}'.format(commit_tree.message))

    # Reads pickle and retrieves branch as linked list object
    branch_path = path + '.geet/branch'

    with open(branch_path, 'rb') as file:
        branch = pickle.load(file)

    '''
    TODO no. 5: Insert commit node

        => In the previous lines we just read our master branch object (Linked List), assigned to the 'branch' variable.

            - In this branch instance, use the insert_last(<node>) method to add the commit Node into the branch.

            - You'll need to create a Node object (node from Tree class, not LL). The 'name' and 'message' are already in the 'commit_tree' object.

            - To pass the 'username' and 'email' params, you'll have to read the previously persisted list (activity no. 4).

            - Lastly, overwrite the persisted version of the branch with the new one, just like you did in activity number 3.

    ⬇ Your code starts here:
    '''
    file_name = path + '.geet/branch'  


    # Lee la master branch del archivo pickle 
    with open(file_name, 'rb') as file:
        branch = pickle.load(file)

    # Crea un nodo de confirmacion usando el nombre y mensaje
    commit_node = Node(commit_tree.name, commit_tree.message, username, email)  

    # lee la persisted list para obtener el nombre y email 
    with open('persisted_list.pickle', 'rb') as file:
        persisted_list = pickle.load(file)
        username = persisted_list['username']
        email = persisted_list['email']

    # Acrualiza los valores anteriores y lo comitea
    commit_node.author = username
    commit_node.email = email
    branch.insert_last(commit_node)

    # reescribe
    with open(file_name, 'wb') as file:
        pickle.dump(branch, file)

    '''
    ⬆ Your code ends here.
    '''


@cli.command()
def log():

    path = status_utils.get_current_path()
    # Reads pickle and retrieves branch as linked list object
    branch_path = path + '.geet/branch'

    '''
    TODO no. 6: Read branch

        => In order to print a commit log, we'll need to bring to memory the persisted branch (Linked List). Then we'll need to reverse it so commits are printed from latest to oldest. 
        
            - Read the pickle saved at 'branch_path'.

            - Reverse the linked list with its reverse() method. 

    ⬇ Your code starts here:
    '''
def print_confirmation_log(branch_path):
    # Lea el archivo pickle almacenado en 'branch_path'
    with open(branch_path, 'rb') as file:
        branch = pickle.load(file)
    
    # Invierte la lista enlazada usando su método reverse()
    branch.reverse()
    
    # Imprimir el registro de confirmación
    for confirmation in branch:
        print(confirmation)
       
    # Ejemplo de uso
    branch_path = 'path/to/branch.pickle'
    print_confirmation_log(branch_path)
    branch = None # Remove. Added to avoid warning in line 211.
    '''
    ⬆ Your code ends here.
    '''

    print('[HEAD]\n')

    for commit in branch:
        print('Commit hash:', commit.hash)
        print('Commit message:', commit.message)
        print('Commit author:', commit.author)
        print('Commit contact:', commit.email, '\n')

    print('[Beginning of time]')


if __name__ == '__main__':
    cli()

@cli.command()
@click.option('-h', '--hash', help='Commit hash')
def delete_commit(hash):
    path = status_utils.get_current_path()
    branch_path = os.path.join(path, '.geet/branch.pickle')

    with open(branch_path, 'rb') as file:
        branch = pickle.load(file)

    branch.delete_commit(hash)

    with open(branch_path, 'wb') as file:
        pickle.dump(branch, file)