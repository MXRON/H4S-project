import sys
import sqlite3
import datetime
import string
import random

# connecting to database
conn = sqlite3.connect('db1')
c = conn.cursor()


# functions for creating and reading content
def password_generator(length):
    # count is the total length of password, we minus values from it in order to generate a password with this length
    count = int(length)
    # we divide the whole length by 3 so that a maximum of a 1/3 of proportion can be given to letters
    stop = int(count / 2)
    password = []
    # num is the random number for the proportion of letters out of the total length of password
    num = random.randint(0, stop)
    count -= num
    # generating random letters including upper and lower case letters
    while num > 0:
        # while the proportion generated is positive a random letter will be added
        lttr = random.choice(string.ascii_lowercase)
        case = random.choice(['lower', 'upper'])
        if case == 'lower':
            password.append(lttr.lower())
        else:
            password.append(lttr.upper())
        num -= 1

    if count > 0:
        num2 = random.randint(0, int(count))
        count -= num2
        while num2 > 0:
            integer = random.randint(0, 10)
            password.append(str(integer))
            num2 -= 1
    if count > 0:
        while count > 0:
            symbols = random.choice("<>,*):('.!-?; []")
            password.append(symbols)
            count -= 1

    # Shuffling the password list and returning a string
    random.shuffle(password)
    # joining the password list and returning it
    return ''.join(password)


def creating_content():
    global dashes_
    # to generate a random password the length, username and website, while password is set to the generator function
    pass_ = input('Use generated password (G)\nOwn password (O)')
    # character length for the password generator are inputted and the generated password is generated
    if pass_.lower() == 'g':
        length = input('Character length of password: ')
        username = input(dashes + 'Username: ')
        password = password_generator(length)
        print('Password: ' + str(password) + dashes_)

        while True:
            # another password is generated and displayed using the while loop until c is entered
            another = input("Generate another password(G)\nContinue(C)")
            if another.lower() == 'g':
                password = password_generator(length)
                print(dashes_ + '\nUsername: ' + username + '\nPassword: ' + str(password) + dashes_)

            if another.lower() == 'c':
                with conn:
                    website = input('Website: ')
                    # the date of entry is calculated using:
                    today = datetime.date.today()
                    # the values are added to the ROOT2 table and a success message is printed
                    c.execute('INSERT INTO ROOT2 VALUES (?,?,?,?)', (username, password, website, today))
                    print(dashes + f'({username}, {password}, {website}, {today})' + '\nContent successfully added!')
                    break

    if pass_.lower() == 'o':
        # details for the content are inputted manually and then added to the table
        with conn:
            username = input('Username: ')
            password = input('Password: ')
            website = input('Website: ')
            today = datetime.date.today()

            c.execute('INSERT INTO ROOT2 VALUES (?,?,?,?)', (username, password, website, today))
            print(dashes + f'({username}, {password}, {website}, {today}\n' + 'Content successfully added!')


def reading_content(web='to be inputted from user'):
    while True:
        global c
        if web == 'to be inputted from user':
            specific_or_all = input(dashes + "Specific website(S)\nAll websites(A)")

            if specific_or_all.lower() == 's':
                web_name = input(dashes + 'Website name: ')

                # to check that this content exists, the table is checked, if None is returned process is restarted
                c.execute("SELECT * FROM ROOT2 WHERE website=?", (str(web_name),))
                data = c.fetchone()

                if data is None:
                    try_again = input('Entered website has not been found\nTry again (Y/N)')
                    # the loop is restarted or broken depending on the input
                    if try_again.lower() == 'y':
                        continue
                    if try_again.lower() == 'n':
                        break
                # if the content is present it is displayed
                else:
                    return data
            # fetching all of the data if this is wanted by the user
            if specific_or_all.lower() == 'a':
                c.execute("SELECT * FROM ROOT2")
                all_data = c.fetchall()

                if all_data is None:
                    print('This table contains no data!')
                    # if there is no content, then the it is offered to create content
                    create_content = input('Create content now (Y/N)')
                    if create_content.lower() == 'y':
                        creating_content()
                        break
                    else:
                        break
                else:
                    return [print(row) for row in all_data]

        if web == 'all':
            c.execute("SELECT * FROM ROOT2")
            all_data = c.fetchall()

            if all_data is None:
                print('This table contains no data!')
                # if there is no content, then the it is offered to create content
                create_content = input('Create content now (Y/N)')
                if create_content.lower() == 'y':
                    creating_content()
                    break
                else:
                    break
            else:
                return [print(row) for row in all_data]

            # else is added so that content can be seen when using the update and delete function
        else:
            c.execute("SELECT * FROM ROOT2 WHERE Website=?", (str(web),))
            data = c.fetchone()

            if data is None:
                no_content = input('Entered website has not been found\nCreate content for this website(CC)\n'
                                   'Quit(Q)' + dashes_)
                # as this part of the function is only used for the update and delete functions, if no content is found
                # then option of creating content is presented which is then triggered by the creating content function
                if no_content.lower() == 'cc':
                    creating_content()
                    return 'creating content do not update'

                if no_content.lower() == 'q':
                    break
            # if the content is present it is displayed for the delete and update functions
            else:
                print('Current content:')
                return data


def update_content():
    global dashes_
    with conn:
        while True:
            # displaying the current content for the inputted website using the reading_content function
            web = input('Website to update content for: ')
            print(dashes_)
            current = reading_content(web=web)
            if current == 'creating content do not update':
                break

            else:
                print(current)
                print(dashes)
                # updating a specific part of the content or all of it
                which = input('Update password (P)\nUpdate username (U) ')
                # new password/username are taken in the table is updated and the updated content is displayed
                # if password needs to be updated then the option of generating one is given
                if which.lower() == 'p':
                    _type_ = input(dashes + 'Generate password (G)\nOwn password (O) ')
                    # if the password needs to be generated then the password generator will be called in a loop with
                    # the length specified
                    if _type_.lower() == 'g':
                        length_ = input(dashes + 'Length of password: ')

                        while True:
                            new_password = password_generator(length_)
                            print(dashes + 'New password: ' + new_password)
                            again_ = input('Generate another(G)\nContinue(C) ')

                            if again_.lower() == 'g':
                                continue
                            if again_.lower() == 'c':
                                # if user is happy with generated password then the password is inserted into the
                                # table and the current details are displayed
                                c.execute("""UPDATE ROOT2 SET password = (?) WHERE website = (?)""",
                                          (new_password, web))
                                print(dashes + 'Content updated!' + dashes_)
                                reading_content(web=web)
                                print(dashes)
                                break

                    if _type_.lower() == 'o':
                        new_password = input('New password: ')
                        c.execute("""UPDATE ROOT2 SET password = (?) WHERE website = (?)""", (new_password, web))
                        print(dashes + 'Content updated!' + dashes_)
                        new_content = reading_content(web=web)
                        print(new_content)
                        print(dashes)
                # if username is chosen, the new username is inputted and inserted into the table, the current
                # details are then displayed
                if which.lower() == 'u':
                    new_username = input(dashes + 'New username: ')
                    c.execute("""UPDATE ROOT2 SET username = (?) WHERE website = (?)""", (new_username, web))
                    print(dashes + 'Content updated!' + dashes_)
                    new_content = reading_content(web=web)
                    print(new_content)
                    print(dashes)


def again():
    global running, first_time
    while True:
        more = input('More requests(M)\nQuit(Q)')
        if more.lower() == 'm':
            running = True
            first_time = 'no'
            return running

        if more.lower() == 'q':
            sys.exit()


def welcome_screen(type_=''):
    global action
    # the whole welcome screen is displayed
    if type_ == '':
        print(dashes + 'Welcome back to db1 table ROOT2\n' + dashes +
              'All content is displayed as:\n(Username, Password, Website, Date)\n' + dashes + 'COMMANDS ARE:')

        action = input("'r' to read content\n'cc' to create content\n'q' to quite the program\n'u' to update content\n"
                       "'d' to delete content\n" + dashes)
        return action
    # only commands are displayed
    if type_ == 'again':
        print(dashes + 'COMMANDS ARE:')
        action = input("'r' to read content\n'cc' to create content\n'q' to quite the program\n'u' to update content\n"
                       "'d' to delete content\n" + dashes)
    return action


def delete_content():
    global dashes_, loop2, loop1, loop3, loop4
    with conn:
        while True:
            # Given the option of deleting something specific or everything
            all_or_specific = input('Delete ALL content (A) or Specific content (S) ')
            if all_or_specific.lower() == 'a':
                loop1 = True
                break
            if all_or_specific.lower() == 's':
                loop3 = True
                break

        while loop1:
            see = input('See all of the content first (Y/N) ')
            if see.lower() == 'y':
                print(dashes_)
                reading_content(web='all')
                print(dashes)
                loop1 = False
                loop2 = True
            if see.lower() == 'n':
                break
            else:
                continue
        # all the content is deleted in loop2
        while loop2:
            sure = input('Are you sure you want to delete ALL content (Y/N) ')
            if sure.lower() == 'y':
                c.execute('SELECT * FROM ROOT2')
                c.execute('TRUNCATE TABLE ROOT2')
                return print('All content successfully deleted')

            if sure.lower() == 'n':
                break

        # get an input of the website to be deleted and print out the current contents
        while loop3:
            web_name = input('Website to DELETE content for: ')
            print(dashes_)
            reading_content(web=web_name)
            print(dashes)
            loop3 = False
            loop4 = True

        # the row is deleted if the user is sure
        while loop4:
            sure = input(f'\nAre you sure that you want to delete content for {web_name} (Y/N) ')
            if sure.lower() == 'y':
                c.execute('DELETE FROM ROOT2 WHERE website ==?', (str(web_name),))
                print(dashes_ + f'Content for {web_name} successfully deleted!' + dashes)
            if sure.lower() == 'n':
                break
            else:
                continue


# START. Trying to create a table or connect if it already exists
try:
    c.execute('''CREATE TABLE ROOT2 
    (Username text,  
    Password text, 
    Website text, 
    Date integer)''')
    print("Safe 'ROOT2' has been created")

except sqlite3.OperationalError:
    print("ROOT2 already created")

# global variables are created
dashes = '******************************\n'
dashes_ = '\n******************************'
action = ''
first_time = 'first'
loop1 = False
loop2 = False
loop3 = False
loop4 = False

# Responding to commands
running = True
while running:
    if first_time == 'first':
        welcome_screen()

    if action.lower() == 'q':
        sys.exit()

    if action.lower() == 'cc':
        creating_content()
        again()
        welcome_screen('again')

    if action.lower() == 'r':
        reading_content()
        again()
        welcome_screen('again')

    if action.lower() == 'u':
        update_content()
        again()
        welcome_screen('again')

    if action.lower() == 'd':
        delete_content()
        again()
        welcome_screen('again')

conn.commit()
conn.close()
